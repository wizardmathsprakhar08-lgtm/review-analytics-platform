"""
Automated Render Cloud Deployment Script
Uses Render REST API v1 to create and deploy the web service automatically.
"""

import urllib.request
import json
import sys
import os

RENDER_API_BASE = "https://api.render.com/v1"
REPO_URL = "https://github.com/wizardmathsprakhar08-lgtm/review-analytics-platform"

def deploy(api_key: str):
    headers = {
        "Authorization": f"Bearer {api_key.strip()}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    print("[1/3] Validating Render API Key & fetching user account details...")
    try:
        req = urllib.request.Request(f"{RENDER_API_BASE}/owners", headers=headers)
        with urllib.request.urlopen(req) as res:
            owners = json.loads(res.read().decode())
    except urllib.error.HTTPError as e:
        print(f"[ERROR] Authentication failed ({e.code}): {e.read().decode()}")
        return None
    except Exception as e:
        print(f"[ERROR] Failed to reach Render API: {e}")
        return None

    if not owners:
        print("[ERROR] No owners/workspaces found for this Render account.")
        return None

    owner_id = owners[0]["owner"]["id"]
    owner_name = owners[0]["owner"]["name"]
    print(f"[OK] Authenticated as '{owner_name}' (ID: {owner_id})")

    # Check if service already exists
    print("[2/3] Checking existing services...")
    req = urllib.request.Request(f"{RENDER_API_BASE}/services?limit=20", headers=headers)
    with urllib.request.urlopen(req) as res:
        services_data = json.loads(res.read().decode())

    existing_service = None
    for item in services_data:
        srv = item.get("service", {})
        if srv.get("name") == "sentiment-pulse-platform":
            existing_service = srv
            break

    if existing_service:
        service_id = existing_service["id"]
        service_url = existing_service.get("serviceDetails", {}).get("url")
        print(f"[INFO] Service 'sentiment-pulse-platform' already exists (ID: {service_id})")
        print("[3/3] Triggering a fresh deployment...")
        deploy_req = urllib.request.Request(
            f"{RENDER_API_BASE}/services/{service_id}/deploys",
            data=json.dumps({"clearCache": "do_not_clear"}).encode(),
            headers=headers,
            method="POST"
        )
        with urllib.request.urlopen(deploy_req) as d_res:
            d_data = json.loads(d_res.read().decode())
            print(f"[SUCCESS] Deployment triggered! Deploy ID: {d_data.get('id')}")
        print(f"\n=======================================================")
        print(f"  YOUR 24/7 PERMANENT CLOUD URL: {service_url}")
        print(f"=======================================================\n")
        return service_url

    # Create new Web Service
    print("[3/3] Creating and provisioning new Web Service on Render...")
    payload = {
        "type": "web_service",
        "name": "sentiment-pulse-platform",
        "ownerId": owner_id,
        "repo": REPO_URL,
        "branch": "main",
        "autoDeploy": "yes",
        "serviceDetails": {
            "env": "python",
            "plan": "free",
            "buildCommand": "pip install -r requirements.txt",
            "startCommand": "python run.py",
            "region": "oregon",
            "envVars": [
                {"key": "PYTHON_VERSION", "value": "3.11.8"}
            ]
        }
    }

    create_req = urllib.request.Request(
        f"{RENDER_API_BASE}/services",
        data=json.dumps(payload).encode(),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(create_req) as c_res:
            c_data = json.loads(c_res.read().decode())
            srv_info = c_data.get("service", c_data)
            service_url = srv_info.get("serviceDetails", {}).get("url")
            print(f"[SUCCESS] Service created successfully!")
            print(f"\n=======================================================")
            print(f"  YOUR 24/7 PERMANENT CLOUD URL: {service_url}")
            print(f"=======================================================\n")
            return service_url
    except urllib.error.HTTPError as e:
        print(f"[ERROR] Service creation failed ({e.code}): {e.read().decode()}")
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        api_key = os.environ.get("RENDER_API_KEY", "")

    if not api_key:
        print("Usage: python deploy_render.py <RENDER_API_KEY>")
        print("Or set RENDER_API_KEY environment variable.")
        sys.exit(1)

    deploy(api_key)
