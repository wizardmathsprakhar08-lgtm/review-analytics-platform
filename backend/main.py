import os
import sys
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

# Ensure backend package imports correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import (
    init_db,
    get_categories,
    get_category_by_slug,
    get_reviews,
    get_or_create_user,
    insert_review,
    insert_sentiment_score,
    get_category_analytics,
    get_cross_category_analytics,
    get_reviews_text_by_category,
    count_reviews,
    increment_helpful_count
)
from nlp import analyze_sentiment, extract_topics_and_keywords
from seed import run_seed

app = FastAPI(
    title="Multi-Category Review Analytics Platform",
    description="Full-stack NLP platform for multi-vertical review sentiment analysis and topic extraction.",
    version="1.0.0"
)

# Enable CORS for local testing or external clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic schemas for request validation
class ReviewCreateRequest(BaseModel):
    category_slug: str = Field(..., description="Slug of the category: products, restaurants, movies, or mobile-apps")
    item_name: str = Field(..., min_length=2, max_length=150, description="Name of the product, restaurant, movie, or app")
    title: str = Field(..., min_length=2, max_length=200, description="Headline or title of review")
    text: str = Field(..., min_length=5, description="Full review body text")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5 stars")
    username: str = Field(default="Guest User", description="Reviewer name")
    email: Optional[str] = Field(default="guest@analytics.demo", description="Reviewer email")

class LiveAnalyzeRequest(BaseModel):
    text: str = Field(..., description="Text to analyze in real time")

# Startup event: Initialize DB and ensure seed data is present
@app.on_event("startup")
def on_startup():
    init_db()
    if count_reviews() == 0:
        print("Empty database detected at startup. Seeding initial reviews...")
        run_seed()

# ----------------- REST API Endpoints -----------------

@app.get("/api/categories", summary="List all categories with summary stats")
def list_categories():
    categories = get_categories()
    return {"categories": categories}

@app.get("/api/reviews", summary="Get filterable reviews with sentiment tags")
def list_reviews(
    category: Optional[str] = Query("all", description="Category slug: all, products, restaurants, movies, mobile-apps"),
    sentiment: Optional[str] = Query("all", description="Sentiment filter: all, positive, neutral, negative"),
    rating: Optional[int] = Query(0, description="Filter by exact rating (1-5, 0 for all)"),
    search: Optional[str] = Query(None, description="Search keyword in title, text, or item"),
    sort_by: str = Query("newest", description="Sort order: newest, oldest, rating_desc, rating_asc, sentiment_desc, sentiment_asc, helpful"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    result = get_reviews(
        category_slug=category,
        sentiment=sentiment,
        rating=rating,
        search=search,
        sort_by=sort_by,
        limit=limit,
        offset=offset
    )
    return result

@app.post("/api/reviews", status_code=status.HTTP_201_CREATED, summary="Submit a new review with automatic NLP scoring")
def create_review(payload: ReviewCreateRequest):
    cat = get_category_by_slug(payload.category_slug)
    if not cat:
        raise HTTPException(
            status_code=404,
            detail=f"Category '{payload.category_slug}' not found. Valid: products, restaurants, movies, mobile-apps"
        )
    
    # 1. Ensure user exists
    user_id = get_or_create_user(payload.username, payload.email or f"{payload.username.lower().replace(' ', '')}@demo.com")

    # 2. Insert Review record
    review_id = insert_review(
        category_id=cat["id"],
        user_id=user_id,
        item_name=payload.item_name.strip(),
        title=payload.title.strip(),
        text=payload.text.strip(),
        rating=payload.rating
    )

    # 3. Perform NLP Sentiment Analysis
    combined_text = f"{payload.title}. {payload.text}"
    sentiment_result = analyze_sentiment(combined_text)

    # 4. Save Sentiment Scores in relational table
    insert_sentiment_score(
        review_id=review_id,
        sentiment_label=sentiment_result["label"],
        compound_score=sentiment_result["compound"],
        pos_score=sentiment_result["pos"],
        neu_score=sentiment_result["neu"],
        neg_score=sentiment_result["neg"]
    )

    return {
        "message": "Review submitted and analyzed successfully.",
        "review_id": review_id,
        "category": cat["name"],
        "sentiment": sentiment_result
    }

@app.get("/api/analytics/category/{category_slug}", summary="Get category-specific analytics and sentiment distribution")
def get_category_stats(category_slug: str):
    stats = get_category_analytics(category_slug)
    if not stats:
        raise HTTPException(status_code=404, detail=f"Category '{category_slug}' not found.")
        
    # Extract topics/keywords for this category
    reviews_data = get_reviews_text_by_category(category_slug)
    topics = extract_topics_and_keywords(reviews_data, top_n=16)
    stats["topics"] = topics

    return stats

@app.get("/api/analytics/topics/{category_slug}", summary="Get top topics and keywords per category")
def get_category_topics(category_slug: str, top_n: int = 20):
    reviews_data = get_reviews_text_by_category(category_slug)
    topics = extract_topics_and_keywords(reviews_data, top_n=top_n)
    return {"category": category_slug, "topics": topics}

@app.get("/api/analytics/cross-category", summary="Admin executive aggregate analytics across all categories")
def get_cross_analytics():
    data = get_cross_category_analytics()
    return data

@app.post("/api/nlp/analyze", summary="Live sentiment preview endpoint for UI input")
def live_analyze(payload: LiveAnalyzeRequest):
    return analyze_sentiment(payload.text)

@app.post("/api/reviews/{review_id}/helpful", summary="Increment review helpfulness count")
def upvote_review(review_id: int):
    new_count = increment_helpful_count(review_id)
    return {"review_id": review_id, "helpful_count": new_count}

@app.get("/api/export", summary="Export reviews dataset as CSV or JSON")
def export_dataset(category: Optional[str] = "all", format: Optional[str] = "json"):
    data = get_reviews(category_slug=category, limit=500)
    reviews = data.get("reviews", [])

    if format.lower() == "csv":
        import io
        import csv
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "Category", "Item", "Title", "Text", "Rating", "Sentiment", "Compound", "Pos", "Neu", "Neg", "Date", "Helpful"])
        for r in reviews:
            writer.writerow([
                r["id"], r["category_name"], r["item_name"], r["title"], r["text"].replace("\n", " "),
                r["rating"], r["sentiment_label"], r["compound_score"], r["pos_score"], r["neu_score"], r["neg_score"],
                r["created_at"], r["helpful_count"]
            ])
        from fastapi.responses import Response
        return Response(
            content=output.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=sentiment_reviews_{category}.csv"}
        )

    return {"category": category, "total": len(reviews), "reviews": reviews}

@app.post("/api/reset-data", summary="Reset and re-seed database with authentic dataset")
def reset_seed():
    count = run_seed(force=True)
    return {"status": "success", "message": f"Database successfully reset and re-seeded with {count} reviews."}

# Mount Frontend static files
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    @app.get("/", include_in_schema=False)
    def serve_frontend_root():
        index_file = os.path.join(frontend_dir, "index.html")
        return FileResponse(index_file)
