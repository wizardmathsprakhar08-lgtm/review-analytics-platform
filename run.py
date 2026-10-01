"""
SentimentPulse - One-Click Application Launcher
Runs database migrations/seed, starts FastAPI backend & frontend server, and launches browser.
"""

import sys
import os
import time
import webbrowser
import threading

# Add root and backend to python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, "backend"))

def check_and_seed_db():
    print("================================================================")
    print("  SENTIMENTPULSE - MULTI-CATEGORY REVIEW ANALYTICS PLATFORM")
    print("================================================================")
    try:
        from backend.database import init_db, count_reviews
        from backend.seed import run_seed
        
        init_db()
        count = count_reviews()
        if count == 0:
            print("[INFO] Database is empty. Seeding initial ~240 authentic reviews...")
            seeded = run_seed()
            print(f"[SUCCESS] Seeded {seeded} reviews across all categories.")
        else:
            print(f"[INFO] SQLite database active with {count} reviews.")
    except Exception as e:
        print(f"[ERROR] Database verification failed: {e}")

def open_browser():
    """Wait for server to bind and open default browser."""
    time.sleep(1.8)
    url = "http://127.0.0.1:8000"
    print(f"\n[INFO] Launching dashboard at: {url}")
    try:
        webbrowser.open(url)
    except Exception:
        pass

def main():
    check_and_seed_db()
    
    port = int(os.environ.get("PORT", 8000))
    is_cloud = "PORT" in os.environ

    if not is_cloud:
        # Spawn browser open thread only when running locally on desktop
        threading.Thread(target=open_browser, daemon=True).start()
    
    print("\n[INFO] Starting Uvicorn ASGI Server...")
    print(f"  - Web Dashboard:     http://localhost:{port}  (or http://127.0.0.1:{port})")
    print(f"  - Interactive Docs:  http://localhost:{port}/docs")
    print(f"  - ReDoc Reference:   http://localhost:{port}/redoc")
    print(f"  - OpenAPI Schema:    http://localhost:{port}/openapi.json")
    print("\nPress Ctrl+C to stop the server.\n")

    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=False, log_level="info")

if __name__ == "__main__":
    main()
