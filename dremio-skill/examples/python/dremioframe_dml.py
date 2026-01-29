"""
DremioFrame DML Example
Usage: python dremio-skill/examples/python/dremioframe_dml.py

Description:
  Demonstrates Data Manipulation Language (DML) operations.
  - CTAS (Create Table As Select)
  - Insert (from DataFrame)
  - Update / Delete  
  - SCD2 (Slowly Changing Dimensions)
"""

import os
import pandas as pd
from dremioframe.client import DremioClient
from dremioframe import F
from dotenv import load_dotenv

def run_dml():
    load_dotenv()
    client = DremioClient(token=os.getenv("DREMIO_PAT"))
    
    # Define a test space/folder (Must be an Iceberg source)
    target_space = "Spaces.scratch" 
    table_name = f"{target_space}.dml_demo"

    # 1. Create Table (CTAS)
    print(f"Creating {table_name}...")
    try:
        # Create from a query (e.g. from Samples)
        client.table("Samples.\"samples.dremio.com\".\"NYC-taxi-trips\"") \
            .limit(10) \
            .create(table_name)
        print("Table created.")
    except Exception as e:
        print(f"Creation failed (might exist): {e}")

    # 2. Insert Data (from Pandas)
    print("Inserting local data...")
    new_data = pd.DataFrame({
        "pickup_datetime": ["2023-01-01 12:00:00"],
        "fare_amount": [50.0],
        "trip_distance_mi": [10.5]
        # ... other columns would need to match schema or be handled by schema evolution
    })
    
    # Note: For production, ensure schema matches exactly
    try:
        client.table(table_name).insert(table_name, data=new_data)
        print("Insert successful.")
    except Exception as e:
        print(f"Insert failed: {e}")

    # 3. Update Data
    print("Updating high fares...")
    client.table(table_name).filter("fare_amount > 40").update({"tip_amount": 10.0})
    
    # 4. Delete Data
    print("Deleting short trips...")
    client.table(table_name).filter("trip_distance_mi < 0.5").delete()

    # 5. SCD2 (Type 2 History) Example
    # This assumes we have a staging table and a dimension table setup with valid_from/valid_to
    print("Running SCD2 logic (Mock)...")
    try:
        client.table(f"{target_space}.staging_users").scd2(
            target_table=f"{target_space}.dim_users",
            on=["user_id"],
            track_cols=["status", "email"],
            valid_from_col="valid_from",
            valid_to_col="valid_to"
        )
        print("SCD2 Complete")
    except Exception:
        print("Skipping SCD2 (Tables likely don't exist in demo environment)")

if __name__ == "__main__":
    run_dml()
