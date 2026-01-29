"""
DremioFrame Basics Example
Usage: python dremio-skill/examples/python/dremioframe_basics.py

Description:
  Demonstrates the core DataFrame API for querying data.
  - Connecting to Dremio
  - Selecting tables
  - Filtering, Selecting columns, Limiting
  - Collecting results to Pandas
"""

import os
import sys
from dremioframe.client import DremioClient
from dotenv import load_dotenv

def run_basics():
    load_dotenv()
    
    endpoint = os.getenv("DREMIO_ENDPOINT") or os.getenv("DREMIO_SOFTWARE_HOST")
    token = os.getenv("DREMIO_PAT") or os.getenv("DREMIO_SOFTWARE_PAT")
    
    if not token:
        print("Please configure .env environment variables.")
        return

    # 1. Initialize Client
    client = DremioClient(endpoint=endpoint, token=token)
    
    # 2. Get a Builder for a Table
    # Replace with a valid table in your Dremio instance
    table_name = "Samples.\"samples.dremio.com\".\"NYC-taxi-trips\""
    print(f"Querying {table_name}...")
    
    builder = client.table(table_name)
    
    # 3. Build the Query (Lazy Evaluation)
    # This does NOT execute until .collect() is called
    query = (
        builder
        .select("pickup_datetime", "fare_amount", "trip_distance_mi")
        .filter("fare_amount > 10")
        .filter("trip_distance_mi > 5")
        .limit(10)
    )
    
    # 4. Explain the Query (Optional)
    # See the SQL that will be generated
    print("\n--- Generated SQL ---")
    print(query.explain())
    
    # 5. Execute and Collect Results
    print("\n--- Results ---")
    df = query.collect()
    print(df)

if __name__ == "__main__":
    run_basics()
