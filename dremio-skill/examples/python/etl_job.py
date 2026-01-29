import os
import sys
from dremioframe.client import DremioClient
from dremioframe.admin import Admin
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_etl_job():
    # 1. Initialize Client
    try:
        # Checking for Dremio Cloud vs Software configuration
        endpoint = os.getenv("DREMIO_ENDPOINT") or os.getenv("DREMIO_SOFTWARE_HOST")
        token = os.getenv("DREMIO_PAT") or os.getenv("DREMIO_SOFTWARE_PAT")
        # For software legacy auth
        username = os.getenv("DREMIO_SOFTWARE_USER")
        password = os.getenv("DREMIO_SOFTWARE_PASSWORD")
        
        project_id = os.getenv("DREMIO_PROJECT_ID") # Optional/Cloud only

        if not endpoint:
            raise ValueError("DREMIO_ENDPOINT or DREMIO_SOFTWARE_HOST is not set.")

        print(f"Connecting to Dremio at {endpoint}...")
        
        # Initialize
        client = DremioClient(
            endpoint=endpoint, 
            token=token, 
            username=username, 
            password=password,
            project_id=project_id,
            tls=os.getenv("DREMIO_SOFTWARE_TLS", "false").lower() == "true"
        )
        print("Successfully connected.")

    except Exception as e:
        print(f"Failed to connect: {e}")
        sys.exit(1)

    # 2. Extract Data (Query)
    # Using a typical bronze/raw layer query
    source_table = "Samples.\"samples.dremio.com\".\"NYC-taxi-trips\""
    print(f"Extracting data from {source_table}...")
    
    # We can execute SQL directly to Create a View (Silver Layer)
    silver_view_path = "Spaces.Analytics.Silver.Taxi_Summary"
    
    # Define SQL transformation
    silver_sql = f"""
    SELECT 
        pickup_datetime,
        passenger_count,
        trip_distance_mi,
        fare_amount,
        tip_amount,
        total_amount
    FROM {source_table}
    WHERE fare_amount > 0
    """

    try:
        # Check if space exists, if not create logic would go here (omitted for brevity)
        # Create or Update View
        client.catalog.create_view(
            path=silver_view_path.split("."),
            sql=silver_sql
        )
        print(f"Created/Updated Silver View: {silver_view_path}")
    except Exception as e:
        # If it fails, it might exist, so we try update (or simple error handling)
        print(f"View creation note (might exist): {e}")

    # 3. Validation / Quality Check
    # Verify the view works
    try:
        df = client.query(f"SELECT COUNT(*) as cnt FROM {silver_view_path}")
        print(f"Verification successful. Row count: {df.iloc[0]['cnt']}")
    except Exception as e:
        print(f"Verification failed: {e}")

if __name__ == "__main__":
    run_etl_job()
