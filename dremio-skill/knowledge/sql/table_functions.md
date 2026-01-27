## Table Functions

Table functions in Dremio return a table as a result and can be used in the `FROM` clause of a query.

### sys.recommend_reflections

Returns a list of recommendations for Reflections that can be created to accelerate queries.

**Syntax:**
```sql
SELECT * FROM TABLE(sys.recommend_reflections())
```

**Columns:**

| Column | Data Type | Description |
| --- | --- | --- |
| query_id | VARCHAR | The job ID of the query that would benefit from the reflection. |
| dataset_id | VARCHAR | The ID of the dataset. |
| dataset_name | VARCHAR | The name of the dataset. |
| reflection_type | VARCHAR | The type of reflection (RAW or AGGREGATION). |
| display_columns | LIST | The list of display columns. |
| dimension_columns | LIST | The list of dimension columns. |
| measure_columns | LIST | The list of measure columns. |
| sort_columns | LIST | The list of sort columns. |
| partition_columns | LIST | The list of partition columns. |
| distribution_columns | LIST | The list of distribution columns. |
| acceleration_count | BIGINT | The number of times the reflection would have accelerated queries. |
| ratio | DOUBLE | The ratio of acceleration. |
| error_message | VARCHAR | Any error message associated with the recommendation. |

### sys.reflection_lineage

Return a list of the Reflections that will also be refreshed if a refresh is triggered for a particular Reflection.

**Syntax:**
```sql
SELECT * FROM TABLE(sys.reflection_lineage('<reflection_id>'))
```

**Parameters:**
*   `<reflection_id>` (String): The ID of the Reflection.

**Columns:**

| Column | Data Type | Description |
| --- | --- | --- |
| reflection_id | nvarchar | The ID of the Reflection. |
| reflection_name | nvarchar | The name of the Reflection. |
| dataset_name | nvarchar | The name of the dataset. |
| dataset_id | nvarchar | The ID of the dataset. |
| reflection_type | nvarchar | The type of Reflection. Enum: `RAW`, `AGG` |
| status | nvarchar | The status of the Reflection. Enum: `INVALID`, `REFRESHING`, `METADATA_REFRESH`, `COMPACTING`, `FAILED`, `DEPRECATED`, `CANNOT_ACCELERATE`, `MANUAL_REFRESH`, `DONE` |
| num_failures | integer | The number of consecutive failures for the Reflection. |
| is_active | boolean | Indicates whether the Reflection is active (true) or inactive (false). |
| can_view | boolean | Indicates whether the current user has permission to view the Reflection. |

### sys.reflection_refresh_settings

Returns the refresh settings for a Reflection, including settings inherited from the datasets that the Reflection depends on.

**Syntax:**
```sql
SELECT * FROM TABLE(sys.reflection_refresh_settings('<reflection_id>'))
```

**Columns:**

| Column | Data Type | Description |
| --- | --- | --- |
| table_type | nvarchar | Defines the type of table. Enum: `DATASET` or `EXTERNAL_QUERY` |
| table_path | nvarchar | Identifies the path to the dataset or external query source that the Reflection depends on. |
| table_version_context | nvarchar | Specifies the versioning context for datasets, stored in JSON format. |
| overrides_source | boolean | Indicates whether settings are inherited from the source (true) or set on the table (false). |
| refresh_method | nvarchar | Shows the method used for the most recent refresh of the Reflection. Enum: `FULL`, `INCREMENTAL`, `AUTO` |
| refresh_policy | nvarchar | Identifies the type of refresh policy. Enum: `PERIOD`, `SCHEDULE`, `LIVE_REFRESH`, `NEVER_REFRESH` |
| refresh_period_seconds | double | Specifies the time in seconds (truncated from milliseconds) between refreshes. |
| refresh_schedule | nvarchar | Provides the cron expression (UTC) that defines the refresh schedule for the Reflection. |
| never_expire | boolean | Indicates whether the Reflection never expires (true) or uses the expiration setting (false). |
| expiration_seconds | double | Defines the expiration time in seconds (truncated from milliseconds), after which the system removes the Reflection. |

