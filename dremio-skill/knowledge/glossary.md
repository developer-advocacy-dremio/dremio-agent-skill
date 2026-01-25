# Dremio Terminology & Glossary

This glossary defines key Dremio concepts to ensure accurate terminology in code and explanations.

## Core Concepts

### Dataset Types
-   **PDS (Physical Dataset)**: A direct representation of data in a source (table, file, folder).
    -   *Icon*: Purple table icon.
    -   *Promotion*: Files/Folders must be "promoted" to PDS to be queryable (format settings apply).
-   **VDS (Virtual Dataset)**: A logical view defined by SQL.
    -   *Icon*: Green table icon.
    -   *Usage*: The primary building block for the semantic layer. VDS can query PDS or other VDS.

### Organization
-   **Space**: A top-level container for VDS and folders (e.g., "Marketing", "Finance").
-   **Source**: A connection to an external system (S3, Postgres, Snowflake).
-   **Home Space**: A private space for each user (`@username`).

### Acceleration & Performance
-   **Reflection**: An optimized materialization of data (like an index or materialized view) managed by Dremio.
    -   **Raw Reflection**: Accelerates queries requiring detailed row data (filtering, sorting).
    -   **Aggregation Reflection**: Accelerates BI-style group-by and aggregation queries.
    -   **Invisible**: Users query the logical VDS; the optimizer automatically substitutes the reflection.

### Architecture
-   **Coordinator**: The "brain" node that plans queries and manages metadata.
-   **Executor**: The "muscle" node that processes data.

## Data Lakehouse Terms
-   **Iceberg**: The open table format Dremio uses natively for data lake tables.
-   **Time Travel**: Querying data as it existed at a past point in time (`AT SNAPSHOT`, `AT TIMESTAMP`).
-   **Catalog**: The entity holding the metadata (tables, views, branches).
