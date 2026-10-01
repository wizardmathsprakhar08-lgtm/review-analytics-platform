import urllib.request
import json
import time
import subprocess
import sys
import os

print("Starting FastAPI test runner...")
proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"],
    cwd=os.path.dirname(os.path.abspath(__file__))
)

try:
    time.sleep(3)
    
    # 1. Test Categories
    res = urllib.request.urlopen("http://127.0.0.1:8000/api/categories")
    cats = json.loads(res.read().decode())
    print("\n[OK] Categories count:", len(cats["categories"]))
    for c in cats["categories"]:
        print(f"   * {c['name']} (slug: {c['slug']}): {c['review_count']} reviews, avg sentiment: {c['avg_sentiment']}")

    # 2. Test Category Analytics
    res = urllib.request.urlopen("http://127.0.0.1:8000/api/analytics/category/products")
    prod_analytics = json.loads(res.read().decode())
    print("\n[OK] Products Analytics Summary:", prod_analytics["summary"])
    print(f"   * Sentiment Distribution: {prod_analytics['sentiment_distribution']['counts']}")
    print(f"   * Top Topics count: {len(prod_analytics.get('topics', []))}")
    if prod_analytics.get("topics"):
        print("   * Sample Topics:", [t["keyword"] for t in prod_analytics["topics"][:5]])

    # 3. Test Cross Category
    res = urllib.request.urlopen("http://127.0.0.1:8000/api/analytics/cross-category")
    cross = json.loads(res.read().decode())
    print("\n[OK] Cross-Category Analytics:")
    print(f"   * Total platform reviews: {cross['overall']['total_reviews']}")
    print(f"   * Platform avg sentiment: {cross['overall']['platform_avg_sentiment']}")
    print(f"   * Categories in benchmark: {len(cross['categories'])}")

    # 4. Test Live NLP endpoint
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/nlp/analyze", 
        data=json.dumps({"text": "This is an exceptional product with brilliant build quality and great battery life!"}).encode(),
        headers={"Content-Type": "application/json"}
    )
    res = urllib.request.urlopen(req)
    nlp_res = json.loads(res.read().decode())
    print("\n[OK] Live NLP Analysis:")
    print(f"   * Compound Score: {nlp_res['compound']}")
    print(f"   * Classification: {nlp_res['label']}")
    print(f"   * Cues Detected: {nlp_res['sentiment_cues']}")

    # 5. Test Submit Review
    new_rev = {
        "category_slug": "products",
        "item_name": "Test Wireless Headphones",
        "title": "Stunning audio immersion",
        "text": "The active noise cancellation blocks everything out, extremely comfortable for long flights.",
        "rating": 5,
        "username": "Prof. Evaluation Demo"
    }
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/reviews",
        data=json.dumps(new_rev).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    res = urllib.request.urlopen(req)
    created = json.loads(res.read().decode())
    print("\n[OK] Submit Review Response:")
    print(f"   * Review ID: {created['review_id']}")
    print(f"   * Auto-classified Sentiment: {created['sentiment']['label']} (compound: {created['sentiment']['compound']})")

    # 6. Test Helpful Upvote
    req = urllib.request.Request("http://127.0.0.1:8000/api/reviews/1/helpful", method="POST")
    res = urllib.request.urlopen(req)
    upvote_res = json.loads(res.read().decode())
    print("\n[OK] Upvote Endpoint:", upvote_res)

    # 7. Test Export CSV & JSON
    res_csv = urllib.request.urlopen("http://127.0.0.1:8000/api/export?format=csv")
    csv_text = res_csv.read().decode()
    print(f"\n[OK] Export CSV: {len(csv_text.splitlines())} lines generated")

    res_json = urllib.request.urlopen("http://127.0.0.1:8000/api/export?format=json")
    json_export = json.loads(res_json.read().decode())
    print(f"\n[OK] Export JSON: {json_export['total']} reviews exported")

    # 8. Test Frontend HTML Root
    res = urllib.request.urlopen("http://127.0.0.1:8000/")
    html = res.read().decode()
    print(f"\n[OK] Frontend Root HTML status: {res.status}, Length: {len(html)} chars")
    assert "<title>SentimentPulse" in html, "Title check failed"
    assert "speedometerNeedle" in html, "Speedometer SVG check failed"
    assert "wordCloudContainer" in html, "Word cloud container check failed"
    print("\n>>> ALL BACKEND, NLP, DATABASE & FRONTEND TESTS PASSED 100%! <<<\n")

finally:
    proc.terminate()
    proc.wait()
