## Data Types

`Data Types`  
A data type classifies data and determines the operations allowed on it. Dremio supports numeric, string and binary, boolean, date and time, and semi-structured types.

The following topics are covered:  
`Coercions Support`: how types are coerced when source and table differ.  
`Summary of Supported Data Types in Dremio`.

`Numeric Data Types`

#### DECIMAL
    A DECIMAL type has precision (p) and scale (s): `DECIMAL(p,s)`. Precision is total digits. Scale is digits to the right of the decimal. Arithmetic between DECIMAL values adjusts precision and scale automatically.  
    Decimal limits:  
    - Decimal literals cannot exceed BIGINT max: `9223372036854775807`.  
    - Arithmetic with column + literal may fail. Example: `SELECT CAST(12345 as DOUBLE) * CAST(A as DOUBLE)` fails. Use a string literal instead.  
    - Casting numeric literals to DECIMAL requires explicit precision. Precision cannot be lowered.  
    - Decimal overflows return overflow values.  
    Example: `987.65` is a `DECIMAL(5,2)`.

#### INT  
    A 4-byte signed integer: -2147483648 to 2147483647.  
    Example: `5135`

#### BIGINT  
    An 8-byte signed integer: -9223372036854775808 to 9223372036854775807.  
    Example: `-749826542587`

#### FLOAT  
    4-byte single-precision float with six decimal digits.  
    Example: `123.123456`

#### DOUBLE  
    8-byte double-precision float with fifteen decimal digits.  
    Example: `123.123456789012345`

`String & Binary Data Types`

#### VARCHAR  
    Variable-length UTF-8 string.  
    Example: `18852367854`

#### VARBINARY  
    Variable-length binary string (up to 32,000 bytes).  
    Example:  
        - `SELECT CAST('help' AS VARBINARY)`
        - `-- aGVscA==`

`Boolean Data Type`

#### BOOLEAN  
    Supported values: `TRUE`, `FALSE`, `NULL`.

`Date & Time Data Types`

`note:` Dremio retrieves TIME and TIMESTAMP values as UTC without conversion.

#### DATE  
    Stores calendar dates.  
    `note:` String literal format must be `yyyy-mm-dd`.  
    Example: `DATE '2000-01-01'`

#### TIME  
    Stores time of day.  
    `note:` Supported formats: `HH24:MI:SS.sss` and `HH24:MI:SS`.  
    Examples:  
        - `TIME '17:30:50.235'`  
        - `TIME '17:30:50'`

#### TIMESTAMP  
    Represents an absolute moment with millisecond precision (no time zone).  
    Examples:  
        - `TIMESTAMP '2000-01-01 01:30:50'`  
        - `TIMESTAMP '2000-01-01 17:30:50.9'`  
        - `TIMESTAMP '2000-01-01 17:30:50.123'`

#### INTERVAL  
    Represents spans of time (year-month or day-time).  
    Supported forms include:  
    - `INTERVAL '3' DAY`  
    - `INTERVAL '3' MONTH`  
    - `INTERVAL '1' YEAR`  
    - `INTERVAL '5' MINUTE`  
    - `INTERVAL '4 01:01' DAY TO MINUTE`  
    Examples:  
        - `INTERVAL '1 2:34:56.789' DAY TO SECOND`  
        - `INTERVAL '1-5' YEAR TO MONTH`

`Semi-structured Data Types`

#### STRUCT  
    Represents key-value pairs. Keys are case-insensitive strings; values may be any type.  
    `note:` Use `CONVERT_FROM` with JSON strings to create STRUCT-like literals.  
    Example:  
        - `SELECT CONVERT_FROM('{"name":"Gnarly","age":7}', 'json')`  
        - `SELECT address['city'] FROM customerTable`

#### LIST  
    A list indexed by non-negative integers, values share one type.  
    `note:` LIST literals use `ARRAY`.  
    Example:  
        - `SELECT ARRAY[1,2,3]`  
        - `SELECT customerOrders[100] FROM OrderHistoryTable`
#### MAP  
    Key-value pairs where keys are case-insensitive strings and values share one type.  
    Syntax:  
        SELECT column_name['key'] FROM table_name  
    `note:`  
    - Run `ALTER TABLE ... FORGET METADATA` if MAP columns were previously read as STRUCT.  
    - MAP does not support null values.  
    Example:  
        - `SELECT address['city'] FROM customerTable`


