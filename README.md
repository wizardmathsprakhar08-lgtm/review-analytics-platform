# SentimentPulse: Multi-Category Review Analytics Platform

> **College Final Year Capstone Project**  
> A full-stack Natural Language Processing (NLP) web platform that ingests, scores, analyzes, and visualizes customer feedback across multiple commercial verticals: **Products**, **Restaurants**, **Movies**, and **Mobile Apps**.

---

## 1. System Architecture

```
+-----------------------------------------------------------------------------------+
|                        Frontend Web Dashboard (SPA)                               |
|   TailwindCSS + Chart.js 4 + Lucide Icons + Real-Time Live NLP Gauge              |
+-----------------------------------------------------------------------------------+
                                         |
                                         | REST APIs (JSON)
                                         v
+-----------------------------------------------------------------------------------+
|                           FastAPI Backend (Python)                                |
|   +-----------------------+   +----------------------+   +--------------------+   |
|   |      API Layer        |   |      NLP Engine      |   |   Data Access DAL  |   |
|   | - /api/categories     |   | - VADER Sentiment    |   | - SQLite Driver    |   |
|   | - /api/reviews        |   | - TF-IDF Extraction  |   | - Relational ORM   |   |
|   | - /api/analytics/*    |   | - Real-time Preview  |   | - Auto-Seeder      |   |
|   +-----------------------+   +----------------------+   +--------------------+   |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                         SQLite Relational Database                                |
|   - users (id, username, email, avatar_url, created_at)                           |
|   - categories (id, name, slug, description, icon)                                |
|   - reviews (id, category_id, user_id, item_name, title, text, rating, date)      |
|   - sentiment_scores (id, review_id, sentiment_label, compound, pos, neu, neg)    |
+-----------------------------------------------------------------------------------+
```

---

## 2. Key Features

1. **Multi-Vertical Segmentation**:
   - Distinct categorization for **Products**, **Restaurants**, **Movies**, and **Mobile Apps**.
   - Comes pre-seeded with **~250 authentic, high-fidelity reviews** with realistic ratings, author personas, and timestamps.

2. **Real-time VADER NLP Sentiment Classification**:
   - Calculates **Compound score** (normalized between $-1.0$ and $+1.0$), along with **Positive**, **Neutral**, and **Negative** sub-ratios.
   - Classification Thresholds:
     - **Positive**: $\text{Compound} \ge +0.05$
     - **Neutral**: $-0.05 < \text{Compound} < +0.05$
     - **Negative**: $\text{Compound} \le -0.05$

3. **TF-IDF & N-gram Topic/Keyword Extractor**:
   - Automatically computes Term Frequency-Inverse Document Frequency (TF-IDF) scores across review corpuses.
   - Identifies high-frequency key phrases (e.g., *"battery life"*, *"noise cancellation"*, *"sync crashes"*).
   - Dynamically correlates each topic with positive or negative sentiment orientation.

4. **Live NLP Sentiment Preview Gauge**:
   - While drafting a new review in the UI modal, an interactive NLP gauge analyzes the text in real-time on every keystroke, revealing compound score and detected lexicon cues before publishing.

5. **Executive Cross-Category Benchmarking (Admin View)**:
   - Aggregate comparative analytics comparing Sentiment Compound vs. Star Ratings across all four industries.
   - Stacked sentiment volume breakdown and vertical performance scorecard.

6. **Filterable Review Explorer**:
   - Search across review titles, text, and item names.
   - Filter by sentiment label (Positive / Neutral / Negative) and star rating (1–5).
   - Interactive topic chips: clicking any keyword immediately filters matching reviews.

---

## 3. Database Schema

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    avatar_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    slug TEXT NOT NULL UNIQUE,
    description TEXT,
    icon TEXT
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    item_name TEXT NOT NULL,
    title TEXT NOT NULL,
    text TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    helpful_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sentiment_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    review_id INTEGER NOT NULL UNIQUE REFERENCES reviews(id) ON DELETE CASCADE,
    sentiment_label TEXT NOT NULL CHECK (sentiment_label IN ('positive', 'neutral', 'negative')),
    compound_score REAL NOT NULL,
    pos_score REAL NOT NULL,
    neu_score REAL NOT NULL,
    neg_score REAL NOT NULL,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 4. Setup and Quickstart Instructions

### Prerequisites
- Python 3.10+ (tested and verified on Python 3.14)
- Web browser (Chrome, Edge, Firefox, Safari)

### Installation

1. Navigate to the project directory:
   ```powershell
   cd C:\Users\prakhar\.gemini\antigravity\scratch\review-analytics-platform
   ```

2. Install dependencies:
   ```powershell
   py -m pip install -r requirements.txt
   ```

### Running the Application

Run the all-in-one launcher script:
```powershell
py run.py
```

`run.py` automatically:
- Initializes the SQLite database.
- Checks if seed data is present (if empty, automatically seeds ~250 reviews).
- Launches the FastAPI backend server on `http://127.0.0.1:8000`.
- Automatically opens the web dashboard in your default browser.

### Accessing the System
- **Web Dashboard**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc API Reference**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 5. REST API Documentation

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/categories` | Returns all 4 categories with total reviews, average ratings, and sentiment averages. |
| `GET` | `/api/reviews` | Searchable & filterable reviews by category, sentiment, star rating, and sort order. |
| `POST` | `/api/reviews` | Submits a new review, runs VADER NLP analysis, and stores the record. |
| `GET` | `/api/analytics/category/{slug}` | Returns summary KPIs, sentiment distribution %, trend line data, and rating breakdown. |
| `GET` | `/api/analytics/topics/{slug}` | Returns TF-IDF extracted top keywords and informative bigrams for a vertical. |
| `GET` | `/api/analytics/cross-category` | Returns executive aggregate metrics and comparative benchmarks across verticals. |
| `POST` | `/api/nlp/analyze` | Real-time sentiment analysis preview endpoint for live text input. |
| `POST` | `/api/reset-data` | Resets SQLite database and repopulates with authentic dataset. |

---

## 6. College Viva / Evaluation Q&A Guide

### Q1: What is VADER and why was it chosen over transformer models (like BERT/RoBERTa)?
**Answer**: VADER (*Valence Aware Dictionary for sEntiment Reasoning*) is a specialized rule- and lexicon-based sentiment analysis model tuned specifically for micro-reviews, customer feedback, and social media text.  
- **Advantages**: It requires zero heavy GPU hardware, exhibits millisecond execution latency (enabling our **Live NLP Preview** as the user types), handles punctuation (e.g. `!`), capitalization (e.g. `GREAT`), negations (`"not good"`), and contrastive conjunctions (`"good battery but bad screen"`).

### Q2: How does the Compound Score work mathematically?
**Answer**: The compound score is computed by summing the valence scores of each word in the lexicon, adjusted according to rules (punctuations, amplifiers), and then normalized between $-1$ (most negative) and $+1$ (most positive) using the formula:
$$\text{Compound} = \frac{x}{\sqrt{x^2 + \alpha}}$$
where $x$ is the sum of valence scores and $\alpha \approx 15$ is a normalization parameter.

### Q3: How are topics and keywords extracted?
**Answer**: We employ TF-IDF (Term Frequency - Inverse Document Frequency) coupled with N-gram tokenization:
- High-frequency stop words and domain noise words are filtered out.
- Unigrams and informative bigrams are extracted.
- $\text{TF}(t, d) = \frac{\text{count}(t, d)}{\text{total words in } d}$
- $\text{IDF}(t) = \ln\left(1 + \frac{N}{1 + \text{doc\_freq}(t)}\right) + 1$
- The resulting TF-IDF weights surface distinct vertical topics (e.g. *"noise cancellation"* in Products, *"tonkotsu broth"* in Restaurants, *"cinematography"* in Movies).

### Q4: How is database integrity handled?
**Answer**: SQLite enforces strict foreign key constraints with `ON DELETE CASCADE`. The `reviews` table links to `categories` and `users`, and `sentiment_scores` maintains a 1-to-1 relationship with `reviews` through a unique foreign key index.
