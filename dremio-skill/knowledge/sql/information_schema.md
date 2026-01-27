## Information Schema

Dremio stores metadata for the objects in your project in the Information Schema, which is a set of system-generated read-only views.

### INFORMATION_SCHEMA.CATALOGS

Returns metadata for the catalogs.

**Fields:**

| Field | Data Type | Description |
| --- | --- | --- |
| CATALOG_NAME | nvarchar | The name of the catalog, which is always DREMIO. |
| CATALOG_DESCRIPTION | nvarchar | The description for the catalog that contains metadata. |
| CATALOG_CONNECT | nvarchar | The connection permissions to the catalog that contains metadata information. This is an inherited field and is always empty. |

### INFORMATION_SCHEMA.COLUMNS

Returns metadata for columns in tables and views.

**Fields:**

| Field | Data Type | Description |
| --- | --- | --- |
| TABLE_CATALOG | nvarchar | The name of the catalog, which is always DREMIO. |
| TABLE_SCHEMA | nvarchar | The path (source, space, folders) to the table or view. |
| TABLE_NAME | nvarchar | The name of the table or view that the column belongs to. |
| COLUMN_NAME | nvarchar | The name of the column in the table or view. |
| ORDINAL_POSITION | integer | This represents the position at which the column appears in the table or view. |
| COLUMN_DEFAULT | nvarchar | The default value of the column. |
| IS_NULLABLE | nvarchar | The value is YES if null values can be stored in the column and the value is NO if null values cannot be stored in the column. |
| DATA_TYPE | nvarchar | The system-defined data type of the column in the table or view. |
| COLUMN_SIZE | integer | The size of the table or view column in bytes. |
| CHARACTER_MAXIMUM_LENGTH | integer | The maximum length in characters for binary data, character data, or text and image data. |
| CHARACTER_OCTET_LENGTH | integer | The maximum length in bytes for binary data, character data, or text and image data. |
| NUMERIC_PRECISION | integer | The precision of approximate numeric data, exact numeric data, integer data, or monetary data. |
| NUMERIC_PRECISION_RADIX | integer | The precision radix of approximate numeric data, exact numeric data, integer data, or monetary data. |
| NUMERIC_SCALE | integer | The scale of approximate numeric data, exact numeric data, integer data, or monetary data. |
| DATETIME_PRECISION | integer | The supported precision for datetime and interval data types. |
| INTERVAL_TYPE | integer | If the data type is interval, then specified fields (year) are returned. |
| INTERVAL_PRECISION | integer | If the data type is interval, then the declared precision is displayed. |

### INFORMATION_SCHEMA.SCHEMATA

Returns metadata for schemas (folders/spaces).

**Fields:**

| Field | Data Type | Description |
| --- | --- | --- |
| CATALOG_NAME | nvarchar | Name of the catalog, which is always DREMIO. |
| SCHEMA_NAME | nvarchar | Path (source, space, folders) that contains datasets. |
| SCHEMA_OWNER | nvarchar | Owner of the schema. This is an inherited field and <owner> is always returned. |
| TYPE | nvarchar | Type of the schema, which is always SIMPLE. |
| IS_MUTABLE | nvarchar | The value in this column is YES if the schema can be modified. NO if it's immutable. |

### INFORMATION_SCHEMA."TABLES"

Returns metadata for tables and views.

**Fields:**

| Field | Data Type | Description |
| --- | --- | --- |
| TABLE_CATALOG | nvarchar | Name of the catalog, which is always DREMIO. |
| TABLE_SCHEMA | nvarchar | The path (source, space, folders) to the table or view. |
| TABLE_NAME | nvarchar | The name of the table or view. |
| TABLE_TYPE | nvarchar | The type of the object. Enum: `SYSTEM_TABLE`, `TABLE`, `VIEW` |

### INFORMATION_SCHEMA.VIEWS

Returns metadata for views.

**Fields:**

| Field | Data Type | Description |
| --- | --- | --- |
| TABLE_CATALOG | nvarchar | The name of the catalog, which is always DREMIO. |
| TABLE_SCHEMA | nvarchar | The path (source, space, folders) to the view. |
| TABLE_NAME | nvarchar | The name of the view. |
| VIEW_DEFINITION | nvarchar | The original SQL query (underlying DDL statement) used to define the view. |
