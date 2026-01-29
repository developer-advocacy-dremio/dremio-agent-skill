"""
DremioFrame Iceberg Maintenance Example
Usage: python dremio-skill/examples/python/dremioframe_iceberg_maintenance.py

Description:
  Demonstrates Iceberg table maintenance and Time Travel.
  - Optimize (Compaction)
  - Vacuum (Expiration)
  - Time Travel Queries
"""

import os
from dremioframe.client import DremioClient
from dotenv import load_dotenv

def run_maintenance():
    load_dotenv()
    client = DremioClient(token=os.getenv("DREMIO_PAT"))
    
    # Use a writable Iceberg table
    table_name = "Spaces.scratch.dml_demo"
    
    print(f"Managing {table_name}...")
    
    try:
        # 1. Optimize (Compaction)
        # Merges small files into larger ones for performance
        print("Running Optimize...")
        client.table(table_name).optimize()
        print("Optimize complete.")
        
        # 2. Vacuum (Expire Snapshots)
        # Removes old snapshots to save space
        print("Running Vacuum...")
        client.table(table_name).vacuum(retain_days=7)
        print("Vacuum complete.")
        
        # 3. Time Travel
        # Get history to find a snapshot ID
        history = client.table(table_name).history()
        if not history.empty:
            snapshot_id = history.iloc[0]['snapshot_id']
            print(f"Querying Snapshot ID: {snapshot_id}")
            
            # Query at that point in time
            past_df = client.table(table_name).at(snapshot_id=snapshot_id).limit(5).collect()
            print(past_df)
            
            # Rollback (Careful!)
            # client.table(table_name).rollback(snapshot_id=snapshot_id)
            
    except Exception as e:
        print(f"Maintenance failed (Table might not exist): {e}")

if __name__ == "__main__":
    run_maintenance()
