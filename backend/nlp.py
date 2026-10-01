import re
import math
from collections import Counter, defaultdict
from typing import List, Dict, Any, Tuple
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize VADER analyzer
vader_analyzer = SentimentIntensityAnalyzer()

# Standard English stop words + common conversational fillers
STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", 
    "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", 
    "but", "by", "can", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", 
    "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", 
    "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", 
    "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", 
    "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", 
    "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", 
    "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", 
    "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", 
    "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", 
    "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", 
    "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", 
    "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", 
    "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", 
    "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", 
    "yours", "yourself", "yourselves", "will", "just", "like", "also", "even", "really", "get", 
    "got", "one", "two", "much", "many", "well", "way", "back", "still", "make", "made", 
    "think", "know", "see", "went", "day", "time", "thing", "things", "first", "second"
}

# Domain-specific generic words that don't add semantic value when isolated
GENERIC_DOMAIN_WORDS = {
    "product", "item", "movie", "film", "restaurant", "food", "app", "application", "place"
}

def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Computes sentiment metrics using VADER (Valence Aware Dictionary for sEntiment Reasoning).
    Classifies compound score:
      - Positive: compound >= 0.05
      - Neutral:  -0.05 < compound < 0.05
      - Negative: compound <= -0.05
    """
    if not text or not text.strip():
        return {
            "compound": 0.0,
            "pos": 0.0,
            "neu": 1.0,
            "neg": 0.0,
            "label": "neutral",
            "intensity": 0.0
        }

    scores = vader_analyzer.polarity_scores(text)
    compound = round(scores["compound"], 3)
    
    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"

    # Identify any prominent sentiment cue words present in text for UI explanation
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    cues = []
    for w in set(words):
        if w in vader_analyzer.lexicon:
            valence = vader_analyzer.lexicon[w]
            if abs(valence) >= 1.5:
                cues.append({
                    "word": w,
                    "valence": valence,
                    "type": "positive" if valence > 0 else "negative"
                })
    cues.sort(key=lambda x: abs(x["valence"]), reverse=True)

    return {
        "compound": compound,
        "pos": round(scores["pos"], 3),
        "neu": round(scores["neu"], 3),
        "neg": round(scores["neg"], 3),
        "label": label,
        "intensity": round(abs(compound) * 100, 1),
        "sentiment_cues": cues[:6]
    }

def clean_and_tokenize(text: str) -> List[str]:
    """Cleans text and extracts alphanumeric words."""
    cleaned = re.sub(r"[^\w\s-]", " ", text.lower())
    tokens = [t for t in cleaned.split() if len(t) >= 3 and not t.isdigit()]
    return tokens

def extract_topics_and_keywords(reviews_data: List[Dict[str, Any]], top_n: int = 18) -> List[Dict[str, Any]]:
    """
    Performs TF-IDF and N-gram keyword/topic extraction across a collection of reviews.
    Associates each topic with sentiment polarity from the reviews it appears in.
    """
    if not reviews_data:
        return []

    num_docs = len(reviews_data)
    
    # 1. Document frequency map and term frequency tracking
    doc_freq = Counter()
    term_freq = Counter()
    term_sentiment_scores = defaultdict(list)
    
    for rev in reviews_data:
        full_text = f"{rev.get('title', '')} {rev.get('text', '')}"
        tokens = clean_and_tokenize(full_text)
        
        # Filter tokens
        filtered_tokens = [w for w in tokens if w not in STOP_WORDS and w not in GENERIC_DOMAIN_WORDS]
        
        # Generate unigrams
        doc_terms = set(filtered_tokens)
        
        # Generate informative bigrams (e.g., 'battery life', 'customer service')
        bigrams = []
        for i in range(len(tokens) - 1):
            w1, w2 = tokens[i], tokens[i + 1]
            if (w1 not in STOP_WORDS or w1 in {"no", "not"}) and (w2 not in STOP_WORDS):
                if len(w1) >= 3 and len(w2) >= 3:
                    bigram = f"{w1} {w2}"
                    bigrams.append(bigram)
        
        doc_terms.update(bigrams)
        
        # Update counts
        for term in doc_terms:
            doc_freq[term] += 1
            compound = rev.get("compound_score", 0.0) or 0.0
            term_sentiment_scores[term].append(compound)
            
        for term in filtered_tokens + bigrams:
            term_freq[term] += 1

    # 2. Compute TF-IDF Score
    # Minimum occurrences: at least 2 reviews or top occurring
    min_count = 2 if num_docs >= 10 else 1
    scored_terms = []

    for term, count in term_freq.items():
        df = doc_freq.get(term, 1)
        if df < min_count:
            continue
            
        # IDF calculation with smoothing
        idf = math.log((num_docs + 1) / (df + 1)) + 1.0
        # TF scaled by frequency
        tf = math.sqrt(count)
        tfidf = tf * idf
        
        # Average sentiment of reviews mentioning this term
        compounds = term_sentiment_scores.get(term, [0.0])
        avg_sentiment = sum(compounds) / len(compounds) if compounds else 0.0
        
        # Labeling sentiment orientation
        if avg_sentiment >= 0.15:
            orientation = "positive"
        elif avg_sentiment <= -0.15:
            orientation = "negative"
        else:
            orientation = "neutral"

        scored_terms.append({
            "keyword": term,
            "frequency": count,
            "doc_count": df,
            "tfidf_score": round(tfidf, 2),
            "avg_sentiment": round(avg_sentiment, 3),
            "orientation": orientation,
            "is_phrase": " " in term
        })

    # Sort by a balanced composite of TF-IDF and frequency
    scored_terms.sort(key=lambda x: (x["tfidf_score"] * 0.7 + x["frequency"] * 0.3), reverse=True)
    
    # Return top N keywords/phrases
    return scored_terms[:top_n]
