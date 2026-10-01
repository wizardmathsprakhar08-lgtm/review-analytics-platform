import sqlite3
import os
from contextlib import contextmanager
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reviews.db")

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            avatar_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            slug TEXT NOT NULL UNIQUE,
            description TEXT,
            icon TEXT
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
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
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sentiment_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            review_id INTEGER NOT NULL UNIQUE REFERENCES reviews(id) ON DELETE CASCADE,
            sentiment_label TEXT NOT NULL CHECK (sentiment_label IN ('positive', 'neutral', 'negative')),
            compound_score REAL NOT NULL,
            pos_score REAL NOT NULL,
            neu_score REAL NOT NULL,
            neg_score REAL NOT NULL,
            analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_reviews_cat ON reviews(category_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_reviews_created ON reviews(created_at);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sentiment_label ON sentiment_scores(sentiment_label);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sentiment_compound ON sentiment_scores(compound_score);")

def get_categories() -> List[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
        SELECT 
            c.*,
            COUNT(r.id) as review_count,
            ROUND(AVG(r.rating), 2) as avg_rating,
            ROUND(AVG(s.compound_score), 3) as avg_sentiment
        FROM categories c
        LEFT JOIN reviews r ON c.id = r.category_id
        LEFT JOIN sentiment_scores s ON r.id = s.review_id
        GROUP BY c.id
        ORDER BY c.id ASC;
        """
        return cursor.execute(query).fetchall()

def get_category_by_slug(slug: str) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM categories WHERE slug = ?;"
        return cursor.execute(query, (slug,)).fetchone()

def get_reviews(
    category_slug: Optional[str] = None,
    sentiment: Optional[str] = None,
    rating: Optional[int] = None,
    search: Optional[str] = None,
    sort_by: str = "newest",
    limit: int = 50,
    offset: int = 0
) -> Dict[str, Any]:
    with get_db() as conn:
        cursor = conn.cursor()
        
        where_clauses = []
        params = []
        
        if category_slug and category_slug != "all":
            where_clauses.append("c.slug = ?")
            params.append(category_slug)
            
        if sentiment and sentiment != "all":
            where_clauses.append("s.sentiment_label = ?")
            params.append(sentiment.lower())
            
        if rating and rating > 0:
            where_clauses.append("r.rating = ?")
            params.append(rating)
            
        if search:
            where_clauses.append("(r.title LIKE ? OR r.text LIKE ? OR r.item_name LIKE ?)")
            search_param = f"%{search}%"
            params.extend([search_param, search_param, search_param])
            
        where_str = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        # Sort options
        order_clause = "ORDER BY r.created_at DESC"
        if sort_by == "oldest":
            order_clause = "ORDER BY r.created_at ASC"
        elif sort_by == "rating_desc":
            order_clause = "ORDER BY r.rating DESC, r.created_at DESC"
        elif sort_by == "rating_asc":
            order_clause = "ORDER BY r.rating ASC, r.created_at DESC"
        elif sort_by == "sentiment_desc":
            order_clause = "ORDER BY s.compound_score DESC"
        elif sort_by == "sentiment_asc":
            order_clause = "ORDER BY s.compound_score ASC"
        elif sort_by == "helpful":
            order_clause = "ORDER BY r.helpful_count DESC"

        # Count total matches
        count_query = f"""
        SELECT COUNT(r.id) as total
        FROM reviews r
        JOIN categories c ON r.category_id = c.id
        LEFT JOIN sentiment_scores s ON r.id = s.review_id
        {where_str};
        """
        total = cursor.execute(count_query, params).fetchone()["total"]

        # Fetch reviews
        select_query = f"""
        SELECT 
            r.id,
            r.category_id,
            c.name as category_name,
            c.slug as category_slug,
            c.icon as category_icon,
            r.user_id,
            u.username,
            u.avatar_url,
            r.item_name,
            r.title,
            r.text,
            r.rating,
            r.helpful_count,
            r.created_at,
            s.sentiment_label,
            ROUND(s.compound_score, 3) as compound_score,
            ROUND(s.pos_score, 3) as pos_score,
            ROUND(s.neu_score, 3) as neu_score,
            ROUND(s.neg_score, 3) as neg_score
        FROM reviews r
        JOIN categories c ON r.category_id = c.id
        JOIN users u ON r.user_id = u.id
        LEFT JOIN sentiment_scores s ON r.id = s.review_id
        {where_str}
        {order_clause}
        LIMIT ? OFFSET ?;
        """
        
        fetch_params = params + [limit, offset]
        reviews = cursor.execute(select_query, fetch_params).fetchall()
        
        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "reviews": reviews
        }

def get_or_create_user(username: str, email: str, avatar_url: Optional[str] = None) -> int:
    with get_db() as conn:
        cursor = conn.cursor()
        user = cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?;", (username, email)).fetchone()
        if user:
            return user["id"]
        
        if not avatar_url:
            avatar_url = f"https://api.dicebear.com/7.x/bottts/svg?seed={username}"
            
        cursor.execute(
            "INSERT INTO users (username, email, avatar_url) VALUES (?, ?, ?);",
            (username, email, avatar_url)
        )
        return cursor.lastrowid

def insert_review(
    category_id: int,
    user_id: int,
    item_name: str,
    title: str,
    text: str,
    rating: int,
    helpful_count: int = 0,
    created_at: Optional[str] = None
) -> int:
    with get_db() as conn:
        cursor = conn.cursor()
        if created_at:
            cursor.execute(
                """
                INSERT INTO reviews (category_id, user_id, item_name, title, text, rating, helpful_count, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (category_id, user_id, item_name, title, text, rating, helpful_count, created_at)
            )
        else:
            cursor.execute(
                """
                INSERT INTO reviews (category_id, user_id, item_name, title, text, rating, helpful_count)
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """,
                (category_id, user_id, item_name, title, text, rating, helpful_count)
            )
        return cursor.lastrowid

def insert_sentiment_score(
    review_id: int,
    sentiment_label: str,
    compound_score: float,
    pos_score: float,
    neu_score: float,
    neg_score: float,
    analyzed_at: Optional[str] = None
):
    with get_db() as conn:
        cursor = conn.cursor()
        if analyzed_at:
            cursor.execute(
                """
                INSERT OR REPLACE INTO sentiment_scores 
                (review_id, sentiment_label, compound_score, pos_score, neu_score, neg_score, analyzed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """,
                (review_id, sentiment_label, compound_score, pos_score, neu_score, neg_score, analyzed_at)
            )
        else:
            cursor.execute(
                """
                INSERT OR REPLACE INTO sentiment_scores 
                (review_id, sentiment_label, compound_score, pos_score, neu_score, neg_score)
                VALUES (?, ?, ?, ?, ?, ?);
                """,
                (review_id, sentiment_label, compound_score, pos_score, neu_score, neg_score)
            )

def increment_helpful_count(review_id: int) -> int:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE reviews SET helpful_count = helpful_count + 1 WHERE id = ?;", (review_id,))
        res = cursor.execute("SELECT helpful_count FROM reviews WHERE id = ?;", (review_id,)).fetchone()
        return res["helpful_count"] if res else 0

def get_category_analytics(category_slug: str) -> Dict[str, Any]:
    with get_db() as conn:
        cursor = conn.cursor()
        
        cat_filter = ""
        params = []
        cat_info = None
        
        if category_slug != "all":
            cat_info = cursor.execute("SELECT * FROM categories WHERE slug = ?;", (category_slug,)).fetchone()
            if not cat_info:
                return {}
            cat_filter = "WHERE r.category_id = ?"
            params = [cat_info["id"]]

        # 1. Summary KPIs
        summary_query = f"""
        SELECT 
            COUNT(r.id) as total_reviews,
            ROUND(AVG(r.rating), 2) as avg_rating,
            ROUND(AVG(s.compound_score), 3) as avg_sentiment,
            ROUND(AVG(s.pos_score) * 100, 1) as avg_pos_pct,
            ROUND(AVG(s.neu_score) * 100, 1) as avg_neu_pct,
            ROUND(AVG(s.neg_score) * 100, 1) as avg_neg_pct
        FROM reviews r
        JOIN sentiment_scores s ON r.id = s.review_id
        {cat_filter};
        """
        summary = cursor.execute(summary_query, params).fetchone()

        # 2. Sentiment Breakdown (counts and percentages)
        sentiment_breakdown_query = f"""
        SELECT 
            s.sentiment_label,
            COUNT(s.id) as count
        FROM reviews r
        JOIN sentiment_scores s ON r.id = s.review_id
        {cat_filter}
        GROUP BY s.sentiment_label;
        """
        breakdown_rows = cursor.execute(sentiment_breakdown_query, params).fetchall()
        
        breakdown = {"positive": 0, "neutral": 0, "negative": 0}
        total_in_breakdown = sum(row["count"] for row in breakdown_rows)
        for row in breakdown_rows:
            breakdown[row["sentiment_label"]] = row["count"]
            
        breakdown_pct = {
            "positive": round((breakdown["positive"] / total_in_breakdown * 100), 1) if total_in_breakdown > 0 else 0,
            "neutral": round((breakdown["neutral"] / total_in_breakdown * 100), 1) if total_in_breakdown > 0 else 0,
            "negative": round((breakdown["negative"] / total_in_breakdown * 100), 1) if total_in_breakdown > 0 else 0
        }

        # 3. Rating distribution (1 to 5 stars)
        rating_query = f"""
        SELECT 
            r.rating,
            COUNT(r.id) as count
        FROM reviews r
        {cat_filter}
        GROUP BY r.rating
        ORDER BY r.rating ASC;
        """
        rating_rows = cursor.execute(rating_query, params).fetchall()
        ratings = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for row in rating_rows:
            ratings[row["rating"]] = row["count"]

        # 4. Sentiment Trend Over Time (grouped by week/month for smooth charts)
        trend_query = f"""
        SELECT 
            strftime('%Y-%m-%d', r.created_at) as date_label,
            COUNT(r.id) as volume,
            ROUND(AVG(s.compound_score), 3) as avg_sentiment,
            ROUND(AVG(r.rating), 2) as avg_rating
        FROM reviews r
        JOIN sentiment_scores s ON r.id = s.review_id
        {cat_filter}
        GROUP BY strftime('%Y-%W', r.created_at)
        ORDER BY r.created_at ASC;
        """
        trends = cursor.execute(trend_query, params).fetchall()

        return {
            "category": cat_info if cat_info else {"name": "All Categories", "slug": "all", "icon": "layers"},
            "summary": summary,
            "sentiment_distribution": {
                "counts": breakdown,
                "percentages": breakdown_pct
            },
            "rating_distribution": ratings,
            "trend": trends
        }

def get_cross_category_analytics() -> Dict[str, Any]:
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Comparison metrics across categories
        query = """
        SELECT 
            c.id,
            c.name,
            c.slug,
            c.icon,
            COUNT(r.id) as total_reviews,
            ROUND(AVG(r.rating), 2) as avg_rating,
            ROUND(AVG(s.compound_score), 3) as avg_sentiment,
            SUM(CASE WHEN s.sentiment_label = 'positive' THEN 1 ELSE 0 END) as positive_count,
            SUM(CASE WHEN s.sentiment_label = 'neutral' THEN 1 ELSE 0 END) as neutral_count,
            SUM(CASE WHEN s.sentiment_label = 'negative' THEN 1 ELSE 0 END) as negative_count,
            ROUND(100.0 * SUM(CASE WHEN s.sentiment_label = 'positive' THEN 1 ELSE 0 END) / NULLIF(COUNT(r.id), 0), 1) as positive_pct,
            ROUND(100.0 * SUM(CASE WHEN s.sentiment_label = 'negative' THEN 1 ELSE 0 END) / NULLIF(COUNT(r.id), 0), 1) as negative_pct
        FROM categories c
        LEFT JOIN reviews r ON c.id = r.category_id
        LEFT JOIN sentiment_scores s ON r.id = s.review_id
        GROUP BY c.id
        ORDER BY avg_sentiment DESC;
        """
        categories_data = cursor.execute(query).fetchall()

        # Overall platform metrics
        overall_query = """
        SELECT 
            COUNT(r.id) as total_reviews,
            ROUND(AVG(r.rating), 2) as platform_avg_rating,
            ROUND(AVG(s.compound_score), 3) as platform_avg_sentiment,
            COUNT(DISTINCT r.user_id) as total_users
        FROM reviews r
        JOIN sentiment_scores s ON r.id = s.review_id;
        """
        overall = cursor.execute(overall_query).fetchone()

        return {
            "overall": overall,
            "categories": categories_data
        }

def get_reviews_text_by_category(category_slug: Optional[str] = None) -> List[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        where_clause = ""
        params = []
        if category_slug and category_slug != "all":
            where_clause = "WHERE c.slug = ?"
            params = [category_slug]
            
        query = f"""
        SELECT 
            r.id,
            r.title,
            r.text,
            s.sentiment_label,
            s.compound_score
        FROM reviews r
        JOIN categories c ON r.category_id = c.id
        LEFT JOIN sentiment_scores s ON r.id = s.review_id
        {where_clause};
        """
        return cursor.execute(query, params).fetchall()

def count_reviews() -> int:
    with get_db() as conn:
        cursor = conn.cursor()
        res = cursor.execute("SELECT COUNT(*) as c FROM reviews;").fetchone()
        return res["c"] if res else 0
