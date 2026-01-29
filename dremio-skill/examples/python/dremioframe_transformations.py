"""
DremioFrame Transformations Example
Usage: python dremio-skill/examples/python/dremioframe_transformations.py

Description:
  Demonstrates advanced transformations using the DataFrame API.
  - Group By and Aggregations
  - Mutations (Calculated Columns)
  - Window Functions
"""

import os
from dremioframe.client import DremioClient
from dremioframe import F 
from dotenv import load_dotenv

def run_transformations():
    load_dotenv()
    token = os.getenv("DREMIO_PAT") or os.getenv("DREMIO_SOFTWARE_PAT")
    client = DremioClient(token=token)
    
    table_name = "Samples.\"samples.dremio.com\".\"NYC-taxi-trips\""
    builder = client.table(table_name)
    
    print("1. Aggregation Example")
    agg_df = (
        builder
        .group_by("passenger_count")
        .agg(
            avg_fare="AVG(fare_amount)",
            max_trip="MAX(trip_distance_mi)",
            total_trips="COUNT(*)"
        )
        .filter("total_trips > 100")
        .sort("passenger_count")
    )
    print(agg_df.collect())
    
    print("\n2. Mutation (Calculated Column) Example")
    # Mutate adds a new column based on an expression
    mutated_df = (
        client.table(table_name)
        .select("fare_amount", "tip_amount")
        .mutate(total_cost="fare_amount + tip_amount")
        .limit(5)
    )
    print(mutated_df.collect())

    print("\n3. Window Function Example")
    # Calculate rank of fare_amount within each passenger_count group
    window_spec = F.Window.partition_by("passenger_count").order_by(F.col("fare_amount").desc())
    
    window_df = (
        client.table(table_name)
        .select("passenger_count", "fare_amount")
        .select(
            F.rank().over(window_spec).alias("fare_rank")
        )
        .filter("fare_rank <= 3") # Top 3 fares per passenger count
        .limit(10)
    )
    print(window_df.collect())

if __name__ == "__main__":
    run_transformations()
