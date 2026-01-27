## SQL Commands

### `SELECT`

Dremio supports querying using standard `SELECT` statements. You can query tables and views in connected sources and catalogs.

When working with Apache Iceberg tables, you can:

- Query table metadata  
- Run queries by snapshot ID  

**note**  
Dremio supports reading positional and equality deletes for Iceberg v2 tables. Dremio writes using copy-on-write by default and supports merge-on-read when enabled in table properties.

#### Syntax

```sql
[ WITH ... ]
SELECT [ ALL | DISTINCT ]
{ *
| <column_name1>, <column_name2>, ... }
FROM { <table_name> | <view_name>
| TABLE ( <iceberg_metadata> ( <table_name> ) )
| UNNEST ( <list_expression> ) [ WITH ORDINALITY ] }
[ { PIVOT | UNPIVOT } ( <expression> ) ]
[ WHERE <condition> ]
[ GROUP BY <expression> ]
[ QUALIFY <expression> ]
[ ORDER BY <column_name1>, <column_name2>, ... [ DESC ] ]
[ LIMIT <count> ]
[ AT { { REF[ERENCE] | BRANCH | TAG | COMMIT } <reference_name>
[ AS OF <timestamp> ]
| { SNAPSHOT <snapshot_id> | <timestamp> } } ]
| <function_name>
[ AT { REF[ERENCE] | BRANCH | TAG | COMMIT } <reference_name> ]
[ AS OF <timestamp> ]
| TABLE(<source_name>.EXTERNAL_QUERY ('<select_statement>'))
```

#### Parameters

- **`WITH`**  
  Defines a common table expression (CTE).

- **`ALL` / `DISTINCT`**  
  `ALL` returns all rows. `DISTINCT` removes duplicates.

- **`*`**  
  Selects all columns.

- **`<column_name>`**  
  One or more columns to query.

- **`FROM <table_name> | <view_name>`**  
  Source of the data.

- **`FROM TABLE(<iceberg_metadata>(<table_name>))`**  
  Queries Iceberg system metadata. Metadata includes:
  - Data files  
  - History  
  - Manifest files  
  - Partition statistics  
  - Snapshots  

#### Supported Iceberg Metadata Tables

##### `table_files(<table_name>)`
Returns metadata for each data file including:
- file_path  
- file_format  
- partition  
- record_count  
- file_size_in_bytes  
- column_sizes  
- value_counts  
- null_value_counts  
- nan_value_counts  
- lower_bounds  
- upper_bounds  
- key_metadata  
- split_offsets  

##### `table_history(<table_name>)`
Returns:
- made_current_at  
- snapshot_id  
- parent_id  
- is_current_ancestor  

##### `table_manifests(<table_name>)`
Returns:
- path  
- length  
- partition_spec_id  
- added_snapshot_id  
- added_data_files_count  
- existing_data_files_count  
- deleted_data_files_count  
- partition_summaries  

##### `table_partitions('<table_name>')`
Includes:
- partition  
- record_count  
- file_count  
- spec_id  

##### `table_snapshot(<table_name>)`
Includes:
- committed_at  
- snapshot_id  
- parent_id  
- operation  
- manifest_list  
- summary  

##### `clustering_information('<table_name>')`
Includes:
- table_name  
- clustering_keys  
- clustering_depth  
- last_clustering_timestamp  

#### `UNNEST(<list_expression>) [WITH ORDINALITY]`

- Expands a LIST into rows.  
- `WITH ORDINALITY` adds index values.

#### `PIVOT` / `UNPIVOT`

- `PIVOT`: rows → columns  
- `UNPIVOT`: columns → rows  

**note:** Aliases between table/subquery and pivot clauses are not supported.

#### `WHERE <condition>`

Filters records using comparison or logical operators (`=`, `>=`, `<`, `AND`, `OR`, `IN`, etc.).

#### `GROUP BY <expression>`

Groups rows to compute aggregations like `COUNT()`, `SUM()`, `AVG()`.

#### `QUALIFY <expression>`

Filters results *after* window functions are evaluated.

#### `ORDER BY <column_name> [DESC]`

Sorts results.

#### `LIMIT <count>`

Restricts number of returned rows.

#### `AT REF | BRANCH | TAG | COMMIT <reference_name>`

Time-travel and versioned queries.

- `REF` for any reference  
- `BRANCH`, `TAG`, `COMMIT`  
- Commit hashes must be in double quotes

#### `AS OF <timestamp>`

Reads the reference as of a timestamp.

#### `AT SNAPSHOT <snapshot_id>`

Reads a specific Iceberg or Delta snapshot.

#### `<function_name>`

Execute a UDF.

#### `TABLE(<source>.EXTERNAL_QUERY('...'))`

Runs a native query directly on external systems.

Limitations:

- Only SELECT statements allowed  
- No batched/multi-statement returns  
- Views created from EXTERNAL_QUERY cannot move before first refresh  

#### Examples

##### Query an existing table
```sql
SELECT *
FROM Samples."samples.dremio.com"."zips.json";
```

##### Query a specific column
```sql
SELECT city
FROM Samples."samples.dremio.com"."zips.json";
```

##### DISTINCT example
```sql
SELECT DISTINCT city
FROM Samples."samples.dremio.com"."zips.json";
```

##### WHERE clause
```sql
SELECT *
FROM Samples."samples.dremio.com"."zips.json"
WHERE state = 'MA' AND city = 'AGAWAM';
```

##### QUALIFY example (in SELECT)
```sql
SELECT passenger_count, trip_distance_mi, fare_amount,
RANK() OVER (PARTITION BY passenger_count ORDER BY trip_distance_mi) AS pc_rank
FROM "NYC-taxi-trips"
QUALIFY pc_rank = 1;
```

##### QUALIFY example (in QUALIFY)
```sql
SELECT passenger_count, trip_distance_mi, fare_amount
FROM "NYC-taxi-trips"
QUALIFY RANK() OVER (PARTITION BY passenger_count ORDER BY trip_distance_mi) = 1;
```

##### GROUP BY and ORDER BY
```sql
SELECT COUNT(city), city, state
FROM Samples."samples.dremio.com"."zips.json"
GROUP BY state, CITY
ORDER BY COUNT(city) DESC;
```

##### CTE example
```sql
WITH cte_quantity (Total) AS (
SELECT SUM(passenger_count) AS Total
FROM Samples."samples.dremio.com"."NYC-taxi-trips"
WHERE passenger_count > 2
GROUP BY pickup_datetime
)
SELECT AVG(Total) AS average_pass
FROM cte_quantity;
```

##### PIVOT / UNPIVOT example
```sql
ALTER DATASET Samples."samples.dremio.com"."SF weather 2018-2019.csv"
REFRESH METADATA auto promotion FORCE UPDATE;

SELECT * FROM (
SELECT EXTRACT(YEAR FROM CAST(F AS DATE)) AS "YEAR",
EXTRACT(MONTH FROM CAST(F AS DATE)) AS "MONTH",
K AS MAX_TEMP
FROM Samples."samples.dremio.com"."SF weather 2018-2019.csv"
WHERE F <> 'DATE'
)
PIVOT (
max(MAX_TEMP) FOR "MONTH" IN (1 AS JAN, 2 AS FEB, 3 AS MAR, 4 AS APR, 5 AS MAY, 6 AS JUN,
7 AS JUL, 8 AS AUG, 9 AS SEP, 10 AS OCT, 11 AS NOV, 12 AS "DEC")
)
UNPIVOT (
GLOBAL_MAX_TEMP FOR "MONTH" IN (JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, "DEC")
)
ORDER BY "YEAR","MONTH";
```

##### UNNEST example
```sql
SELECT index, UPPER(array_item)
FROM UNNEST (ARRAY['a','b','c']) WITH ORDINALITY AS my_table (array_item, index)
ORDER BY index;
```

##### Query using a branch reference
```sql
SELECT *
FROM myCatalog.demo_table AT REF main_branch;
```

##### Query using a commit
```sql
SELECT *
FROM myCatalog.demo_view AT COMMIT "7f643f2b9cf250ce1f5d6ff4397237b705d866fbf34d714";
```

##### Time-travel by timestamp
```sql
SELECT *
FROM myTable AT TIMESTAMP '2022-01-01 17:30:50.000';
```

##### Time-travel by snapshot
```sql
SELECT *
FROM myTable AT SNAPSHOT '5393090506354317772';
```

##### Query Iceberg history
```sql
SELECT *
FROM TABLE(table_history('myTable'))
WHERE snapshot_id = 4593468819579153853;
```

##### Count snapshots
```sql
SELECT COUNT(*)
FROM TABLE(table_snapshot('myTable'))
```

#### Time-travel by timestamp
```sql
SELECT *
FROM myTable AT TIMESTAMP '2022-01-01 17:30:50.000';
```

#### Time-travel by snapshot
```sql
SELECT *
FROM myTable AT SNAPSHOT '5393090506354317772';
```

#### Query Iceberg history
```sql
SELECT *
FROM TABLE(table_history('myTable'))
WHERE snapshot_id = 4593468819579153853;
```

#### Count snapshots
```sql
SELECT COUNT(*)
FROM TABLE(table_snapshot('myTable'))
GROUP BY snapshot_id;
```

#### External query
```sql
SELECT *
FROM TABLE(<source_name>.EXTERNAL_QUERY('SELECT * FROM Actor'));
```

#### External query with string literal
```sql
SELECT *
FROM TABLE(<source_name>.EXTERNAL_QUERY('SELECT string_col FROM tbl WHERE string_col = ''test'' '));
```

#### JOIN external query
```sql
SELECT B.customer_id, A.product_id, A.price
FROM TABLE(<source_name>.EXTERNAL_QUERY('SELECT product_id, price FROM products')) AS A,
source_b.sales AS B
WHERE B.product_id = A.product_id;
```

#### Time-travel by snapshot
```sql
SELECT *
FROM myTable AT SNAPSHOT '5393090506354317772';
```

#### Query Iceberg history
```sql
SELECT *
FROM TABLE(table_history('myTable'))
WHERE snapshot_id = 4593468819579153853;
```

#### Count snapshots
```sql
SELECT COUNT(*)
FROM TABLE(table_snapshot('myTable'))
GROUP BY snapshot_id;
```

#### Escaping quotes
```sql
SELECT *
FROM TABLE(<source_name>.EXTERNAL_QUERY('SELECT string_col FROM tbl WHERE string_col = ''john '''' s car '''));
```

#### External query
```sql
SELECT *
FROM TABLE(<source_name>.EXTERNAL_QUERY('SELECT * FROM Actor'));
```

#### External query with string literal
```sql
SELECT *
FROM TABLE(<source_name>.EXTERNAL_QUERY('SELECT string_col FROM tbl WHERE string_col = ''test'' '));
```

#### Escaping quotes
```sql
SELECT *
FROM TABLE(<source_name>.EXTERNAL_QUERY('SELECT string_col FROM tbl WHERE string_col = ''john '''' s car '''));
```

#### JOIN external query
```sql
SELECT B.customer_id, A.product_id, A.price
FROM TABLE(<source_name>.EXTERNAL_QUERY('SELECT product_id, price FROM products')) AS A,
source_b.sales AS B
WHERE B.product_id = A.product_id;
```

#### Column Aliasing

If you specify an alias, you can reference it elsewhere in the query.

#### Example 1
```sql
SELECT c_custkey AS c, lower(c)
FROM "customer.parquet";
```

#### Example 2
```sql
SELECT c_custkey AS c, lower(c)
FROM (
SELECT c_custkey, c_mktsegment AS c
FROM "customer.parquet"
);
```

#### Example 3
```sql
SELECT c_name AS n, n
FROM (
SELECT c_mktsegment AS n, c_name
FROM "customer.parquet"
) AS MY_TABLE
WHERE n = 'BUILDING';
```

#### Example 4
```sql
SELECT c_custkey
FROM (
SELECT c_custkey, c_name AS c
FROM "customer.parquet"
)
WHERE c = 'aa';
```

#### Example 5
```sql
SELECT *
FROM (
SELECT c_custkey AS c, c_name
FROM "customer.parquet"
)
JOIN "orders.parquet" ON c = o_orderkey;
```

#### Example 6
```sql
SELECT c_custkey AS c
FROM "customer.parquet"
JOIN "orders.parquet" ON c = o_orderkey;
```

#### Distributing Data Evenly Across Engines (BROADCAST Hint)

Use a BROADCAST hint if a join is skewed.

**note:** Not supported on views; ignored for nested-loop joins.

Syntax (inline): `/*+ BROADCAST */`

#### Example 1
```sql
SELECT *
FROM T1 /*+ BROADCAST */
INNER JOIN t2 ON t1.key = t2.key
INNER JOIN t3 ON t2.key = t3.key;
```

#### Example 2
```sql
SELECT *
FROM T1
INNER JOIN (
SELECT key, max(cost) cost
FROM t2 /*+ BROADCAST */
) T2 ON t1.key = t2.key
INNER JOIN t3 ON t2.key = t3.key;
```

#### `copy_errors()` — Inspect Rejected COPY INTO Records

#### Syntax
```sql
SELECT *
FROM TABLE(copy_errors('<table_name>', ['<query_id>']));
```

#### Fields Returned

- `job_id`: ID of the COPY job  
- `file_name`: file path  
- `line_number`: physical line number  
- `row_number`: record position  
- `column_name`: column with error  
- `error`: error description  

### `ALTER PIPE` Preview

Changes an existing autoingest pipe.

#### Syntax

```sql
ALTER PIPE <pipe_name>
{ SET PIPE_EXECUTION_RUNNING = { TRUE | FALSE }
| [ DEDUPE_LOOKBACK_PERIOD <number_of_days> ]
AS COPY INTO <table_name>
FROM '@<storage_location_name>[ /<folder_name> ]'
[ FILE_FORMAT 'csv' | 'json' | 'parquet']
[ ( [csv_format_options] | [json_format_options] | [parquet_format_options]) ]
}
```

#### CSV Format Options
```sql
[ DATE_FORMAT '<string>' ]
[ EMPTY_AS_NULL [ '<boolean>' ] [, ...] ]
[ ESCAPE_CHAR '<escape_character>' ]
[ EXTRACT_HEADER '<boolean>' ]
[ FIELD_DELIMITER '<character>' ]
[ NULL_IF ('<string>' [, ...]) ]
[ ON_ERROR 'skip_file' ]
[ QUOTE_CHAR '<character>' ]
[ RECORD_DELIMITER '<character>' ]
[ SKIP_LINES <n> ]
[ TIME_FORMAT '<string>' ]
[ TIMESTAMP_FORMAT '<string>' ]
[ TRIM_SPACE [ '<boolean>' ] ]
```

#### JSON Format Options
```sql
[ DATE_FORMAT '<string>' ]
[ EMPTY_AS_NULL [ '<boolean>' ] [, ...] ]
[ NULL_IF ('<string>' [, ...]) [, ...] ]
[ ON_ERROR 'skip_file' ]
[ TIME_FORMAT '<string>' ]
[ TIMESTAMP_FORMAT '<string>' ]
[ TRIM_SPACE [ '<boolean>' ] ]
```

#### Parquet Format Options
```sql
[ ON_ERROR 'skip_file' ]
```

#### Parameters

- **`<pipe_name>`**  
  Unique name of the autoingest pipe. Cannot be modified.

- **`SET PIPE_EXECUTION_RUNNING = { TRUE | FALSE }`**  
  Controls whether the pipe triggers a `COPY INTO` on notifications.  
  - `TRUE`: pipe active  
  - `FALSE`: pipe paused (default is TRUE)

- **`DED UPE_LOOKBACK_PERIOD <days>`**  
  - Days to look back for deduplication (0–90).  
  - Default: 14 days.

- **`AS COPY INTO <table_name>`**  
  Target Iceberg table. Use full qualifier if not in current context.

- **`@<storage_location_name>`**  
  Source location for files. Must exist as a configured Dremio source.

  **note:** Autoingest pipes ingest only from Amazon S3.

- **`/<folder_name>`**  
  Optional subfolder under the storage location.

- **`FILE_FORMAT 'csv' | 'json' | 'parquet'`**  
  Required. All files must match format.  
  - CSV/JSON may be compressed (`.gz`, `.bz2`)  
  - Parquet supports only `ON_ERROR 'skip_file'`

#### CSV Format Option Details

- **`DATE_FORMAT '<string>'`**  
  Defaults to `YYYY-MM-DD`.

- **`EMPTY_AS_NULL '<boolean>'`**  
  Default: `TRUE`.

- **`ESCAPE_CHAR '<escape_character>'`**  
  Default: `"`.

- **`EXTRACT_HEADER '<boolean>'`**  
  Default: `TRUE`.

- **`FIELD_DELIMITER '<character>'`**  
  Default: `,`.

- **`NULL_IF ('<string>' ...)`**  
  Strings to convert to NULL.

- **`ON_ERROR 'skip_file'`**  
  Stops at first error and logs error to `sys.project.copy_errors_history`.

- **`QUOTE_CHAR '<character>'`**  
  Default: `"`. 

- **`RECORD_DELIMITER '<character>'`**  
  Default: `\r\n`.

- **`SKIP_LINES <n>`**  
  Skips initial lines.

- **`TIME_FORMAT '<string>'`**  
  Default: `HH24:MI:SS.FFF`.

- **`TIMESTAMP_FORMAT '<string>'`**  
  Default: `YYYY-MM-DD HH24:MI:SS.FFF`.

- **`TRIM_SPACE '<boolean>'`**  
  Default: `FALSE`.

#### JSON Format Option Details

- **`DATE_FORMAT '<string>'`** – default: `YYYY-MM-DD`  
- **`EMPTY_AS_NULL '<boolean>'`** – default: `TRUE`  
- **`NULL_IF ('<string>'...)`** – replace values with NULL  
- **`ON_ERROR 'skip_file'`** – default, only supported mode  
- **`TIME_FORMAT '<string>'`** – default: `HH24:MI:SS.FFF`  
- **`TIMESTAMP_FORMAT '<string>'`** – default: `YYYY-MM-DD HH24:MI:SS.FFF`  
- **`TRIM_SPACE '<boolean>'`** – default: `FALSE`

#### Parquet Format Option Details

- **`ON_ERROR 'skip_file'`** only  
  - Logs first error to history  
  - Requires extra file processing  
  - Skips entire file on any error  

#### Examples

#### Pause an autoingest pipe
```sql
ALTER PIPE test_pipe
SET PIPE_EXECUTION_RUNNING = FALSE
```

#### Change the pipe storage location
```sql
ALTER PIPE test_pipe
AS COPY INTO Table_one
FROM '@s3_source/folder'
FILE_FORMAT 'json'
```

### `ALTER SOURCE`

Change the configuration or status of an existing source.

#### Syntax
```sql
ALTER SOURCE <source_name>
{ CLEAR PERMISSION CACHE | REFRESH STATUS }
```

To run `ALTER SOURCE`, you need the **MODIFY** privilege on the source.

#### Parameters

- **`<source_name>`**  
  Name of the source to alter.

- **`CLEAR PERMISSION CACHE`**  
  - Clears the AWS Lake Formation permission cache.  
  - Applies only to AWS Glue Data Catalog sources.  
  - Dremio caches Lake Formation permissions for one hour.  
  - Use this command after changing permissions in AWS Lake Formation to invalidate the cache immediately.

  **note:**  
  Any change to AWS Glue Data Catalog settings also clears the permission cache.

- **`REFRESH STATUS`**  
  Refreshes the status of the source.

#### Examples

#### Clear the Lake Formation permission cache
```sql
ALTER SOURCE glue1
CLEAR PERMISSION CACHE
```

#### Refresh status for an Amazon S3 source
```sql
ALTER SOURCE S3
REFRESH STATUS
```



### `ALTER TABLE`

Update a table’s definition or schema.

#### Syntax

```sql
ALTER TABLE <table_name>
{ ADD PRIMARY KEY ( <column_name> [ , ... ] )
| DROP PRIMARY KEY
| ADD COLUMNS ( <column_name> <data_type> [ NULL ] [ , ... ] )
| DROP COLUMN <column_name>
| { ALTER | MODIFY | CHANGE } COLUMN <old_name> <new_name> <data_type> [ { NULL | NOT NULL | DROP NOT NULL } ]
| MODIFY COLUMN <column_name> { SET MASKING POLICY <function_name> ( <column_name> [, ... ] ) | UNSET MASKING POLICY <function_name> }
| { ADD | DROP } ROW ACCESS POLICY <function_name> ( <column_name> [, ... ] )
| CLUSTER BY ( <column_name> [ , ... ] )
| DROP CLUSTERING KEY
| LOCALSORT BY ( <column_name> [ , ... ] )
| REFRESH METADATA [ IN <catalog_name> ] [ FOR PARTITIONS ( <partition_name> = '<value>') ] [ { AVOID | AUTO } PROMOTION ] [ { FORCE | LAZY } UPDATE ] [ { MAINTAIN | DELETE } WHEN MISSING ]
| FORGET METADATA
| SET TBLPROPERTIES ( '<property_name>' = '<property_value>' [ , ... ] )
| UNSET TBLPROPERTIES ( '<property_name>' [ , ... ] )
| CREATE AGGREGATE REFLECTION <reflection_name> USING { DIMENSIONS ( <column_name> [ , ... ] ) | MEASURES ( <column_name> ( <aggregation_type> ) [ , ... ] ) ) | DIMENSIONS ( <column_name> [ , ... ] ) MEASURES ( <column_name> ( <aggregation_type> ) [ , ... ] ) } [ PARTITION BY ( { <column_name> | <partition_transform> } [ , ... ] ) ] [ LOCALSORT BY ( <column_name> [ , ... ] ) ]
| CREATE EXTERNAL REFLECTION <reflection_name> USING <table_name>
| CREATE RAW REFLECTION <reflection_name> USING DISPLAY ( <column_name> [ , ... ] ) [ PARTITION BY ( { <column_name> | <partition_transform> } [ , ... ] ) ] [ LOCALSORT BY ( <column_name> [ , ... ] ) ]
| DROP REFLECTION <reflection_name>
| REFRESH REFLECTIONS
| ROUTE REFLECTIONS TO { DEFAULT ENGINE | ENGINE { <engine_name> | <engine_uuid> } }
| { ADD | DROP } PARTITION FIELD { <column_name> | <partition_transform> }
}
```

#### Parameters

- **`<table_name>`**  
  The name of the table that you want to alter.

- **`ADD PRIMARY KEY ( <column_name> [ , ... ] )`**  
  Specifies to use one or more existing columns as the primary key of a table. Primary keys provide hints to the query planning during join planning. They can be added to Apache Iceberg tables only. Uniqueness of the values in a primary key is not enforced.

- **`DROP PRIMARY KEY`**  
  Removes a table's primary key. The columns that make up the primary key remain in the table.

- **`ADD COLUMNS ( <column_name> <data_type> [ NULL ] [ , ... ] )`**  
  Creates one or more columns that have the specified names, data types, character limits, and nullability properties.
  
  Supported primitive types: `BOOLEAN`, `VARBINARY`, `DATE`, `FLOAT`, `DECIMAL`, `DOUBLE`, `INTERVAL`, `INT`, `BIGINT`, `TIME`, `TIMESTAMP`, `VARCHAR`.
  
  Complex types syntax:
  - `ROW( name primitive_or_complex_type, .. )`
  - `ARRAY(primitive_or_complex_type)`
  - `STRUCT <name : primitive_or_complex_type, ... >`
  - `{ LIST | ARRAY } < primitive_or_complex_type >`

  Use `NULL` to allow NULL values (default). You cannot add a `NOT NULL` column to an existing table.

- **`DROP COLUMN <column_name>`**  
  Drops the specified column. This action cannot be undone.

- **`{ ALTER | MODIFY | CHANGE } COLUMN <old_column_name> <new_column_name> <data_type>`**  
  Changes the data type for a column, and gives you the option to rename the column. Renaming is supported except for Parquet, JSON, or BSON.
  
  Allowed primitive type changes:
  - `INT` to `BIGINT`
  - `FLOAT` to `DOUBLE`
  - `DECIMAL(p, s)` to `DECIMAL(p', s)` (widening precision)

- **`[ { NULL | NOT NULL | DROP NOT NULL } ]`**  
  - `NULL`: Allow NULL values.
  - `NOT NULL`: Prevent NULL values.
  - `DROP NOT NULL`: Change from preventing NULLs to allowing them.

- **`MODIFY COLUMN <column_name> { SET | UNSET } MASKING POLICY`**  
  Sets or unsets a masking policy on a column. (Enterprise only)

- **`{ ADD | DROP } ROW ACCESS POLICY`**  
  Adds or removes a row-access policy. (Enterprise only)

- **`CLUSTER BY ( <column_name> [ , ... ] )`**  
  Columns to cluster the table by. Future `OPTIMIZE TABLE` commands will follow this scheme. (Enterprise only)

- **`DROP CLUSTERING KEY`**  
  Removes clustering keys.

- **`LOCALSORT BY ( <column_name> [ , ... ] )`**  
  Columns to sort new data by.

- **`REFRESH METADATA`**  
  Refreshes table metadata.
  - `FOR PARTITIONS ( <partition_name> = '<value>' )`: Partial refresh.
  - `{ AVOID | AUTO } PROMOTION`: Handle file promotion.
  - `{ FORCE | LAZY } UPDATE`: Force full update or lazy update.
  - `{ MAINTAIN | DELETE } WHEN MISSING`: Handle missing metadata.

- **`FORGET METADATA`**  
  Deletes metadata until next refresh.

- **`SET TBLPROPERTIES`**  
  Sets table properties (e.g., for Iceberg).

- **`UNSET TBLPROPERTIES`**  
  Removes table properties.

- **`CREATE AGGREGATE REFLECTION`**  
  Creates an aggregation reflection.
  - `DIMENSIONS`: Columns for dimensions.
  - `MEASURES`: Columns for measures and aggregation types (`COUNT`, `MIN`, `MAX`, `SUM`, `APPROXIMATE COUNT DISTINCT`).
  - `PARTITION BY`: Horizontal partitioning.
  - `LOCALSORT BY`: Sort order.

- **`CREATE EXTERNAL REFLECTION`**  
  Creates an external reflection using a derived table.

- **`CREATE RAW REFLECTION`**  
  Creates a raw reflection.
  - `USING DISPLAY`: Columns to include.

- **`DROP REFLECTION`**  
  Drops a reflection.

- **`REFRESH REFLECTIONS`**  
  Triggers reflection refresh.

- **`ROUTE REFLECTIONS TO`**  
  Specifies engine for reflection jobs.

- **`{ ADD | DROP } PARTITION FIELD`**  
  Adds or drops partition fields (Iceberg only).
  Transforms: `identity`, `year`, `month`, `day`, `hour`, `bucket`, `truncate`.

#### Examples

##### Add a primary key
```sql
ALTER TABLE services ADD PRIMARY KEY (Country_ID);
```

##### Add columns
```sql
ALTER TABLE services ADD COLUMNS (county varchar);
```

##### Modify column type
```sql
ALTER TABLE services MODIFY COLUMN tip_amount tip_amount DECIMAL;
```

##### Modify struct column
```sql
ALTER TABLE struct_type MODIFY COLUMN a a struct<x: varchar, y: bigint>;
```

##### Rename and modify column
```sql
ALTER TABLE services MODIFY COLUMN tip_amount gratuity_amount DECIMAL;
```

##### Change column nullability
```sql
ALTER TABLE age_table CHANGE age age INT DROP NOT NULL;
```

##### Add multiple columns
```sql
ALTER TABLE my_table ADD COLUMNS ( email VARCHAR NULL, date_of_birth DATE );
```

##### Refresh metadata
```sql
ALTER TABLE services REFRESH METADATA;
```

##### Refresh metadata with options
```sql
ALTER TABLE services REFRESH METADATA AUTO PROMOTION LAZY UPDATE MAINTAIN WHEN MISSING;
```

##### Partial metadata refresh
```sql
ALTER TABLE Samples."samples.dremio.com"."zips.json" REFRESH METADATA FOR PARTITIONS (state = 'TX');
```

##### Forget metadata
```sql
ALTER TABLE Samples."samples.dremio.com"."zips.json" FORGET METADATA;
```

##### Create raw reflection
```sql
ALTER TABLE Sales."customers" CREATE RAW REFLECTION customers_by_country USING DISPLAY (id,lastName,firstName,address,country) PARTITION BY (country) LOCALSORT BY (lastName);
```

##### Create aggregate reflection
```sql
ALTER TABLE Samples."samples.dremio.com"."zips.json" CREATE AGGREGATE REFLECTION per_state USING DIMENSIONS (state) MEASURES (city (COUNT)) LOCALSORT BY (state);
```

##### Route reflections
```sql
ALTER TABLE "Table 1" ROUTE REFLECTIONS TO ENGINE "Engine 1";
```

##### Cluster by
```sql
ALTER TABLE clustered_table CLUSTER BY (Col_one, Col_two, Col_three);
```

##### Drop clustering key
```sql
ALTER TABLE clustered_table DROP CLUSTERING KEY;
```


### `ALTER VIEW`

Change an existing view.

#### Syntax

```sql
ALTER VIEW <view_name>
{ REFRESH METADATA [ FOR PARTITIONS ( <partition_name> = '<value>') ] [ { AVOID | AUTO } PROMOTION ] [ { FORCE | LAZY } UPDATE ] [ { MAINTAIN | DELETE } WHEN MISSING ]
| CREATE EXTERNAL REFLECTION <reflection_name> USING <view_name>
| CREATE AGGREGATE REFLECTION <reflection_name> USING { DIMENSIONS ( <column_name1>, <column_name2>, ... ) | MEASURES ( <column_name1> ( <aggregation_type>, <column_name2> <aggregation_type> , ... ) ) | DIMENSIONS ( <column_name1>, <column_name2>, ... ) MEASURES ( <column_name1> ( <aggregation_type>, <column_name2> <aggregation_type> , ... ) ) } [ PARTITION BY ( <column_name1>, <column_name2>, ... ) ] [ LOCALSORT BY ( <column_name1>, <column_name2>, ... ) ]
| CREATE RAW REFLECTION <reflection_name> USING DISPLAY ( <column_name1>, <column_name2>, ...) [ PARTITION BY ( <column_name1>, <column_name2>, ... ) ] [ LOCALSORT BY ( <column_name1>, <column_name2>, ... ) ]
| DROP REFLECTION <reflection_name>
| REFRESH REFLECTIONS
| ROUTE REFLECTIONS TO { DEFAULT ENGINE | ENGINE { <engine_name> | <engine_uuid> } }
}
```

#### Parameters

- **`<view_name>`**  
  The name of the view that you want to alter.

- **`REFRESH METADATA`**  
  Refreshes metadata (Iceberg REST Catalog sources only).
  - `FOR PARTITIONS ( <partition_name> = '<value>' )`: Partial refresh.
  - `{ AVOID | AUTO } PROMOTION`: Handle file promotion.
  - `{ FORCE | LAZY } UPDATE`: Force full update or lazy update.
  - `{ MAINTAIN | DELETE } WHEN MISSING`: Handle missing metadata.

- **`CREATE EXTERNAL REFLECTION`**  
  Creates an external reflection.

- **`CREATE AGGREGATE REFLECTION`**  
  Creates an aggregate reflection.

- **`CREATE RAW REFLECTION`**  
  Creates a raw reflection.

- **`DROP REFLECTION`**  
  Drops a reflection.

- **`REFRESH REFLECTIONS`**  
  Triggers reflection refresh.

- **`ROUTE REFLECTIONS TO`**  
  Specifies engine for reflection jobs.

#### Examples

##### Create raw reflection on view
```sql
ALTER VIEW Sales."customers" CREATE RAW REFLECTION customers_by_country USING DISPLAY (id,lastName,firstName,address,country) PARTITION BY (country) LOCALSORT BY (lastName);
```

##### Create aggregate reflection on view
```sql
ALTER VIEW Samples."samples.dremio.com"."zips.json" CREATE AGGREGATE REFLECTION per_state USING DIMENSIONS (state) MEASURES (city (COUNT)) LOCALSORT BY (state);
```

##### Route reflections
```sql
ALTER VIEW "View 1" ROUTE REFLECTIONS TO ENGINE "Engine 1";
```

### `ANALYZE TABLE`

Compute and delete statistics for tables, including estimated number of distinct values, number of rows, and number of null values.

#### Syntax

```sql
ANALYZE TABLE <table_name> FOR { ALL COLUMNS | COLUMNS ( <column_name1>, <column_name2>, ... ) } { COMPUTE | DELETE } STATISTICS
```

#### Parameters

- **`<table_name>`**  
  The path to the table.

- **`FOR { ALL COLUMNS | COLUMNS (...) }`**  
  Specify columns to analyze.

- **`{ COMPUTE | DELETE } STATISTICS`**  
  Compute or delete statistics.

#### Examples

##### Compute statistics for all columns
```sql
ANALYZE TABLE Samples."samples.dremio.com"."NYC-taxi-trips" FOR ALL COLUMNS COMPUTE STATISTICS
```

##### Compute statistics for specific columns
```sql
ANALYZE TABLE Samples."samples.dremio.com"."NYC-taxi-trips" FOR COLUMNS (fare_amount, tip_amount) COMPUTE STATISTICS
```


### `COPY INTO`

Load data from CSV, JSON, or Parquet files into an existing Apache Iceberg table.

#### Syntax

```sql
COPY INTO <table_name>
FROM '@<storage_location_name>[/<path>[/<file_name>] ]'
[ FILES ( '<file_name>' [ , ... ] ) | REGEX '<regex_pattern>' ]
[ FILE_FORMAT 'csv' | 'json' | 'parquet' ]
[ ( [csv_format_options] | [json_format_options] | [parquet_format_options] ) ]
```

#### Parameters

- **`<table_name>`**  
  The target table.

- **`FROM '@<storage_location_name>...'`**  
  Source location. Can be a directory or specific file.

- **`FILES ( '<file_name>' ... )`**  
  List of specific files to load.

- **`REGEX '<regex_pattern>'`**  
  Regex pattern to match files.

- **`FILE_FORMAT`**  
  `csv`, `json`, or `parquet`.

#### Format Options

**CSV Options:**
- `DATE_FORMAT`: Date format string.
- `EMPTY_AS_NULL`: Treat empty strings as NULL (default TRUE).
- `ESCAPE_CHAR`: Escape character (default `"`).
- `EXTRACT_HEADER`: First line is header (default TRUE).
- `FIELD_DELIMITER`: Field separator (default `,`).
- `NULL_IF`: Strings to replace with NULL.
- `ON_ERROR`: `abort` (default), `continue`, or `skip_file`.
- `QUOTE_CHAR`: Quote character (default `"`).
- `RECORD_DELIMITER`: Record separator (default `\r\n`).
- `SKIP_LINES`: Number of lines to skip.
- `TIME_FORMAT`: Time format string.
- `TIMESTAMP_FORMAT`: Timestamp format string.
- `TRIM_SPACE`: Trim whitespace (default FALSE).

**JSON Options:**
- `DATE_FORMAT`
- `EMPTY_AS_NULL`
- `NULL_IF`
- `ON_ERROR`
- `TIME_FORMAT`
- `TIMESTAMP_FORMAT`
- `TRIM_SPACE`

**Parquet Options:**
- `ON_ERROR`: `abort` or `skip_file`.

#### Examples

##### Copy from specific file
```sql
COPY INTO context.myTable FROM '@SOURCE/bucket/path/folder' FILES ('fileName.csv') (ON_ERROR 'continue')
```

##### Copy JSON files
```sql
COPY INTO context.MyTable FROM '@SOURCE/bucket/path/folder/' FILE_FORMAT 'json'
```

##### Copy using Regex
```sql
COPY INTO context.myTable FROM '@SOURCE/bucket/path/folder' REGEX '.*.csv'
```

##### Copy with CSV options
```sql
COPY INTO context.myTable FROM '@SOURCE/bucket/path/folder' FILE_FORMAT 'csv' (RECORD_DELIMITER '\n', FIELD_DELIMITER '\t')
```

### `CREATE FOLDER`

Create a new folder in your catalog.

#### Syntax

```sql
CREATE FOLDER [ IF NOT EXISTS ] <folder_name>
```

#### Parameters

- **`IF NOT EXISTS`**  
  Prevent error if folder exists.

- **`<folder_name>`**  
  Name of the folder. Cannot include `/`, `:`, `[`, `]`.

#### Examples

##### Create folder
```sql
CREATE FOLDER myFolder
```

##### Create if not exists
```sql
CREATE FOLDER IF NOT EXISTS myFolder
```


### `CREATE FUNCTION`

Creates user-defined functions (UDFs) in the catalog.

#### Syntax

```sql
CREATE [ OR REPLACE ] FUNCTION [ IF NOT EXISTS ] <function_name> ( [ <function_parameter> [, ...] ] )
RETURNS { <data_type> | TABLE ( <column_name> [, ...] ) }
RETURN { <expression> | <query> }
```

#### Parameters

- **`OR REPLACE`**  
  Replaces existing UDF. Cannot use with `IF NOT EXISTS`.

- **`IF NOT EXISTS`**  
  Creates only if it doesn't exist. Cannot use with `OR REPLACE`.

- **`<function_name>`**  
  Name of the UDF.

- **`<function_parameter>`**  
  `parameter_name` and `data_type`.

- **`RETURNS <data_type>`**  
  Return type for scalar function.

- **`RETURNS TABLE ( <column_name> [, ...] )`**  
  Return signature for tabular function.

- **`RETURN { <expression> | <query> }`**  
  Body of the UDF. Expression for scalar, query for tabular.

#### Examples

##### Scalar function
```sql
CREATE FUNCTION area (x DOUBLE, y DOUBLE) RETURNS DOUBLE RETURN x * y;
```

##### Tabular function
```sql
CREATE FUNCTION all_fruits() RETURNS TABLE (name VARCHAR, hue VARCHAR) RETURN SELECT * FROM <catalog-name>.t2;
```

### `CREATE PIPE`

Create a pipe object that automatically ingests files from a cloud storage location.

#### Syntax

```sql
CREATE PIPE [ IF NOT EXISTS ] <pipe_name>
[ DEDUPE_LOOKBACK_PERIOD <number_of_days> ]
AS COPY INTO <table_name>
FROM '@<storage_location_name>[ /<folder_name> ]'
[ FILE_FORMAT 'csv' | 'json' | 'parquet']
[ ( [csv_format_options] | [json_format_options] | [parquet_format_options] ) ]
```

#### Parameters

- **`IF NOT EXISTS`**  
  Prevent error if pipe exists.

- **`<pipe_name>`**  
  Unique name of the pipe.

- **`DEDUPE_LOOKBACK_PERIOD <days>`**  
  Days to check for duplicates (0-90, default 14).

- **`AS COPY INTO <table_name>`**  
  Target Iceberg table.

- **`FROM '@<storage_location_name>...'`**  
  Source location (Amazon S3 only).

- **`FILE_FORMAT`**  
  `csv`, `json`, or `parquet`.

#### Examples

##### Create pipe
```sql
CREATE PIPE Example_pipe AS COPY INTO Pipe_sink FROM '@<storage_location_name>/folder' FILE_FORMAT 'csv'
```

##### Create pipe with dedupe lookback
```sql
CREATE PIPE Example_pipe DEDUPE_LOOKBACK_PERIOD 5 AS COPY INTO Table_one FROM '@<storage_location_name>/files' FILE_FORMAT 'csv'
```

### `CREATE ROLE`

Create a new role.

#### Syntax

```sql
CREATE ROLE <role_name>
```

#### Parameters

- **`<role_name>`**  
  Name of the new role.

#### Example

```sql
CREATE ROLE role1
```


### `CREATE TABLE`

Create a new table.

#### Syntax

```sql
CREATE TABLE [ IF NOT EXISTS ] <table_name>
( <column_name> <data_type> [ { NULL | NOT NULL } ] [ , ... ] )
[ MASKING POLICY <function_name> ( <column_name> [ , ... ] ) ]
[ ROW ACCESS POLICY <function_name> ( <column_name> [ , ... ] ) ]
[ PARTITION BY ( { <column_name> | <partition_transform> } [ , ... ] ) ]
[ CLUSTER BY ( <column_name> [ , ... ] ) ]
[ LOCALSORT BY ( <column_name> [ , ... ] ) ]
[ TBLPROPERTIES ( '<property_name>' = '<property_value>' [ , ... ] ) ]
```

#### Parameters

- **`IF NOT EXISTS`**  
  Prevent error if table exists.

- **`<table_name>`**  
  Name of the table.

- **`( <column_name> <data_type> ... )`**  
  Column definitions.
  - Primitive types: `BOOLEAN`, `VARBINARY`, `DATE`, `FLOAT`, `DECIMAL`, `DOUBLE`, `INTERVAL`, `INT`, `BIGINT`, `TIME`, `TIMESTAMP`, `VARCHAR`.
  - Complex types: `ROW`, `ARRAY`, `STRUCT`, `LIST`.
  - Nullability: `NULL` (default) or `NOT NULL`.

- **`MASKING POLICY`**  
  Set masking policy (Enterprise).

- **`ROW ACCESS POLICY`**  
  Set row access policy (Enterprise).

- **`PARTITION BY`**  
  Partition columns or transforms (`identity`, `year`, `month`, `day`, `hour`, `bucket`, `truncate`).

- **`CLUSTER BY`**  
  Cluster columns (Enterprise).

- **`LOCALSORT BY`**  
  Sort columns within files.

- **`TBLPROPERTIES`**  
  Table properties (Iceberg).

#### Examples

##### Create table with columns
```sql
CREATE TABLE employees (PersonID int, LastName varchar, FirstName varchar, Address varchar, City varchar)
```

##### Create table with partitions
```sql
CREATE TABLE myTable (col1 int, col2 date) PARTITION BY (month(col2))
```

##### Create table with complex types
```sql
CREATE TABLE my_table (name VARCHAR NOT NULL, age INT NULL, address STRUCT<street VARCHAR, zip INT NOT NULL, city VARCHAR NOT NULL>);
```

### `CREATE TABLE AS`

Create a new table as a select statement from another table.

#### Syntax

```sql
CREATE TABLE [ IF NOT EXISTS ] <table_name>
[ ( <column_name> <data_type> [ { NULL | NOT NULL } ] [ , ... ] ) ]
[ PARTITION BY ( { <column_name> | <partition_transform> } [ , ... ] )
[ CLUSTER BY ( <column_name> [ , ... ] ) ]
[ LOCALSORT BY ( <column_name> [ , ... ] ) ]
[ TBLPROPERTIES ( '<property_name>' = '<property_value>' [ , ... ] ) ]
AS <select_statement>
```

#### Parameters

- **`IF NOT EXISTS`**  
  Prevent error if table exists.

- **`<table_name>`**  
  Name of the table.

- **`( <column_name> <data_type> ... )`**  
  Optional column definitions to override source.

- **`PARTITION BY`**  
  Partition columns or transforms.

- **`CLUSTER BY`**  
  Cluster columns (Enterprise).

- **`LOCALSORT BY`**  
  Sort columns.

- **`TBLPROPERTIES`**  
  Table properties.

- **`AS <select_statement>`**  
  Query to populate the table.

#### Examples

##### Create table from select
```sql
CREATE TABLE demo_table AS SELECT * FROM Samples."samples.dremio.com"."zips.json"
```

##### Create table with partition and sort
```sql
CREATE TABLE demo_table2 PARTITION BY (state) LOCALSORT BY (city) AS SELECT * FROM Samples."samples.dremio.com"."zips.json"
```

##### Create table from time travel query
```sql
CREATE TABLE demo.example_table AS SELECT * FROM "oracle_tpch".DREMIO.JOBS AT TAG Jan2020
```

### `CREATE USER`

Create a new user.

#### Syntax

```sql
CREATE USER <username>
```

#### Parameters

- **`<username>`**  
  Email of the user (in double quotes).

#### Example

```sql
CREATE USER "user@dremio.com"
```


### `CREATE VIEW`

Create or replace a view.

#### Syntax

```sql
CREATE [ OR REPLACE ] VIEW <view_name> AS <select_statement>
```

#### Parameters

- **`OR REPLACE`**  
  Replaces existing view.

- **`<view_name>`**  
  Name of the view.

- **`AS <select_statement>`**  
  Query to populate the view.

#### Examples

##### Create view
```sql
CREATE VIEW demo.example_view AS SELECT * FROM "oracle_tpch".DREMIO.JOBS
```

##### Replace view
```sql
CREATE OR REPLACE VIEW demo.example_view AS SELECT * FROM "oracle_tpch".DREMIO.INVENTORY
```

### `DESCRIBE FUNCTION`

Returns the metadata about an existing user-defined function (UDF).

#### Syntax

```sql
{ DESC | DESCRIBE } FUNCTION <function_name>
```

#### Parameters

- **`<function_name>`**  
  Name of the UDF.

#### Examples

```sql
DESCRIBE FUNCTION hello
```

### `DESCRIBE PIPE`

Get high-level information about the settings and configuration of a specific autoingest pipe.

#### Syntax

```sql
DESCRIBE PIPE <pipe_name>
```

#### Parameters

- **`<pipe_name>`**  
  Name of the pipe.

#### Examples

```sql
DESCRIBE PIPE Example_pipe
```


### `DESCRIBE TABLE`

Provide high-level information regarding the overall column properties of an existing dataset.

#### Syntax

```sql
DESCRIBE TABLE <table_name>
```

#### Parameters

- **`<table_name>`**  
  Name of the table.

#### Example

```sql
DESCRIBE TABLE taxistats
```

### `DROP FOLDER`

Remove a folder from a catalog.

#### Syntax

```sql
DROP FOLDER [ IF EXISTS ] <folder_name> [ .<child_folder_name> ]
```

#### Parameters

- **`IF EXISTS`**  
  Prevent error if folder doesn't exist.

- **`<folder_name>`**  
  Name of the folder.

#### Examples

##### Drop folder
```sql
DROP FOLDER myFolder
```

##### Drop child folder
```sql
DROP FOLDER myFolder.resources
```

### `DROP FUNCTION`

Drops a user-defined function (UDF) in the catalog.

#### Syntax

```sql
DROP FUNCTION [ IF EXISTS ] <function_name> [ AS OF <timestamp> ]
```

#### Parameters

- **`IF EXISTS`**  
  Prevent error if function doesn't exist.

- **`<function_name>`**  
  Name of the UDF.

#### Examples

##### Drop function
```sql
DROP FUNCTION hello
```

##### Drop if exists
```sql
DROP FUNCTION IF EXISTS hello
```


### `DROP PIPE`

Removes the specified pipe from a source.

#### Syntax

```sql
DROP PIPE <pipe_name>
```

#### Parameters

- **`<pipe_name>`**  
  Name of the pipe.

#### Examples

```sql
DROP PIPE Example_pipe
```

### `DROP ROLE`

Removes a role.

#### Syntax

```sql
DROP ROLE <role_name>
```

#### Parameters

- **`<role_name>`**  
  Name of the role.

#### Examples

```sql
DROP ROLE role1
```

### `DROP TABLE`

Removes a table from your data source.

#### Syntax

```sql
DROP TABLE [ IF EXISTS ] <table_name>
```

#### Parameters

- **`IF EXISTS`**  
  Prevent error if table doesn't exist.

- **`<table_name>`**  
  Name of the table.

#### Example

```sql
DROP TABLE demo.example_table
```


### `DROP USER`

Removes a user.

#### Syntax

```sql
DROP USER <username>
```

#### Parameters

- **`<username>`**  
  Email of the user (in double quotes).

#### Example

```sql
DROP USER "user@dremio.com"
```

### `DROP VIEW`

Removes a view.

#### Syntax

```sql
DROP VIEW [ IF EXISTS ] <view_name>
```

#### Parameters

- **`IF EXISTS`**  
  Prevent error if view doesn't exist.

- **`<view_name>`**  
  Name of the view.

#### Examples

```sql
DROP VIEW demo.example_view
```

### `GRANT ROLE`

Grant a role to a user or a role.

#### Syntax

```sql
GRANT ROLE <role_name> TO { ROLE | USER } <role_or_user_name>
```

#### Parameters

- **`<role_name>`**  
  Name of the role to grant.

- **`TO { ROLE | USER } <role_or_user_name>`**  
  Recipient role or user.

#### Examples

##### Grant role to user
```sql
GRANT ROLE role1 TO USER "user@dremio.com"
```

##### Grant role to role
```sql
GRANT ROLE subrole TO ROLE role1
```


### `GRANT TO ROLE`

Grant privileges to a role.

#### Syntax

```sql
GRANT { <objectPrivilege> | ALL } ON { <object_type> <object_name> } TO ROLE <role_name>
```

#### Parameters

- **`<objectPrivilege>`**  
  Privilege to grant (e.g., `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `ALTER`, `DROP`, `OWNERSHIP`).

- **`<object_type>`**  
  Type of object (e.g., `PROJECT`, `SOURCE`, `TABLE`, `VIEW`, `FOLDER`).

- **`<object_name>`**  
  Name of the object.

- **`<role_name>`**  
  Name of the role.

#### Examples

##### Grant create project
```sql
GRANT CREATE PROJECT, CREATE CLOUD ON ORG TO ROLE "DATA_ENGINEER"
```

##### Grant select on table
```sql
GRANT SELECT ON TABLE myTable TO ROLE "DATA_ENGINEER"
```

### `GRANT TO USER`

Grant privileges to a user.

#### Syntax

```sql
GRANT { <objectPrivilege> | ALL } ON { <object_type> <object_name> } TO USER <username>
```

#### Parameters

- **`<objectPrivilege>`**  
  Privilege to grant.

- **`<object_type>`**  
  Type of object.

- **`<object_name>`**  
  Name of the object.

- **`<username>`**  
  Email of the user.

#### Examples

##### Grant select on project
```sql
GRANT SELECT ON PROJECT TO USER "user@dremio.com"
```

##### Grant ownership on catalog
```sql
GRANT OWNERSHIP ON CATALOG prodCatalog TO USER "user@dremio.com"
```

### `RESET ENGINE`

Clears any session-specific execution engine set using the SET ENGINE command.

#### Syntax

```sql
RESET ENGINE
```

#### Examples

```sql
RESET ENGINE;
```


### `REVOKE FROM ROLE`

Revoke privileges from a role.

#### Syntax

```sql
REVOKE { <objectPrivilege> | ALL } ON { <object_type> <object_name> } FROM ROLE <role_name>
```

#### Parameters

- **`<objectPrivilege>`**  
  Privilege to revoke.

- **`<object_type>`**  
  Type of object.

- **`<object_name>`**  
  Name of the object.

- **`<role_name>`**  
  Name of the role.

#### Examples

##### Revoke modify from role
```sql
REVOKE MODIFY, MONITOR ON CLOUD "Default Cloud" FROM ROLE "DATA_ENGINEER"
```

##### Revoke ownership from role
```sql
REVOKE OWNERSHIP ON CATALOG prodCatalog FROM ROLE data_engineer
```

### `REVOKE FROM USER`

Revoke privileges from a user.

#### Syntax

```sql
REVOKE { <objectPrivilege> | ALL } ON { <object_type> <object_name> } FROM USER <username>
```

#### Parameters

- **`<objectPrivilege>`**  
  Privilege to revoke.

- **`<object_type>`**  
  Type of object.

- **`<object_name>`**  
  Name of the object.

- **`<username>`**  
  Email of the user.

#### Examples

##### Revoke select from user
```sql
REVOKE SELECT ON PROJECT FROM USER "user@dremio.com"
```

##### Revoke ownership from user
```sql
REVOKE OWNERSHIP ON CATALOG prodCatalog FROM USER "user@dremio.com"
```

### `REVOKE ROLE`

Revoke a role from the role or user.

#### Syntax

```sql
REVOKE ROLE <role_name> FROM { ROLE | USER } <role_or_user_name>
```

#### Parameters

- **`<role_name>`**  
  Name of the role to revoke.

- **`FROM { ROLE | USER } <role_or_user_name>`**  
  Role or user to revoke from.

#### Example

```sql
REVOKE ROLE role1 FROM USER "user@dremio.com"
```


### `SET ENGINE`

Specify the engine that will be used to execute subsequent queries in the current session.

#### Syntax

```sql
SET ENGINE <engine_name>
```

#### Parameters

- **`<engine_name>`**  
  Name of the engine.

#### Examples

```sql
SET ENGINE first_engine;
```

### `SET TAG`

Specify the routing tag that will be used to route subsequent queries in the current session.

#### Syntax

```sql
SET TAG <tag_name>
```

#### Parameters

- **`<tag_name>`**  
  Name of the routing tag.

#### Examples

```sql
SET TAG Dashboard;
```

### `SHOW CREATE TABLE`

Show the definition that creates the specified table.

#### Syntax

```sql
SHOW CREATE TABLE <table_name>
```

#### Parameters

- **`<table_name>`**  
  Name of the table.

#### Examples

```sql
SHOW CREATE TABLE "company_data".employees
```


### `SHOW CREATE VIEW`

Show the definition for a view.

#### Syntax

```sql
SHOW CREATE VIEW <view_name>
```

#### Parameters

- **`<view_name>`**  
  Name of the view.

#### Examples

```sql
SHOW CREATE VIEW "company_data".Locations."offices_by_region"
```

### `SHOW FUNCTIONS`

Returns the list of user-defined functions (UDFs).

#### Syntax

```sql
SHOW FUNCTIONS [ AS OF <timestamp> ] [ LIKE { <pattern> } ]
```

#### Parameters

- **`AS OF <timestamp>`**  
  Optional timestamp.

- **`LIKE { <pattern> }`**  
  Optional pattern to filter results.

#### Examples

##### Show all functions
```sql
SHOW FUNCTIONS;
```

##### Show functions matching pattern
```sql
SHOW FUNCTIONS LIKE 'hello';
```

### `SHOW TABLES`

Show all the tables that are available in a catalog.

#### Syntax

```sql
SHOW TABLES [ IN <catalog_name> ]
```

#### Parameters

- **`IN <catalog_name>`**  
  Optional catalog name.

#### Examples

##### Show tables
```sql
SHOW TABLES
```

##### Show tables in catalog
```sql
SHOW TABLES IN myCatalog
```


### `SHOW VIEWS`

Show all the views that are available in a catalog.

#### Syntax

```sql
SHOW VIEWS [ IN <catalog_name> ]
```

#### Parameters

- **`IN <catalog_name>`**  
  Optional catalog name.

#### Examples

##### Show views
```sql
SHOW VIEWS
```

##### Show views in catalog
```sql
SHOW VIEWS IN myCatalog
```

### `RESET TAG`

Clears any session-specific routing tag set using the SET TAG command.

#### Syntax

```sql
RESET TAG
```

#### Examples

```sql
RESET TAG;
```

### `VACUUM TABLE`

Remove older table snapshots and orphan files from Iceberg tables.

#### Syntax

```sql
VACUUM TABLE <table_name>
{ EXPIRE SNAPSHOTS [ older_than = <timestamp> ] [ retain_last = <count> ]
| REMOVE ORPHAN FILES [ older_than = <timestamp> ] [ location = <path> ] }
```

#### Parameters

- **`<table_name>`**  
  Name of the table.

- **`EXPIRE SNAPSHOTS`**  
  Remove old snapshots.
  - `older_than`: Timestamp limit (default: 5 days ago).
  - `retain_last`: Minimum snapshots to keep.

- **`REMOVE ORPHAN FILES`**  
  Remove files not in metadata.
  - `older_than`: Creation timestamp limit (default: 3 days ago).
  - `location`: Directory to search.

#### Examples

##### Expire snapshots
```sql
VACUUM TABLE my_table EXPIRE SNAPSHOTS older_than = '2023-01-01 00:00:00.000' retain_last = 5
```

##### Remove orphan files
```sql
VACUUM TABLE my_table REMOVE ORPHAN FILES older_than = '2023-01-01 00:00:00.000'
```


### `WITH`

Defines a common table expression (CTE), which is a temporary named result set.

#### Syntax

```sql
WITH <cte_name> [ ( <cte_column1>, <cte_column2>, ... ) ] AS ( <query> )
SELECT ...
```

#### Parameters

- **`<cte_name>`**  
  Name of the CTE.

- **`<cte_column>`**  
  Optional column names.

- **`AS ( <query> )`**  
  Query defining the CTE.

#### Examples

```sql
WITH cte_quantity (Total) AS ( SELECT SUM(passenger_count) as Total FROM Samples."samples.dremio.com"."NYC-taxi-trips" where passenger_count > 2 GROUP BY pickup_datetime )
SELECT AVG(Total) average_pass FROM cte_quantity
```

### `DELETE`

Delete rows from a table.

#### Syntax

```sql
DELETE FROM <table_name> [ AS <alias> ] [ USING <additional_table_or_query> ] [ WHERE <where_conditions> ]
```

#### Parameters

- **`<table_name>`**  
  Name of the table.

- **`USING <additional_table>`**  
  Additional tables for join conditions.

- **`WHERE <where_conditions>`**  
  Filter for rows to delete.

#### Examples

##### Delete with join
```sql
DELETE FROM orders USING returns WHERE orders.order_id = returns.order_id;
```

##### Delete with subquery
```sql
DELETE FROM orders WHERE EXISTS (select 1 from returns where order_id = orders.order_id)
```

### `INSERT`

Insert records into a table.

#### Syntax

```sql
INSERT INTO <table_name> [ ( <column_name> [ , ... ] ) ]
{ <select_statement> | VALUES ( <value> [ , ... ] ) [ , ... ] }
```

#### Parameters

- **`<table_name>`**  
  Name of the table.

- **`( <column_name> ... )`**  
  Optional column list.

- **`VALUES`**  
  List of values to insert.

#### Examples

##### Insert values
```sql
INSERT INTO myTable VALUES (21, 'Ruth Asawa'), (38, 'Magdalena Abakanowicz')
```

##### Insert from select
```sql
INSERT INTO struct_type VALUES (convert_from('{ x: "hi" }', 'json'))
```


### `MERGE`

Run insert or update operations on a target table from the results of a join with a source table.

#### Syntax

```sql
MERGE INTO <target_table> [ AS <target_alias> ]
USING <source_table> [ AS <source_alias> ]
ON ( <condition> )
[ WHEN MATCHED THEN UPDATE SET <column> = <value> [ , ... ] ]
[ WHEN NOT MATCHED THEN INSERT ( <column> [ , ... ] ) VALUES ( <value> [ , ... ] ) ]
```

#### Parameters

- **`<target_table>`**  
  Table to merge into.

- **`USING <source_table>`**  
  Source table for data.

- **`ON ( <condition> )`**  
  Join condition.

- **`WHEN MATCHED THEN UPDATE`**  
  Update existing rows.

- **`WHEN NOT MATCHED THEN INSERT`**  
  Insert new rows.

#### Examples

```sql
MERGE INTO target_table AS t USING source_table AS s ON (t.id = s.id)
WHEN MATCHED THEN UPDATE SET description = s.description_2
WHEN NOT MATCHED THEN INSERT (id, description) VALUES (s.id, s.description_1);
```

### `OPTIMIZE TABLE`

Rewrite data and manifest files to provide peak performance.

#### Syntax

```sql
OPTIMIZE TABLE <table_name>
[ REWRITE DATA [ USING BIN_PACK ]
  [ ( { TARGET_FILE_SIZE_MB | MIN_FILE_SIZE_MB | MAX_FILE_SIZE_MB | MIN_INPUT_FILES } = <value> [, ... ] ) ]
  [ FOR PARTITIONS <predicate> ] ]
[ REWRITE MANIFESTS ]
```

#### Parameters

- **`<table_name>`**  
  Name of the table.

- **`REWRITE DATA`**  
  Rewrite data files.
  - `TARGET_FILE_SIZE_MB`: Target size.
  - `MIN_INPUT_FILES`: Min files to trigger optimization.

- **`FOR PARTITIONS`**  
  Filter partitions to optimize.

- **`REWRITE MANIFESTS`**  
  Optimize manifest files.

#### Examples

##### Optimize data
```sql
OPTIMIZE TABLE demo.example_table REWRITE DATA USING BIN_PACK (TARGET_FILE_SIZE_MB=512, MIN_INPUT_FILES=10)
```

##### Optimize manifests
```sql
OPTIMIZE TABLE demo.example_table REWRITE MANIFESTS
```

### `ROLLBACK TABLE`

Roll back an Iceberg table to a previous snapshot.

#### Syntax

```sql
ROLLBACK TABLE <table_name> TO { SNAPSHOT '<snapshot_id>' | TIMESTAMP '<timestamp>' }
```

#### Parameters

- **`<table_name>`**  
  Name of the table.

- **`TO SNAPSHOT '<snapshot_id>'`**  
  Rollback to snapshot ID.

- **`TO TIMESTAMP '<timestamp>'`**  
  Rollback to timestamp.

#### Examples

##### Rollback to snapshot
```sql
ROLLBACK TABLE demo.example_table TO SNAPSHOT '2489484212521283189'
```

##### Rollback to timestamp
```sql
ROLLBACK TABLE demo.example_table TO TIMESTAMP '2022-06-22 17:06:00'
```


### `TRUNCATE`

Delete all rows from a table with minimal computation.

#### Syntax

```sql
TRUNCATE [ TABLE ] [ IF EXISTS ] <table_name>
```

#### Parameters

- **`TABLE`**  
  Optional keyword.

- **`IF EXISTS`**  
  Prevent error if table missing.

- **`<table_name>`**  
  Name of the table.

#### Examples

```sql
TRUNCATE TABLE IF EXISTS myTable
```

### `UPDATE`

Update rows in a table.

#### Syntax

```sql
UPDATE <table_name> [ AS <alias> ]
SET <column> = <value> [ , ... ]
[ WHERE <condition> ]
```

#### Parameters

- **`<table_name>`**  
  Name of the table.

- **`SET <column> = <value>`**  
  Columns to update.

- **`WHERE <condition>`**  
  Filter for rows to update.

#### Examples

```sql
UPDATE MYSOURCE.MYTABLE SET EXPR$0 = s.EXPR$1 FROM MYSOURCE.MYTABLE2 AS s
```

