## System Tables

System tables make up Dremio's system-created catalog to store metadata for the objects in your Dremio organization.

### sys.organization.model_usage

Contains metadata for LLM model usage through Dremio.

| Field | Data Type | Description |
| --- | --- | --- |
| organization_id | nvarchar | The UUID of the organization. |
| project_id | nvarchar | The UUID of the project. |
| user_id | nvarchar | The UUID of the user. |
| model_name | nvarchar | The name of the model. |
| operation | nvarchar | The operation performed. Enum: `CHAT`, `SQL` |
| input_tokens | integer | The number of input tokens. |
| output_tokens | integer | The number of output tokens. |
| timestamp | timestamp | The timestamp of the usage. |

### sys.organization.privileges

Contains metadata for privileges at the organization-level.

| Field | Data Type | Description |
| --- | --- | --- |
| grantee_id | nvarchar | The UUID of the user or role that has been granted the privilege. |
| grantee_type | nvarchar | The type of grantee. Enum: `user`, `role` |
| privilege | nvarchar | The privilege that has been granted. |
| object_id | nvarchar | The UUID of the object on which the privilege has been granted. |
| object_type | nvarchar | The type of the object on which the privilege has been granted. |

### sys.organization.projects

Contains metadata for projects in an organization.

| Field | Data Type | Description |
| --- | --- | --- |
| project_id | nvarchar | The UUID to identify the project. |
| project_name | nvarchar | The name of the project. |
| project_state | nvarchar | The state of the project. Enum: `COMMISSIONING`, `ACTIVE`, `FAILED`, `MARK_DELETE` |
| description | nvarchar | The description of the project. |
| created | timestamp | The timestamp for when the project was created. |
| organization_id | nvarchar | The UUID of the organization. |
| identity_type | nvarchar | The type of identity. Enum: `ACCESS_KEY`, `IAM_ROLE` |
| owner_id | nvarchar | The UUID of the owner. |
| owner_type | nvarchar | The type of owner. Enum: `USER`, `ROLE` |

### sys.organization.roles

Contains metadata for roles in an organization.

| Field | Data Type | Description |
| --- | --- | --- |
| role_id | nvarchar | The UUID to identify the role. |
| role_name | nvarchar | The name of the role. |
| role_type | nvarchar | The type of role. Enum: `SYSTEM`, `INTERNAL`, `USER` |
| owner_id | nvarchar | The UUID of the owner (user or role) of the role. |
| owner_type | nvarchar | The type of owner of the role. Enum: `USER`, `ROLE` |
| created | timestamp | The timestamp for when the role was created. |
| created_by | nvarchar | The method of creation. Enum: `LOCAL`, `SCIM` |

### sys.organization.usage

Contains data about an organization's usage.

| Field | Data Type | Description |
| --- | --- | --- |
| organization_id | nvarchar | The UUID of the organization. |
| project_id | nvarchar | The UUID of the project. |
| edition | nvarchar | The edition of Dremio. |
| job_id | nvarchar | The UUID of the job. |
| user_id | nvarchar | The UUID of the user. |
| start_time | timestamp | The start time of the job. |
| end_time | timestamp | The end time of the job. |
| engine_id | nvarchar | The UUID of the engine. |
| engine_name | nvarchar | The name of the engine. |
| engine_size | nvarchar | The size of the engine (e.g., m5d.4xlarge). |
| dcu | double | The number of Dremio Capacity Units (DCUs) consumed. |
| job_type | nvarchar | The type of job. |
| status | nvarchar | The status of the job. |
| considered_reflection_count | integer | The number of reflections considered. |
| matched_reflection_count | integer | The number of reflections matched. |
| chosen_reflection_count | integer | The number of reflections chosen. |

### sys.organization.users

Contains metadata for users in an organization.

| Field | Data Type | Description |
| --- | --- | --- |
| user_id | nvarchar | The UUID to identify the user. |
| user_name | nvarchar | The email of the user is used as the username. |
| first_name | nvarchar | The first name of the user. |
| last_name | nvarchar | The last name of the user. |
| status | nvarchar | The state of the user depending on if they have accepted the invite to the organization and have logged in to the application. Enum: `active`, `invited` |
| user_type | nvarchar | The type of user based on how it was created. Enum: `EXTERNAL`, `LOCAL` |
| created | timestamp | The timestamp for when the user was created. |
| owner_id | nvarchar | The UUID for the owner (user or role) of the user. This UUID corresponds to the `user_id` or `role_id` in the `users` or `roles` table. |
| owner_type | nvarchar | The type of owner of the user. Enum: `user`, `role` |
| created_by | nvarchar | The method of creation. Enum: `LOCAL`, `SCIM` |

### sys.project.engines

Contains metadata for engines in a project.

| Field | Data Type | Description |
| --- | --- | --- |
| engine_id | nvarchar | The UUID to identify the engine. |
| engine_name | nvarchar | The name of the engine. |
| engine_size | nvarchar | The size of the engine. Enum: `XX_SMALL_V1`, `X_SMALL_V1`, `SMALL_V1`, `MEDIUM_V1`, `LARGE_V1`, `X_LARGE_V1`, `XX_LARGE_V1`, `XXX_LARGE_V1` |
| engine_state | nvarchar | The state of the engine. Enum: `DELETING`, `DISABLED`, `DISABLING`, `ENABLED` |
| min_replicas | integer | The minimum number of replicas for the engine. |
| max_replicas | integer | The maximum number of replicas for the engine. |
| current_replicas | integer | The current number of replicas for the engine. |
| instance_family | nvarchar | The instance family of the engine. |
| tag | nvarchar | The tag of the engine. |

### sys.project.jobs

Contains the metadata for the jobs in a project.

| Field | Data Type | Description |
| --- | --- | --- |
| job_id | nvarchar | The UUID to identify the job. |
| job_type | nvarchar | The type of job. Enum: `ACCELERATOR_CREATE`, `ACCELERATOR_DROP`, `ACCELERATOR_EXPLAIN`, `FLIGHT`, `INTERNAL_ICEBERG_METADATA_DROP`, `JDBC`, `UI_EXPORT`, `UI_INTERNAL_PREVIEW`, `UI_INTERNAL_RUN`, `UI_PREVIEW`, `UI_RUN`, `METADATA_REFRESH`, `ODBC`, `PREPARE_INTERNAL`, `REST`, `UNKNOWN` |
| status | nvarchar | The status of the job. Enum: `SETUP`, `QUEUED`, `ENGINE START`, `RUNNING` |
| user_name | nvarchar | The username of the user who submitted the job. |
| submitted_ts | timestamp | The timestamp for when the job was submitted. |
| submitted_epoch | bigint | The epoch timestamp for when the job was submitted. |
| is_accelerated | boolean | Whether the job was accelerated. |
| accelerated_by_substitution | boolean | Whether the job was accelerated by substitution. |
| queried_datasets | array | The datasets that were queried. |
| scanned_datasets | array | The datasets that were scanned. |
| attempt_count | integer | The number of attempts for the job. |
| error_msg | nvarchar | The error message if the job failed. |
| query_type | nvarchar | The type of query. |

### sys.project.pipes

Contains the metadata for autoingest pipes in a project.

| Column Name | Data Type | Description |
| --- | --- | --- |
| pipe_name | nvarchar | The name of the pipe. |
| pipe_id | nvarchar | The unique identifier of the pipe. |
| pipe_state | nvarchar | The current state of the pipe. Enum: `Running`, `Paused`, `Stopped_Missing_Table_or_Branch`, `Stopped_Storage_Location_Altered`, `Stopped_Access_Denied`, `Stopped_Missing_Dremio_Source`, `Unhealthy`, `Stopped_Internal_Error` |
| dedupe_lookback_period | integer | The number of days to look back for deduplication. |
| notification_provider | nvarchar | The notification provider for the pipe. |
| notification_queue_reference | nvarchar | The reference to the notification queue. |
| source_root_path | nvarchar | The root path of the source data. |
| target_table | nvarchar | The target table for the pipe. |
| file_format | nvarchar | The file format of the source data. |
| pipe_owner | nvarchar | The owner of the pipe. |
| created_at | timestamp | The timestamp for when the pipe was created. |
| last_updated_at | timestamp | The timestamp for when the pipe was last updated. |
| cloud_settings | nvarchar | The cloud settings for the pipe. |

### sys.project.privileges

Contains metadata for privileges at the project-level.

| Field | Data Type | Description |
| --- | --- | --- |
| grantee_id | nvarchar | The UUID of the user or role that has been granted the privilege. |
| grantee_type | nvarchar | The type of grantee. Enum: `user`, `role` |
| privilege | nvarchar | The privilege that has been granted. |
| object_id | nvarchar | The UUID of the object on which the privilege has been granted. |
| object_type | nvarchar | The type of the object on which the privilege has been granted. (e.g., VDS for view) |

### sys.project.reflection_dependencies

Contains metadata for Reflection dependencies in the current project.

| Field | Data Type | Description |
| --- | --- | --- |
| reflection_id | nvarchar | The UUID of the Reflection. |
| dependency_id | nvarchar | The UUID of the dependency. |
| dependency_type | nvarchar | The type of dependency. Enum: `DATASET`, `REFLECTION` |
| dependency_path | array | The path of the dependency. |

### sys.project.reflections

Contains metadata for Reflections in a project.

| Field | Data Type | Description |
| --- | --- | --- |
| reflection_id | nvarchar | The UUID to identify the Reflection. |
| reflection_name | nvarchar | The name of the Reflection. |
| type | nvarchar | The type of Reflection. Enum: `AGGREGATION`, `RAW` |
| status | nvarchar | The status of the Reflection. Enum: `CAN_ACCELERATE`, `CAN_ACCELERATE_WITH_FAILURES`, `REFRESHING`, `FAILED`, `EXPIRED`, `DISABLED`, `INVALID`, `CANNOT_ACCELERATE_SCHEDULED`, `CANNOT_ACCELERATE_MANUAL` |
| dataset_id | nvarchar | The UUID of the dataset that the Reflection is defined on. |
| dataset_name | nvarchar | The name of the dataset. |
| dataset_type | nvarchar | The type of dataset. Enum: `PHYSICAL_DATASET_HOME_FILE`, `PHYSICAL_DATASET_SOURCE_FILE`, `PHYSICAL_DATASET_SOURCE_FOLDER`, `VIRTUAL_DATASET` |
| sort_columns | array | The columns that the Reflection is sorted by. |
| partition_columns | array | The columns that the Reflection is partitioned by. |
| distribution_columns | array | The columns that the Reflection is distributed by. |
| dimensions | array | The dimensions of the Reflection. |
| measures | array | The measures of the Reflection. |
| external_reflection | nvarchar | The name of the external reflection. |
| arrow_caching_enabled | boolean | Whether Arrow caching is enabled. |
| partition_distribution_strategy | nvarchar | The partition distribution strategy. |
| measure_fields | array | The measure fields. |
| dimension_fields | array | The dimension fields. |
| display_columns | array | The display columns. |
| num_failures | integer | The number of failures. |
| created | timestamp | The timestamp for when the Reflection was created. |
| modified | timestamp | The timestamp for when the Reflection was last modified. |
| refresh_method | nvarchar | The refresh method. Enum: `Manual`, `Autonomous` |
| refresh_status | nvarchar | The refresh status. Enum: `NONE` |

### sys.project."tables"

Contains metadata for tables in a project.

| Field | Data Type | Description |
| --- | --- | --- |
| table_id | nvarchar | The UUID to identify the table. |
| table_name | nvarchar | The name of the table. |
| schema_id | nvarchar | The UUID for the schema/folder in which the table is contained. |
| path | nvarchar | The string array representation of the path of the table. |
| tag | nvarchar | The UUID that is generated to identify the instance of the table. Dremio changes this tag whenever a change is made to the table. |
| type | nvarchar | The type of table. Enum: `PHYSICAL_DATASET`, `SYSTEM_TABLE`, `NESSIE_TABLE` |
| format | nvarchar | The format of the table. Enum: `DELTA`, `EXCEL`, `ICEBERG`, `JSON`, `PARQUET`, `TEXT`, `UNKNOWN`, `XLS` |
| created | timestamp | The date and time that the table was created. |
| owner_id | nvarchar | The UUID for the owner (user or role) of the table. |
| owner_type | nvarchar | The type of owner of the table. Enum: `USER_OWNER`, `ROLE_OWNER` |
| record_count | bigint | The number of records in the table. |
| column_count | integer | The number of columns in the table. |
| is_approximate_stats | boolean | Whether the statistics are approximate. |

### sys.project.views

Contains metadata for views in a project.

| Field | Data Type | Description |
| --- | --- | --- |
| view_id | nvarchar | The UUID to identify the view. |
| space_id | nvarchar | The UUID to identify the parent space that the view is saved under. |
| view_name | nvarchar | The user- or system-defined name of the view. |
| schema_id | nvarchar | The UUID for the schema/folder in which the view is contained. |
| path | nvarchar | The string array representation of the path of the view. |
| tag | nvarchar | The UUID that is generated to identify the instance of the view. Dremio changes this tag whenever a change is made to the view. |
| type | nvarchar | The type of view. Enum: `VIRTUAL_DATASET`, `NESSIE_VIEW` |
| created | timestamp | The date and time that the view was created. |
| sql_definition | nvarchar | The DDL statement that was used to create the view. |
| sql_context | nvarchar | The context for the SQL definition. |
| owner_id | nvarchar | The UUID for the owner (user or role) of the view. |
| owner_type | nvarchar | The type of owner of the view. Enum: `USER_OWNER`, `ROLE_OWNER` |

### sys.project.copy_errors_history

Contains metadata for copy errors history.

| Column Name | Data Type | Description |
| --- | --- | --- |
| executed_at | timestamp | The timestamp when the copy command was executed. |
| job_id | nvarchar | The UUID of the job that executed the copy command. |
| table_name | nvarchar | The name of the table. |
| user_name | nvarchar | The name of the user who executed the command. |
| file_path | nvarchar | The path of the file that caused the error. |
| line_number | bigint | The line number in the file where the error occurred. |
| error_message | nvarchar | The error message. |

### sys.project.copy_file_history

Contains metadata for copy file history.

| Column Name | Data Type | Description |
| --- | --- | --- |
| executed_at | timestamp | The timestamp when the copy command was executed. |
| job_id | nvarchar | The UUID of the job that executed the copy command. |
| table_name | nvarchar | The name of the table. |
| user_name | nvarchar | The name of the user who executed the command. |
| file_path | nvarchar | The path of the file that was copied. |
| file_state | nvarchar | The state of the file copy. Enum: `LOADED`, `PARTIALLY_LOADED`, `SKIPPED` |
| records_loaded_count | bigint | The number of records loaded. |
| records_rejected_count | bigint | The number of records rejected. |

### sys.project.history.autonomous_reflections

Contains metadata for autonomous reflections history.

| Column Name | Data Type | Description |
| --- | --- | --- |
| reflection_id | nvarchar | The UUID of the Reflection. |
| reflection_name | nvarchar | The name of the Reflection. |
| dataset_id | nvarchar | The UUID of the dataset. |
| dataset_name | nvarchar | The name of the dataset. |
| status | nvarchar | The status of the Reflection. |
| event_type | nvarchar | The type of event. |
| event_timestamp | timestamp | The timestamp of the event. |
| details | nvarchar | The details of the event. |

### sys.project.history.events

Contains metadata for historical events.

| Field | Data Type | Description |
| --- | --- | --- |
| event_id | nvarchar | The UUID of the event. |
| event_type | nvarchar | The type of event. |
| event_timestamp | timestamp | The timestamp of the event. |
| user_id | nvarchar | The UUID of the user who triggered the event. |
| entity_id | nvarchar | The UUID of the entity related to the event. |
| entity_type | nvarchar | The type of entity. |
| details | nvarchar | The details of the event. |

### sys.project.history.jobs

Contains metadata for historical jobs.

| Field | Data Type | Description |
| --- | --- | --- |
| job_id | nvarchar | The UUID to identify the job. |
| job_type | nvarchar | The type of job. |
| status | nvarchar | The status of the job. |
| user_name | nvarchar | The username of the user who submitted the job. |
| submitted_ts | timestamp | The timestamp for when the job was submitted. |
| submitted_epoch | bigint | The epoch timestamp for when the job was submitted. |
| is_accelerated | boolean | Whether the job was accelerated. |
| accelerated_by_substitution | boolean | Whether the job was accelerated by substitution. |
| queried_datasets | array | The datasets that were queried. |
| scanned_datasets | array | The datasets that were scanned. |
| attempt_count | integer | The number of attempts for the job. |
| error_msg | nvarchar | The error message if the job failed. |
| query_type | nvarchar | The type of query. |

### sys.project.materializations

Contains metadata for materializations.

| Field | Data Type | Description |
| --- | --- | --- |
| materialization_id | nvarchar | The UUID of the materialization. |
| reflection_id | nvarchar | The UUID of the Reflection. |
| job_id | nvarchar | The UUID of the job that created the materialization. |
| created | timestamp | The timestamp for when the materialization was created. |
| expires | timestamp | The timestamp for when the materialization expires. |
| state | nvarchar | The state of the materialization. |
| footprint | bigint | The size of the materialization. |
| original_cost | double | The original cost of the query. |
| reflection_type | nvarchar | The type of Reflection. |
| series_id | nvarchar | The series ID. |
| series_ordinal | integer | The series ordinal. |
| join_analysis | nvarchar | The join analysis. |

### sys.project.pipe_summary

Contains metadata for pipe summary.

| Column Name | Data Type | Description |
| --- | --- | --- |
| pipe_name | nvarchar | The name of the pipe. |
| pipe_id | nvarchar | The unique identifier of the pipe. |
| jobs_count | integer | The number of jobs completed for autoingestion related to this pipe. |
| files_loaded_count | integer | The number of files loaded by the pipe. |
| files_skipped_count | integer | The number of files skipped by the pipe. |
| files_partially_loaded_count | integer | The number of files partially loaded by the pipe. |
| pipe_status | nvarchar | The current status of the pipe. |
| error_message | nvarchar | The error message if the pipe is in an error state. |
| last_updated_at | timestamp | The timestamp of the last update to the pipe summary. |
| total_records_count | integer | The total number of records processed by the pipe. |


