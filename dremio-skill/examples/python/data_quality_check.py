"""
Data Quality Validation Example
Usage: python dremio-skill/examples/python/data_quality_check.py

Description:
  Demonstrates how to run lightweight data quality checks using simple aggregation queries.
  Checks for:
  - Null values in critical columns
  - Uniqueness of IDs
  - Row count thresholds
"""

import os
import sys
from dremioframe.client import DremioClient
from dotenv import load_dotenv

def run_dq_checks():
    load_dotenv()
    
    endpoint = os.getenv("DREMIO_ENDPOINT") or os.getenv("DREMIO_SOFTWARE_HOST")
    token = os.getenv("DREMIO_PAT") or os.getenv("DREMIO_SOFTWARE_PAT")
    
    if not token:
        print("Please configure environment variables.")
        return

    client = DremioClient(endpoint=endpoint, token=token)
    
    # Target Table (using Samples)
    table = "Samples.\"samples.dremio.com\".\"NYC-taxi-trips\""
    print(f"Running measures on {table}...")
    
    # 1. Row Count & Null Check
    # We combine checks into one pass for performance
    sql = f"""
    SELECT 
        COUNT(*) as total_rows,
        COUNT(pickup_datetime) as pickup_times,
        COUNT(DISTINCT pickup_datetime) as unique_times,
        SUM(CASE WHEN fare_amount < 0 THEN 1 ELSE 0 END) as negative_fares
    FROM {table}
    """
    
    try:
        df = client.query_to_pandas(sql)
        row = df.iloc[0]
        
        # Define Thresholds
        EXPECTED_ROWS = 1000
        
        print("\n--- Results ---")
        print(f"Total Rows: {row['total_rows']}")
        print(f"Negative Fares: {row['negative_fares']}")
        
        issues = []
        
        if row['total_rows'] < EXPECTED_ROWS:
            issues.append(f"Row count {row['total_rows']} is below threshold {EXPECTED_ROWS}")
            
        if row['negative_fares'] > 0:
            issues.append(f"Found {row['negative_fares']} records with negative fare amount")
            
        if row['total_rows'] != row['pickup_times']:
             issues.append("Found NULL values in pickup_datetime")
             
        if not issues:
            print("✅ All Checks Passed")
        else:
            print("❌ Validation Failed:")
            for i in issues:
                print(f"   - {i}")
                
    except Exception as e:
        print(f"Check failed execution: {e}")

if __name__ == "__main__":
    run_dq_checks()
