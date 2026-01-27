"""
Self-Correction Script for Dremio Skill
Usage: python dremio-skill/scripts/validate_conn.py

This script diagnoses connection issues by checking environment variables
and attempting a basic API call to Dremio.
"""

import os
import sys
import requests
from dotenv import load_dotenv

def validate_connection():
    load_dotenv()
    
    print("--- Dremio Skill: Connection Diagnostic Tool ---")

    # 1. Check for Critical Env Vars
    endpoint = os.getenv("DREMIO_ENDPOINT") or os.getenv("DREMIO_SOFTWARE_HOST")
    pat = os.getenv("DREMIO_PAT") or os.getenv("DREMIO_SOFTWARE_PAT")
    user = os.getenv("DREMIO_SOFTWARE_USER")
    password = os.getenv("DREMIO_SOFTWARE_PASSWORD")
    project_id = os.getenv("DREMIO_PROJECT_ID")

    missing = []
    
    if not endpoint:
        missing.append("DREMIO_ENDPOINT (or DREMIO_SOFTWARE_HOST)")
    
    if not pat and not (user and password):
        missing.append("DREMIO_PAT (or DREMIO_SOFTWARE_PAT or USER/PASS)")

    if missing:
        print("❌ CRITICAL: Missing Environment Variables")
        for m in missing:
            print(f"   - {m}")
        print("\nPlease check your .env file or reference 'template.env'.")
        sys.exit(1)

    print("✅ Environment Variables Present")
    print(f"   Endpoint: {endpoint}")
    print(f"   Auth Method: {'PAT' if pat else 'User/Pass'}")
    if project_id:
        print(f"   Project ID: {project_id}")

    # 2. Test Connectivity (Basic Ping/Header check)
    print("\nAttempting to connect...")
    
    headers = {}
    if pat:
        headers["Authorization"] = f"Bearer {pat}"
    else:
        # If user/pass, we would need to login first, simplified check here
        # Assuming PAT for modern usage recommendation
        print("⚠️  Detailed API check for User/Password not implemented in quick check.")
        print("   (Ensure your username/password are correct)")
        return

    # Normalize endpoint (remove trailing slash)
    base_url = endpoint.rstrip("/")
    
    # Try a lightweight endpoint. 
    # For Cloud: /v0/projects
    # For Software: /api/v3/catalog 
    # Use a generic strategy or try one then fallback
    
    try:
        # Try Cloud-style header check first (or software if clearly configured)
        if "dremio.cloud" in base_url:
             api_url = f"{base_url}/v0/projects"
        else:
             api_url = f"{base_url}/api/v3/catalog"

        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Connection Successful! API responded with 200 OK.")
            
            # 3. Deep Check: Validate 'Samples' Source
            print("\nChecking for 'Samples' source...")
            try:
                # Dremio Cloud uses catalog/ vs project/ structure, but standard catalog endpoint works usually
                # We'll try to list sources.
                catalog_url = f"{base_url}/api/v3/catalog"
                cat_resp = requests.get(catalog_url, headers=headers, timeout=10)
                if cat_resp.status_code == 200:
                    data = cat_resp.json().get("data", [])
                    samples_found = any(item.get("path", []) == ["Samples"] for item in data)
                    if samples_found:
                        print("✅ 'Samples' source found.")
                    else:
                        print("⚠️  'Samples' source NOT found. Some examples may not work.")
                else:
                    print(f"⚠️  Could not list catalog (Status {cat_resp.status_code}). Skipping deep check.")
            except Exception as e:
                print(f"⚠️  Deep check failed: {e}")

        elif response.status_code == 401:
            print("❌ Authentication Failed (401). Check your PAT or Username/Password.")
        elif response.status_code == 403:
            print("❌ Access Denied (403). Your user may lack permissions.")
        elif response.status_code == 404:
            print(f"⚠️  Endpoint not found (404). Tried: {api_url}")
            print("   Check if your Base URL is correct.")
        else:
            print(f"❌ Connection Error: Status {response.status_code}")
            print(f"   Response: {response.text[:200]}")

    except Exception as e:
        print(f"❌ Network Error: {e}")
        print("   Check your internet connection and DNS settings.")

if __name__ == "__main__":
    validate_connection()
