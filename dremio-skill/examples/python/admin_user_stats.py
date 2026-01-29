"""
Admin User Stats Example
Usage: python dremio-skill/examples/python/admin_user_stats.py

Description:
  Demonstrates how to use Dremio's System Tables to analyze user activity.
  - Queries sys.jobs to count jobs per user.
  - Queries sys.reflections to list reflection status.
"""

import os
import sys
from dremioframe.client import DremioClient
from dotenv import load_dotenv

def run_stats():
    load_dotenv()
    
    endpoint = os.getenv("DREMIO_ENDPOINT") or os.getenv("DREMIO_SOFTWARE_HOST")
    token = os.getenv("DREMIO_PAT") or os.getenv("DREMIO_SOFTWARE_PAT")
    
    if not token:
        print("Configure .env first.")
        return

    client = DremioClient(endpoint=endpoint, token=token)
    
    # 1. User Activity (from Jobs History)
    # Note: access to sys.jobs requires admin privileges or monitor permissions
    print("Analyzing User Activity (Last 100 Jobs)...")
    
    sql_jobs = """
    SELECT 
        user_name,
        COUNT(*) as job_count,
        AVG(duration) as avg_duration_ms,
        SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) as failed_jobs
    FROM sys.jobs
    GROUP BY user_name
    ORDER BY job_count DESC
    LIMIT 20
    """
    
    try:
        df_jobs = client.query(sql_jobs)
        if not df_jobs.empty:
            print("\nUser Activity Summary:")
            print(df_jobs.to_markdown(index=False)) # Markdown table format
        else:
            print("No job history found.")
            
    except Exception as e:
        print(f"Could not query sys.jobs: {e}")

    # 2. Reflection Status
    print("\nChecking Reflection Health...")
    sql_reflections = """
    SELECT 
        status, 
        COUNT(*) as count 
    FROM sys.reflections 
    GROUP BY status
    """
    
    try:
        df_ref = client.query(sql_reflections)
        print(df_ref)
    except Exception as e:
        print(f"Could not query sys.reflections: {e}")

if __name__ == "__main__":
    run_stats()
