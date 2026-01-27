# Cache the result of a heavy query to a local Parquet file
cached_df = client.table("heavy_view").cache("local_cache_name", ttl_seconds=600)

