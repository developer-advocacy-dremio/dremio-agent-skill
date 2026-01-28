# Source Onboarding Wizard

Use this wizard when the user wants to add a new data source (S3, Postgres, Snowflake, Hive, etc.).

## 1. Context & Goal
Connect external data systems to Dremio so they can be queried and virtualized.

## 2. Discovery Phase (Ask the User)
1.  **Type**: "What type of source is it? (Object Storage, Relational DB, Metastore?)"
2.  **Auth**: "Do you have the credentials? (Access Key/Secret, Username/Password, Role ARN?)"
3.  **Privileges**: "Do you need it to be Read-Only or Read-Write?"
4.  **Network**: "Is the source accessible from the Dremio environment (VPC peering, allow-listing)?"

## 3. Implementation Patterns

### Object Storage (S3, ADLS, GCS)
-   **Required**: Bucket Name, Authentication (Access Keys or IAM Role).
-   **Metadata**: Dremio will discover folders. You need to "Format" files (Parquet, JSON, CSV) into PDS.

### Relational Database (Postgres, SQL Server, Oracle)
-   **Required**: Host, Port, Database Name, User/Pass.
-   **Metadata**: Dremio automatically maps schemas and tables to Folder/PDS structure.

### Table Formats (Iceberg, Delta Lake)
-   **Required**: Metastore URL (e.g. Glue, Nessie) or Warehouse Path (S3).
-   **Note**: Native Iceberg is a first-class citizen in Dremio.

## 4. Execution Steps (For the Agent)
1.  **Prepare Config**: Construct the config dictionary based on user input.
    *   *Tip*: Use `dremioframe` documentation or `generate_api_call` to find correct JSON payload structure for `POST /api/v3/catalog/source`.
2.  **Create Source**:
    ```python
    source_config = {"name": "my_s3", "type": "S3", "config": {...}}
    client.catalog.create_source(source_config)
    ```
3.  **Verify**: Run a simple `SELECT *` or `list_catalog` on the new source path.
