"""
Dremio Visualization Example
Usage: python dremio-skill/examples/python/visualize_data.py

Prerequisites:
  pip install dremio-simple-query pandas matplotlib python-dotenv

Description:
  This script demonstrates how to:
  1. Connect to Dremio using environment variables.
  2. Execute an aggregation query to fetch a Pandas DataFrame.
  3. Create a bar chart using Matplotlib.
  4. Save the visualization to a file.
"""

import os
import sys
import matplotlib.pyplot as plt
from dremioframe.client import DremioClient
from dotenv import load_dotenv

def main():
    # 1. Load Environment Variables
    load_dotenv()
    
    endpoint = os.getenv("DREMIO_ENDPOINT") or os.getenv("DREMIO_SOFTWARE_HOST")
    token = os.getenv("DREMIO_PAT") or os.getenv("DREMIO_SOFTWARE_PAT")
    
    if not endpoint or not token:
        print("Error: Missing DREMIO_ENDPOINT or DREMIO_PAT environment variables.")
        print("Please configure your .env file.")
        sys.exit(1)

    # 2. Initialize Client
    print(f"Connecting to Dremio at {endpoint}...")
    try:
        client = DremioClient(endpoint=endpoint, token=token)
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    # 3. Define Query
    # Aggregating trip count by pickup district (top 10)
    # Using the standard samples dataset
    sql = """
    SELECT 
        pickup_district, 
        COUNT(*) as trip_count 
    FROM Samples."samples.dremio.com"."NYC-taxi-trips" 
    WHERE pickup_district IS NOT NULL
    GROUP BY pickup_district 
    ORDER BY trip_count DESC 
    LIMIT 10
    """
    
    print("\nExecuting query...")
    print(f"SQL: {sql}")

    try:
        # 4. Fetch Data
        df = client.query_to_pandas(sql)
        
        if df.empty:
            print("No data returned from query.")
            return

        print(f"Successfully retrieved {len(df)} rows.")
        print(df)

        # 5. Visualize Data
        print("\nGeneratng visualization...")
        
        plt.figure(figsize=(10, 6))
        # Simple bar chart
        bars = plt.bar(df['pickup_district'], df['trip_count'], color='#4B9CD3') # Dremio Blue-ish
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                     f'{int(height):,}',
                     ha='center', va='bottom')

        plt.xlabel('Pickup District')
        plt.ylabel('Trip Count')
        plt.title('Top 10 High-Traffic Pickup Locations (NYC Taxi)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # 6. Save Artifact
        output_file = "dremio_visualization_example.png"
        plt.savefig(output_file)
        print(f"✅ Visualization saved to: {os.path.abspath(output_file)}")
        
    except Exception as e:
        print(f"An error occurred during query or visualization: {e}")

if __name__ == "__main__":
    main()
