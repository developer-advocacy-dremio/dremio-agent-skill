## SQL Functions



















### ABS

Returns the absolute value of the argument.

#### Syntax

```sql
ABS(numeric_expression NUMERIC) → NUMERIC
```

#### Parameters

- `numeric_expression`: BINARY, DECIMAL, DOUBLE, FLOAT, INTEGER

#### Examples

```sql
SELECT ABS(0.0) -- 0.0
SELECT ABS(-2) -- 2
SELECT ABS(NULL) -- null
```

### ACOS

Returns the arc cosine of the argument.

#### Syntax

```sql
ACOS(numeric_expression NUMERIC) → FLOAT
```

#### Parameters

- `numeric_expression`: The number in radians. This must be DOUBLE, INTEGER, BIGINT, DECIMAL, or FLOAT.

#### Examples

```sql
SELECT ACOS(0) -- 1.5707963267948966
SELECT ACOS(1.0) -- 0.0
SELECT ACOS(-1) -- 3.141592653589793
```

### AES_DECRYPT

Decrypts a string using AES encryption.

#### Syntax

```sql
AES_DECRYPT(ciphertext varchar, key varchar) → varchar
```

#### Parameters

- `ciphertext`: The string to be decrypted.
- `key`: The key to use to decrypt the ciphertext. Must be 16, 24, or 32 characters.

#### Examples

```sql
SELECT AES_DECRYPT(UNBASE64('UvicDn/xiUDmfSE+KYjjyw=='), 'mypassword123456') -- Dremio
```

### AES_ENCRYPT

Encrypts a string using AES encryption.

#### Syntax

```sql
AES_ENCRYPT(plaintext varchar, key varchar) → varchar
```

#### Parameters

- `plaintext`: The string to be encrypted.
- `key`: The key to use to encrypt the plaintext. Must be 16, 24, or 32 characters.

#### Examples

```sql
SELECT BASE64(AES_ENCRYPT('Dremio', 'mypassword123456')) -- UvicDn/xiUDmfSE+KYjjyw==
```

### AI_CLASSIFY

Classifies text using a Large Language Model (LLM).

#### Syntax

```sql
AI_CLASSIFY( [model_name VARCHAR,] prompt VARCHAR | (prompt VARCHAR, file_reference), categories ARRAY<VARCHAR|INT|FLOAT|BOOLEAN> ) → VARCHAR|INT|FLOAT|BOOLEAN
```

#### Parameters

- `model_name` (optional): Optional model specification in format 'modelProvider.modelName' (e.g., 'gpt.4o').
- `prompt`: Classification instructions for the LLM. Use (prompt, file_reference) to process files from LIST_FILES.
- `categories`: Array of possible classifications. The LLM will choose one of these values as the result.

#### Examples

```sql
SELECT recipe_name, AI_CLASSIFY( 'Determine the difficulty level based on these ingredients and steps', ingredients || ' - Steps: ' || cooking_instructions, ARRAY['Beginner', 'Easy', 'Intermediate', 'Advanced', 'Expert'] ) AS difficulty_level, prep_time, number_of_ingredients FROM recipe_database;
```

### AI_COMPLETE

Generates text completion using a Large Language Model (LLM).

#### Syntax

```sql
AI_COMPLETE( [model_name VARCHAR,] prompt VARCHAR ) → VARCHAR
```

#### Parameters

- `model_name` (optional): Optional model specification in format 'modelProvider.modelName'.
- `prompt`: Completion instruction for the LLM. Natural language text describing what you want the model to generate.

#### Examples

```sql
SELECT dish_name, AI_COMPLETE( 'Write an appetizing menu description for this dish: ' || dish_name || '. Main ingredients: ' || main_ingredients || '. Cooking style: ' || cuisine_type ) AS menu_description FROM restaurant_dishes;
```

### AI_GENERATE

Generates structured data or text using a Large Language Model (LLM).

#### Syntax

```sql
AI_GENERATE( [model_name VARCHAR,] prompt VARCHAR | (prompt VARCHAR, file_reference) [WITH SCHEMA data_type] ) → ANY|ROW
```

#### Parameters

- `model_name` (optional): Optional model specification in format 'modelProvider.modelName'.
- `prompt`: Natural language instruction for the LLM. Use (prompt, file_reference) to process files from LIST_FILES.
- `WITH SCHEMA data_type`: Output structure specification (optional).

#### Examples

```sql
WITH recipe_analysis AS ( SELECT file['path'] AS recipe_file, AI_GENERATE( 'gpt.4o', ('Extract recipe details', file) WITH SCHEMA ROW( recipe_name VARCHAR, cuisine_type VARCHAR) ) AS recipe_info FROM TABLE(LIST_FILES('@Cookbooks/cookbook_recipes')) WHERE file['path'] LIKE '%.pdf' ) SELECT recipe_file, recipe_info['recipe_name'] AS recipe, recipe_info['cuisine_type'] AS cuisine FROM recipe_analysis ORDER BY recipe ASC;
```

### APPROX_COUNT_DISTINCT

Returns the approximate number of distinct values in a column.

#### Syntax

```sql
APPROX_COUNT_DISTINCT(column_name any primitive) → BIGINT
```

#### Parameters

- `column_name`: You can specify a column of any primitive data type.

#### Examples

```sql
SELECT APPROX_COUNT_DISTINCT(IncidntNum) FROM Samples."samples.dremio.com"."SF_incidents2016.json" -- 116696
```

### APPROX_PERCENTILE

Returns the approximate percentile of a column.

#### Syntax

```sql
APPROX_PERCENTILE(column_name numeric, percentile double) → DOUBLE
```

#### Parameters

- `column_name`: The column for which to compute the approximate percentile.
- `percentile`: The percentile to use in the approximation. Must be a number between 0 and 1.

#### Examples

```sql
SELECT APPROX_PERCENTILE(pop, 0.5) FROM Samples."samples.dremio.com"."zips.json" -- 2780.17855684608
```

### ARRAYS_OVERLAP

Checks if two arrays have any elements in common.

#### Syntax

```sql
ARRAYS_OVERLAP(arr1 LIST, arr2 LIST) → BOOLEAN
```

#### Parameters

- `arr1`: The first array.
- `arr2`: The second array.

#### Examples

```sql
SELECT ARRAYS_OVERLAP(ARRAY['foo', 'bar'], ARRAY['bar', 'baz']) -- true
SELECT ARRAYS_OVERLAP(ARRAY['foo', 'bar'], ARRAY['baz', 'qux']) -- false
```

### ARRAY_AGG

Aggregates values into an array.

#### Syntax

```sql
ARRAY_AGG ( [ DISTINCT ] expression ) → array
```

#### Parameters

- `expression`: An expression of any primitive type to aggregate into an array.

#### Examples

```sql
SELECT ARRAY_AGG(name) FROM <catalog-name>.people; -- ['Bob', 'Charlie', 'Alice']
```

### ARRAY_APPEND

Appends an element to an array.

#### Syntax

```sql
ARRAY_APPEND(array LIST, element ANY) → LIST
```

#### Parameters

- `array`: The array to append to.
- `element`: The element to append to the array.

#### Examples

```sql
SELECT ARRAY_APPEND(ARRAY[1, 2], 3); -- [1, 2, 3]
```

### ARRAY_AVG

Returns the average of the elements in an array.

#### Syntax

```sql
ARRAY_AVG(list_column LIST) → numeric
```

#### Parameters

- `list_column`: Column that contains a LIST expression. Every element of the list must be a number.

#### Examples

```sql
SELECT ARRAY_AVG(array_col) -- 2
```

### ARRAY_CAT

Concatenates two arrays.

#### Syntax

```sql
ARRAY_CAT(arr1 LIST, arr2 LIST) → list
```

#### Parameters

- `arr1`: The source array.
- `arr2`: The array to be appended to the source array.

#### Examples

```sql
SELECT ARRAY_CAT(ARRAY[1, 2, 3], ARRAY[4, 5, 6]) -- [1, 2, 3, 4, 5, 6]
```


### ARRAY_COMPACT

Removes null values from an array.

#### Syntax

```sql
ARRAY_COMPACT(arr LIST) → list
```

#### Parameters

- `arr`: The array from which to remove null values.

#### Examples

```sql
SELECT ARRAY_COMPACT(array_col) -- [1, 2]
```

### ARRAY_CONTAINS

Checks if an array contains a specific value.

#### Syntax

```sql
ARRAY_CONTAINS(list LIST, value any) → boolean
```

#### Parameters

- `list`: The list to search.
- `value`: An expression of a type that is comparable with the LIST.

#### Examples

```sql
SELECT ARRAY_CONTAINS(CONVERT_FROM('["apple", "pear", "banana"]', 'json'), NULL) -- null
SELECT ARRAY_CONTAINS(CONVERT_FROM('["apple", "pear", "banana"]', 'json'), 'pear') -- true
SELECT ARRAY_CONTAINS(CONVERT_FROM('["apple", "pear", "banana"]', 'json'), 'grape') -- false
```

### ARRAY_DISTINCT

Returns an array with distinct elements from the input array.

#### Syntax

```sql
ARRAY_DISTINCT(input LIST) → LIST
```

#### Parameters

- `input`: The input array from which to return only distinct elements.

#### Examples

```sql
SELECT ARRAY_DISTINCT(ARRAY[1, 2, 3, 1, 2, 3]) -- [2, 3, 1]
```

### ARRAY_FREQUENCY

Returns a map where keys are the elements of the array and values are their frequencies.

#### Syntax

```sql
ARRAY_FREQUENCY(array LIST) → MAP
```

#### Parameters

- `array`: The array of values for which to calculate frequency. Accepts primitive types.

#### Examples

```sql
SELECT ARRAY_FREQUENCY(ARRAY[2,1,2,1,1,5]); -- {"1":3, "2":2, "5":1}
SELECT ARRAY_FREQUENCY(ARRAY['a','b','ab','b','a']); -- {"a":2, "ab":1, "b":2}
SELECT ARRAY_FREQUENCY(ARRAY['foo', 'bar', 'FOO', 'foo']); -- {"FOO":1, "bar":1, "foo":2}
SELECT ARRAY_FREQUENCY(array_col); -- {"1":1, "2":2}
```

### ARRAY_GENERATE_RANGE

Generates an array of integers in a specified range.

#### Syntax

```sql
ARRAY_GENERATE_RANGE(start int32, stop int32, step int32) → list
```

#### Parameters

- `start`: The first number in the range of numbers to return.
- `stop`: The last number in the range. Note that this number is not included in the range of numbers returned.
- `step`: The amount to increment or decrement each subsequent number in the array. May be a positive or negative number. Cannot be 0. Default value is 1.

#### Examples

```sql
SELECT ARRAY_GENERATE_RANGE(1, 5) -- [1, 2, 3, 4]
SELECT ARRAY_GENERATE_RANGE(0, 16, 5) -- [0, 5, 10, 15]
SELECT ARRAY_GENERATE_RANGE(0, -16, -5) -- [0, -5, -10, -15]
SELECT ARRAY_GENERATE_RANGE(2, 2, 4) -- []
SELECT ARRAY_GENERATE_RANGE(8, 2, 2) -- []
SELECT ARRAY_GENERATE_RANGE(2, 8, -2) -- []
SELECT ARRAY_GENERATE_RANGE(2, 2) -- []
```

### ARRAY_INSERT

Inserts an element into an array at a specified position.

#### Syntax

```sql
ARRAY_INSERT(arr LIST, position INT, new_element ANY) → LIST
```

#### Parameters

- `arr`: The array to search.
- `position`: The zero-based position in the input array where the new element should be inserted.
- `new_element`: The new element to insert in the specified position.

#### Examples

```sql
SELECT ARRAY_INSERT(ARRAY[1, 2, 3, 4, 5], 2, 55); -- [1, 2, 55, 3, 4, 5]
SELECT ARRAY_INSERT(ARRAY[1, 2, 3], 6, 55); -- [1, 2, 3, NULL, NULL, NULL, 55]
SELECT ARRAY_INSERT(ARRAY[1, 2, 3], -1, 55); -- [1, 2, 55, 3]
```

### ARRAY_MAX

Returns the maximum value in an array.

#### Syntax

```sql
ARRAY_MAX(list_column LIST) → numeric
```

#### Parameters

- `list_column`: Column that contains a LIST expression. Every element of the list must be a number such as INT, BIGINT, FLOAT4, FLOAT8, or DECIMAL. Cannot be an array literal.

#### Examples

```sql
SELECT ARRAY_MAX(array_col) -- 3
SELECT ARRAY_MAX(array_col) -- NULL
```

### ARRAY_MIN

Returns the minimum value in an array.

#### Syntax

```sql
ARRAY_MIN(list_column LIST) → numeric
```

#### Parameters

- `list_column`: Column that contains a LIST expression. Every element of the list must be a number such as INT, BIGINT, FLOAT4, FLOAT8, or DECIMAL. Cannot be an array literal.

#### Examples

```sql
SELECT ARRAY_MIN(array_col) -- 1
SELECT ARRAY_MIN(array_col) -- NULL
```

### ARRAY_POSITION

Returns the position of the first occurrence of an element in an array.

#### Syntax

```sql
ARRAY_POSITION(element ANY, arr LIST) → numeric
```

#### Parameters

- `element`: Element to find in the array.
- `arr`: The array to search.

#### Examples

```sql
SELECT ARRAY_POSITION(CAST(3 AS BIGINT), ARRAY[1, 2, 3]) -- 2
SELECT ARRAY_POSITION(4, ARRAY[1, 2, 3]) -- NULL
SELECT ARRAY_POSITION(NULL, array_col) -- 1
SELECT ARRAY_POSITION(ARRAY[2,3], ARRAY[ARRAY[1,2], ARRAY[2,3]]) -- 1
```

### ARRAY_PREPEND

Prepends an element to the beginning of an array.

#### Syntax

```sql
ARRAY_PREPEND(element ANY, array LIST) → LIST
```

#### Parameters

- `element`: The element to prepend to the array.
- `array`: The array to prepend to.

#### Examples

```sql
SELECT ARRAY_PREPEND(1, ARRAY[2, 3]); -- [1, 2, 3]
```

### ARRAY_REMOVE

Removes all occurrences of a value from an array.

#### Syntax

```sql
ARRAY_REMOVE(list_column LIST, value any) → list
```

#### Parameters

- `list_column`: Column that contains a LIST expression. Cannot be an array literal.
- `value`: An expression of any data type.

#### Examples

```sql
SELECT ARRAY_REMOVE(array_col, 1) -- [2, 3]
SELECT ARRAY_REMOVE(array_col, 2) -- [1,null]
SELECT ARRAY_REMOVE(array_col, null) -- NULL
SELECT ARRAY_REMOVE(array_col, 2) -- NULL
SELECT ARRAY_REMOVE(null, 2) -- NULL
```

### ARRAY_REMOVE_AT

Removes the element at a specified position from an array.

#### Syntax

```sql
ARRAY_REMOVE_AT(arr LIST, position int32) → list
```

#### Parameters

- `arr`: Array from which to remove the element at the specified position.
- `position`: The zero-based position of the element to be removed. The function removes the element at the specified position. A negative position is interpreted as an index from the back of the array. For example, the value -1 removes the last element in the array.

#### Examples

```sql
SELECT ARRAY_REMOVE_AT(ARRAY[1, 2, 3], 1) -- [1, 3]
SELECT ARRAY_REMOVE_AT(ARRAY[1, 2, 3], -1) -- [1, 2]
SELECT ARRAY_REMOVE_AT(ARRAY[1, 2, 3], 10) -- [1, 2, 3]
```

### ARRAY_SIZE

Returns the number of elements in an array.

#### Syntax

```sql
ARRAY_SIZE(arr LIST) → numeric
```

#### Parameters

- `arr`: The source array.

#### Examples

```sql
SELECT ARRAY_SIZE(ARRAY[1, 4, 5]) -- 3
```

### ARRAY_SLICE

Returns a subset of an array.

#### Syntax

```sql
ARRAY_SLICE(arr LIST, from int, to int) → LIST
```

#### Parameters

- `arr`: The input array.
- `from`: The zero-based position in the input array of the first element to include in the output array. Elements in positions that are less than the from position are not included in the output array. A negative position is interpreted as an index from the back of the array. For example, the value -1 begins the output array with the last element in the input array.
- `to`: The zero-based position in the input array of the last element to include in the output array. Elements in positions that are equal to or greater than the to position are not included in the resulting array. A negative position is interpreted as an index from the back of the array. For example, the value -1 ends the output array with the second-to-last element in the input array.

#### Examples

```sql
SELECT ARRAY_SLICE(array_col) -- [0,1,2]
SELECT ARRAY_SLICE(array_col) -- [0,1,2,3,4]
SELECT ARRAY_SLICE(array_col) -- [2,3]
SELECT ARRAY_SLICE(array_col) -- []
```

### ARRAY_SUM

Returns the sum of the elements in an array.

#### Syntax

```sql
ARRAY_SUM(list_column LIST) → numeric
```

#### Parameters

- `list_column`: Column that contains a LIST expression. Every element of the list must be a number such as INT, BIGINT, FLOAT4, FLOAT8, or DECIMAL. Cannot be an array literal.

#### Examples

```sql
SELECT ARRAY_SUM(array_col) -- 6
SELECT ARRAY_SUM(array_col) -- 3
SELECT ARRAY_SUM(array_col) -- 0
SELECT ARRAY_SUM(array_col) -- NULL
```

### ARRAY_TO_STRING

Converts an array to a string, with elements separated by a delimiter.

#### Syntax

```sql
ARRAY_TO_STRING(arr LIST, delimiter VARCHAR) → VARCHAR
```

#### Parameters

- `arr`: The source array.
- `delimiter`: The string to place between each element in the array.

#### Examples

```sql
SELECT ARRAY_TO_STRING(ARRAY[1, 2, 3], ',') -- 1,2,3
SELECT ARRAY_TO_STRING(array_col, ',') -- 1,,3
```

### ASCII

Returns the ASCII code value of the leftmost character of the string.

#### Syntax

```sql
ASCII(expression varchar) → int32
```

#### Parameters

- `expression`: The string for which the ASCII code for the first character in the string is returned.

#### Examples

```sql
SELECT ASCII ('DREMIO') -- 68
SELECT ASCII ('D') -- 68
SELECT ASCII ('') -- 0
```

### ASIN

Returns the arc sine of the argument.

#### Syntax

```sql
ASIN(numeric_expression NUMERIC) → FLOAT
```

#### Parameters

- `numeric_expression`: The number in radians. This must be DOUBLE, INTEGER, or FLOAT.

#### Examples

```sql
SELECT ASIN(0) -- 0.0
SELECT ASIN(1) -- 1.5707963267948966
SELECT ASIN(-1) -- -1.5707963267948966
```

### ATAN

Returns the arc tangent of the argument.

#### Syntax

```sql
ATAN(inputValue FLOAT) → FLOAT
```

#### Parameters

- `inputValue`: Floating-point input value, in the range (negative-infinity:positive-infinity)

#### Examples

```sql
SELECT ATAN(0) -- 0.0
SELECT ATAN(1) -- 0.7853981633974483
SELECT ATAN(-1) -- -0.7853981633974483
SELECT ATAN(19564.7) -- 1.5707452143321894
```

### ATAN2

Returns the arc tangent of the two arguments.

#### Syntax

```sql
ATAN2(y NUMERIC, x NUMERIC) → DOUBLE
```

#### Parameters

- `y`: Floating-point input value for the y-coordinate, in the range (negative-infinity:positive-infinity).
- `x`: Floating-point input value for the x-coordinate, in the range (negative-infinity:positive-infinity).

#### Examples

```sql
SELECT ATAN2(1.0,0.0) -- 1.5707963267948966
SELECT ATAN2(0.0,1.0) -- 0.0
SELECT ATAN2(0.0,-1.0) -- 3.141592653589793
SELECT ATAN2(-0.00000000001,-1.0) -- -3.141592653579793
SELECT ATAN2(0.0,0.0) -- 0.0
```

### AVG

Returns the average of the values in a group.

#### Syntax

```sql
AVG(numeric_expression NUMERIC) → DOUBLE
```

#### Parameters

- `numeric_expression`: The values for which to compute the average. Values can be type DOUBLE, NUMERIC, INTEGER, INTERVAL_DATE, or INTERVAL_YEAR.

#### Examples

```sql
SELECT AVG(3) -- 3.0
SELECT AVG("val_col"); -- -0.333333
```

### BASE64

Encodes a string using Base64.

#### Syntax

```sql
BASE64(expression varbinary) → varchar
```

#### Parameters

- `expression`: The string to encode.

#### Examples

```sql
SELECT BASE64('Dremio') -- RHJlbWlv
```

### BIN

Returns a string representation of the binary value of an integer.

#### Syntax

```sql
BIN(expression integer) → varchar
```

#### Parameters

- `expression`: An integer expression to encode.

#### Examples

```sql
SELECT BIN(100) -- 1100100
SELECT BIN(-100) -- 11111111111111111111111110011100
SELECT BIN(null) -- null
```

### BINARY_STRING

Converts a string to a binary string.

#### Syntax

```sql
BINARY_STRING(expression VARCHAR) → BINARY
```

#### Parameters

- `expression`: Varchar expression to convert to binary

#### Examples

```sql
SELECT BINARY_STRING('DREMIO') -- RFJFTUlP
SELECT BINARY_STRING('000') -- MDAw
```

### BITWISE_AND

Returns the bitwise AND of two numbers.

#### Syntax

```sql
BITWISE_AND(op1 NUMERIC, op2 NUMERIC) → NUMERIC
```

#### Parameters

- `op1`: First operand
- `op2`: Second operand

#### Examples

```sql
SELECT BITWISE_AND(7, 4) -- 4
SELECT BITWISE_AND(1, 2) -- 0
```

### BITWISE_NOT

Returns the bitwise NOT of a number.

#### Syntax

```sql
BITWISE_NOT(op1 NUMERIC) → NUMERIC
```

#### Parameters

- `op1`: Value to invert.

#### Examples

```sql
SELECT BITWISE_NOT(0) -- -1
SELECT BITWISE_NOT(9223372036854775807) -- -9223372036854775808
```

### BITWISE_OR

Returns the bitwise OR of two numbers.

#### Syntax

```sql
BITWISE_OR(op1 NUMERIC, op2 NUMERIC) → NUMERIC
```

#### Parameters

- `op1`: First operand.
- `op2`: Second operand.

#### Examples

```sql
SELECT BITWISE_OR(7, 4) -- 7
SELECT BITWISE_OR(1, 2) -- 3
```

### BITWISE_XOR

Returns the bitwise XOR of two numbers.

#### Syntax

```sql
BITWISE_XOR(op1 NUMERIC, op2 NUMERIC) → NUMERIC
```

#### Parameters

- `op1`: First operand.
- `op2`: Second operand.

#### Examples

```sql
SELECT BITWISE_XOR(7, 4) -- 3
SELECT BITWISE_XOR(1, 2) -- 3
```

### BIT_AND

Returns the bitwise AND of all non-null input values, or null if none.

#### Syntax

```sql
BIT_AND(expression int) → int
```

#### Parameters

- `expression`: An expression that evaluates to a data type that can be cast as an integer.

#### Examples

```sql
SELECT BIT_AND(passenger_count) FROM Samples."samples.dremio.com"."NYC-taxi-trips" -- 0
```

### BIT_LENGTH

Returns the length of the string in bits.

#### Syntax

```sql
BIT_LENGTH(expression binary, varchar) → integer
```

#### Parameters

- `expression`: A binary or varchar expression.

#### Examples

```sql
SELECT BIT_LENGTH(1010) -- 32
SELECT BIT_LENGTH('DREMIO') -- 48
SELECT BIT_LENGTH('abc') -- 24
SELECT BIT_LENGTH(NULL) -- null
```

### BIT_OR

Returns the bitwise OR of all non-null input values, or null if none.

#### Syntax

```sql
BIT_OR(expression int) → int
```

#### Parameters

- `expression`: An expression that evaluates to a data type that can be cast as an integer.

#### Examples

```sql
SELECT BIT_OR(passenger_count) FROM Samples."samples.dremio.com"."NYC-taxi-trips" -- 255
```

### BOOL_AND

Computes the boolean AND of two boolean expressions.

#### Syntax

```sql
BOOL_AND(bool_expression1 boolean, bool_expression2 boolean) → boolean
```

#### Parameters

- `bool_expression1`: Boolean input expression.
- `bool_expression2`: Boolean input expression.

#### Examples

```sql
SELECT BOOL_AND(TRUE, FALSE) -- False
```

### BOOL_OR

Computes the boolean OR of two boolean expressions.

#### Syntax

```sql
BOOL_OR(bool_expression1 boolean, bool_expression2 boolean) → boolean
```

#### Parameters

- `bool_expression1`: Boolean input expression.
- `bool_expression2`: Boolean input expression.

#### Examples

```sql
SELECT BOOL_OR(TRUE, FALSE) -- True
```

### CBRT

Returns the cube root of a number.

#### Syntax

```sql
CBRT(numeric_expression NUMERIC) → FLOAT
```

#### Parameters

- `numeric_expression`: The number (DOUBLE, FLOAT, INTEGER) for which you want to compute the cube root.

#### Examples

```sql
SELECT CBRT(8) -- 2.0
SELECT CBRT(120) -- 4.932424148660941
SELECT CBRT(99.5) -- 4.633839922986558
```

### CEIL

Alias for CEILING.

### CEILING

Returns the smallest integer not less than the argument.

#### Syntax

```sql
CEILING(numeric_expression NUMERIC) → INTEGER
```

#### Parameters

- `numeric_expression`: The number (DOUBLE, FLOAT, INTEGER) for which you want to compute the ceiling.

#### Examples

```sql
SELECT CEILING(3.1459) -- 4
SELECT CEIL(37.775420706711) -- 38
SELECT CEIL(-37.775420706711) -- -37
SELECT CEIL(0) -- 0
```

### CHAR

Alias for CHR.

### CHAR_LENGTH

Returns the number of characters in a string.

#### Syntax

```sql
CHAR_LENGTH(expression STRING) → INTEGER
```

#### Parameters

- `expression`: The expression (VARCHAR) to determine character length for.

#### Examples

```sql
SELECT CHAR_LENGTH('get the char length') -- 19
SELECT CHAR_LENGTH('DREMIO') -- 6
```

### CHARACTER_LENGTH

Returns the number of characters in a string.

#### Syntax

```sql
CHARACTER_LENGTH(expression varchar) → int32
```

#### Parameters

- `expression`: String expression to determine the length of.

#### Examples

```sql
SELECT CHARACTER_LENGTH('DREMIO') -- 6
```

### CHR

Returns the character with the given ASCII code.

#### Syntax

```sql
CHR(integer_expression int32) → varchar
```

#### Parameters

- `integer_expression`: Unicode code point to convert to character.

#### Examples

```sql
SELECT CHR(72) -- H
SELECT CHR(33) -- null
```

### COALESCE

Returns the first non-null expression in the list.

#### Syntax

```sql
COALESCE(expression1, expression2, [ ..., expressionN ]) → same as input type
```

#### Parameters

- `expression`: A combination of symbols and operators that the database evaluates to obtain a single data value. Expressions can be a single constant, variable, column, or scalar function.

#### Examples

```sql
SELECT COALESCE(address1, address2, city, state, zipCode) FROM customers -- 123 Main Street
```

### COL_LIKE

Returns true if the expression matches the pattern.

#### Syntax

```sql
COL_LIKE(expression_col varchar, pattern_col varchar) → boolean
```

#### Parameters

- `expression_col`: A column containing an expression to compare.
- `pattern_col`: A column containing the pattern to compare to the expression.

#### Examples

```sql
-- Assuming table 'names' with columns 'name' and 'pat'
-- values ('john', '%oh%'), ('jacob', '%aco%'), ('bill', '%ob%')
SELECT name FROM names WHERE COL_LIKE(name, pat);
-- john
-- jacob
```

### CONCAT

Concatenates two or more strings.

#### Syntax

```sql
CONCAT(expression1 string [, expression2 string] [, expressionN string]) → string
```

#### Parameters

- `expression1`: First string expression.
- `expression2` (optional): Second string expression.
- `expressionN` (optional): Nth string expression.

#### Examples

```sql
SELECT CONCAT('CON', 'CAT') -- CONCAT
SELECT CONCAT('con', 'cat', NULL) -- concat
```

### CONCAT_WS

Concatenates strings with a separator.

#### Syntax

```sql
CONCAT_WS(separator, expression1, expression2, [ ... expressionN ]) → string
```

#### Parameters

- `separator`: An expression of any character type.
- `expression`: An expression can be any data type. All arguments must be the same data type.

#### Examples

```sql
SELECT CONCAT_WS('-', 'cat', 'dog', 'bird') -- cat-dog-bird
```

### CONVERT_FROM

Converts a binary string to a Dremio data type.

#### Syntax

```sql
CONVERT_FROM(binary_value value_to_convert, data_type name_of_type) → varies
```

#### Parameters

- `binary_value`: The binary string to convert to a Dremio data type.
- `data_type`: The data type of the specified binary string.

#### Examples

```sql
SELECT CONVERT_FROM('["apple", "strawberry", "banana"]', 'json') -- ['apple', 'strawberry', 'banana']
SELECT CONVERT_FROM('{"name":"Gnarly", "age":7, "car":null}', 'json') -- {"name:"Gnarly","age":7}
```

### CONVERT_TO

Converts a value to a binary string.

#### Syntax

```sql
CONVERT_TO(expression value_to_convert, data_type name_of_type) → VARBINARY
```

#### Parameters

- `expression`: The value to convert to a binary string.
- `data_type`: The data type to use for the conversion to a binary string.

#### Examples

```sql
SELECT CONVERT_TO('this value' ,'UTF8') -- dGhpcyB2YWx1ZQ==
```

### CONVERT_TIMEZONE

Converts a timestamp to a different time zone.

#### Syntax

```sql
CONVERT_TIMEZONE([sourceTimezone string], destinationTimezone string, timestamp date, timestamp, or string in ISO 8601 format) → timestamp
```

#### Parameters

- `sourceTimezone` (optional): The time zone of the timestamp. If you omit this parameter, Dremio assumes that the source time zone is UTC.
- `destinationTimezone`: The time zone to convert the timestamp to.
- `timestamp`: The timestamp to convert

#### Examples

```sql
select convert_timezone('America/Los_Angeles', 'America/New_York', '2021-04-01 15:27:32') -- 2021-04-01 18:27:32
select convert_timezone('America/Los_Angeles', 'America/New_York', timestamp '2021-04-01 15:27:32'); -- 2021-04-01 18:27:32
select convert_timezone('PST', 'EST', '2021-04-01 15:27:32') -- 2021-04-01 18:27:32
select convert_timezone('America/Los_Angeles', 'America/New_York', '2021-04-01') -- 2021-04-01 03:00:00
select convert_timezone('America/Los_Angeles', 'America/New_York', date '2021-04-01') -- 2021-04-01 03:00:00
select convert_timezone('EDT', '2021-04-01 15:27:32') -- 2021-04-01 11:27:32
select convert_timezone('PST', '+02:00', '2021-04-01 15:27:32') -- 2021-04-02 01:27:32
```

### CORR

Returns the coefficient of correlation of a set of number pairs.

#### Syntax

```sql
CORR(expression1 numeric, expression2 numeric) → double
```

#### Parameters

- `expression1`: An expression that evaluates to a numeric type. This parameter is the dependent value.
- `expression2`: An expression that evaluates to a numeric type. This parameter is the independent value.

#### Examples

```sql
SELECT "CORR"(100, 4) -- NaN
```

### COS

Returns the cosine of an angle.

#### Syntax

```sql
COS(numeric_expression NUMERIC) → FLOAT
```

#### Parameters

- `numeric_expression`: The number in radians. This must be DOUBLE, INTEGER, or FLOAT.

#### Examples

```sql
SELECT COS(0) -- 1.0
SELECT COS(1.0) -- 0.5403023058681398
SELECT COS(-1) -- 0.5403023058681398
```

### COT

Returns the cotangent of an angle.

#### Syntax

```sql
COT(numeric_expression NUMERIC) → FLOAT
```

#### Parameters

- `numeric_expression`: The number in radians. This must be DOUBLE, INTEGER, or FLOAT.

#### Examples

```sql
SELECT COT(0) -- 1.0
SELECT COT(1.0) -- 0.5403023058681398
SELECT COT(-1) -- 0.5403023058681398
```

### COUNT

Returns the number of rows in the query.

#### Syntax

```sql
COUNT(expression ANY) → BIGINT
```

#### Parameters

- `expression`: The expression to evaluate. Can be an asterisk (*) or the column name of any primitive data type. Use an asterisk to include rows that contain NULL. Use a column name to ignore rows that contain NULL.

#### Examples

```sql
SELECT COUNT(passenger_count) FROM "Samples"."samples.dremio.com"."NYC-taxi-trips"; -- 338293677
```

### COVAR_POP

Returns the population covariance of a set of number pairs.

#### Syntax

```sql
COVAR_POP(expression1 NUMERIC, expression2 NUMERIC) → DOUBLE
```

#### Parameters

- `expression1`: An expression that evaluates to a numeric type. This parameter is the dependent value.
- `expression2`: An expression that evaluates to a numeric type. This parameter is the independent value.

#### Examples

```sql
SELECT COVAR_POP(trip_distance_mi, fare_amount) FROM Samples."samples.dremio.com"."NYC-taxi-trips"; -- 31.705367711861427
SELECT COVAR_POP(DISTINCT trip_distance_mi, fare_amount FROM Samples."samples.dremio.com"."NYC-taxi-trips"; -- 302.592806814534
```

### COVAR_SAMP

Returns the sample covariance of a set of number pairs.

#### Syntax

```sql
COVAR_SAMP(expression1 NUMERIC, expression2 NUMERIC) → DOUBLE
```

#### Parameters

- `expression1`: An expression that evaluates to a numeric type. This parameter is the dependent value.
- `expression2`: An expression that evaluates to a numeric type. This parameter is the independent value.

#### Examples

```sql
SELECT COVAR_SAMP(trip_distance_mi, fare_amount) FROM Samples."samples.dremio.com"."NYC-taxi-trips"; -- 31.705367805565245
SELECT COVAR_SAMP(DISTINCT trip_distance_mi, fare_amount) FROM Samples."samples.dremio.com"."NYC-taxi-trips"; -- 302.5936880585907
```

### CUME_DIST

Calculates the cumulative distribution of a value in a group of values.

#### Syntax

```sql
CUME_DIST() OVER ( [PARTITION BY partition_expression] [ORDER BY order_expression]) → double
```

#### Parameters

- `partition_expression` (optional): An expression that groups rows into partitions.
- `order_expression`: An expression that specifies the order of the rows within each partition.

#### Examples

```sql
SELECT "Category", "Descript", "DayOfWeek", CUME_DIST() OVER ( PARTITION BY "Category" ORDER BY "DayOfWeek") FROM Samples."samples.dremio.com"."SF_incidents2016.json"
-- Category, Descript, DayOfWeek, EXPR$3
-- ARSON, ARSON, Friday, 0.13636363636363635
-- EMBEZZLEMENT, EMBEZZLED VEHICLE, Friday, 0.18452380952380953
```

### CURRENT_DATE

Returns the current date.

#### Syntax

```sql
CURRENT_DATE() → date
```

#### Examples

```sql
SELECT CURRENT_DATE() -- 2021-07-02
SELECT CURRENT_DATE -- 2021-07-02
```

### CURRENT_TIME

Returns the current time.

#### Syntax

```sql
CURRENT_TIME() → TIME
```

#### Examples

```sql
SELECT CURRENT_TIME() -- 06:04:31
SELECT CURRENT_TIME -- 06:04:31
```

### CURRENT_TIMESTAMP

Returns the current timestamp.

#### Syntax

```sql
CURRENT_TIMESTAMP() → TIMESTAMP
```

#### Examples

```sql
SELECT CURRENT_TIMESTAMP() -- 2021-06-24 06:11:51.567000
```

### DATE_ADD

Adds a specified number of days or a time interval to a date or timestamp.

#### Syntax

```sql
DATE_ADD(date_expression string, days integer) → date
DATE_ADD(date_expression date, days integer) → date
DATE_ADD(date_expression string, time_interval interval) → timestamp
DATE_ADD(date_expression date, time_interval interval) → timestamp
DATE_ADD(timestamp_expression string, time_interval interval) → timestamp
```

#### Parameters

- `date_expression`: A string-formatted date ('YYYY-MM-DD') or a DATE column/literal.
- `days`: The number of days to add.
- `time_interval`: A CAST of a number to an interval (e.g., DAY, MONTH, YEAR).
- `timestamp_expression`: A string-formatted timestamp ('YYYY-MM-DD HH24:MI:SS').

#### Examples

```sql
SELECT DATE_ADD('2022-01-01', 2) -- 2022-01-03
SELECT DATE_ADD(DATE '2022-01-01', 30) -- 2022-01-31
SELECT DATE_ADD('2022-01-01', CAST(2 AS INTERVAL DAY)) -- 2022-01-03 00:00:00.000
SELECT DATE_ADD('2022-01-01 12:00:00', CAST(30 AS INTERVAL DAY)) -- 2022-01-31 00:00:00.000
```

### DATE_DIFF

Returns the difference between two dates or timestamps.

#### Syntax

```sql
DATE_DIFF(date_expression DATE, days INTEGER) → DATE
DATE_DIFF(date_expression DATE, date_expression DATE) → INTERVAL DAY
DATE_DIFF(timestamp_expression TIMESTAMP, timestamp_expression TIMESTAMP) → INTERVAL DAY
DATE_DIFF(time_expression TIME, time_interval INTERVAL) → TIME
```

#### Parameters

- `date_expression`: The date to subtract from or subtract days from.
- `days`: Number of days to subtract.
- `timestamp_expression`: The timestamp to subtract from.
- `time_expression`: The time to subtract from.
- `time_interval`: Interval to subtract.

#### Examples

```sql
SELECT DATE_DIFF(DATE '2022-01-01', 5) -- 2021-12-27
SELECT DATE_DIFF(DATE '2022-04-01', DATE '2022-01-01') -- +090 00:00:00.000
SELECT DATE_DIFF(TIMESTAMP '2022-04-01 12:35:23', TIMESTAMP '2022-01-01 01:00:00') -- +090 11:35:23.000
SELECT DATE_DIFF(TIME '12:00:00', CAST(30 AS INTERVAL SECOND)) -- 11:59:30
```

### DATE_PART

Extracts a subfield from a date or timestamp.

#### Syntax

```sql
DATE_PART(field string, source date or timestamp) → integer
```

#### Parameters

- `field`: Must be one of: YEAR, QUARTER, MONTH, WEEK, DAY, HOUR, MINUTE, SECOND.
- `source`: The value from which to extract the subfield

#### Examples

```sql
select date_part('year', timestamp '2021-04-01 15:27:32') -- 2021
select date_part('month', date '2021-04-01') -- 4
```

### DATE_SUB

Subtracts a specified number of days or a time interval from a date or timestamp.

#### Syntax

```sql
DATE_SUB(date_expression STRING, days INTEGER) → DATE
DATE_SUB(date_expression DATE, days INTEGER) → DATE
DATE_SUB(date_expression STRING, time_interval INTERVAL) → TIMESTAMP
DATE_SUB(date_expression DATE, time_interval INTERVAL) → TIMESTAMP
DATE_SUB(timestamp_expression STRING, time_interval INTERVAL) → TIMESTAMP
```

#### Parameters

- `date_expression`: A string-formatted date ('YYYY-MM-DD') or a DATE column/literal.
- `days`: The number of days to subtract.
- `time_interval`: A CAST of a number to an interval.
- `timestamp_expression`: A string-formatted timestamp.

#### Examples

```sql
SELECT DATE_SUB('2022-01-01', 2) -- 2021-12-30
SELECT DATE_SUB(DATE '2022-01-01', 30) -- 2021-12-02
SELECT DATE_SUB('2022-01-01', CAST(2 AS INTERVAL DAY)) -- 2021-12-30 00:00:00.000
SELECT DATE_SUB('2022-01-01 12:00:00', CAST(30 AS INTERVAL DAY)) -- 2021-12-02 00:00:00.000
```

### DATE_TRUNC

Truncates a date or timestamp to the specified time unit.

#### Syntax

```sql
DATE_TRUNC(time_unit LITERAL, date_timestamp_expression DATE OR TIMESTAMP) → DATE
```

#### Parameters

- `time_unit`: 'YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', or 'SECOND'.
- `date_timestamp_expression`: The date or timestamp to truncate.

#### Examples

```sql
SELECT DATE_TRUNC('MONTH', '2021-12-24') -- 2021-12-01
SELECT DATE_TRUNC('MINUTE', CAST('2021-12-24 12:28:33' as TIMESTAMP)) -- 2021-12-24 12:28:00
SELECT DATE_TRUNC('HOUR', '2021-12-24 12:28:33') -- 2021-12-24
```

### DAY

Returns the day of the month from a date or timestamp.

#### Syntax

```sql
DAY(date_timestamp_expression string) → bigint
```

#### Parameters

- `date_timestamp_expression`: A DATE or TIMESTAMP expression.

#### Examples

```sql
SELECT "DAY"('2003-02-01 11:43:22') -- 1
```

### DAYOFMONTH

Returns the day of the month from a date or timestamp.

#### Syntax

```sql
DAYOFMONTH(date_timestamp_expression string) → bigint
```

#### Parameters

- `date_timestamp_expression`: A DATE or TIMESTAMP expression.

#### Examples

```sql
SELECT DAYOFMONTH(DATE '2021-02-28') -- 28
SELECT DAYOFMONTH(TIMESTAMP '2021-02-28 11:43:22') -- 28
```

### DAYOFWEEK

Returns the day of the week from a date or timestamp.

#### Syntax

```sql
DAYOFWEEK(date_timestamp_expression string) → bigint
```

#### Parameters

- `date_timestamp_expression`: A DATE or TIMESTAMP expression.

#### Examples

```sql
SELECT DAYOFWEEK(DATE '2021-02-28') -- 1
SELECT DAYOFWEEK(TIMESTAMP '2021-02-27 11:43:22') -- 7
```

### DAYOFYEAR

Returns the day of the year from a date or timestamp.

#### Syntax

```sql
DAYOFYEAR(date_timestamp_expression string) → bigint
```

#### Parameters

- `date_timestamp_expression`: A DATE or TIMESTAMP expression.

#### Examples

```sql
SELECT DAYOFYEAR(DATE '2021-02-28') -- 59
SELECT DAYOFYEAR(TIMESTAMP '2021-03-15 11:43:22') -- 74
```

### DEGREES

Converts radians to degrees.

#### Syntax

```sql
DEGREES(numeric_expression NUMERIC) → FLOAT
```

#### Parameters

- `numeric_expression`: The number of radians. This must be an DOUBLE, INTEGER, or FLOAT.

#### Examples

```sql
SELECT DEGREES(PI()) -- 180.0
SELECT DEGREES(0) -- 0.0
SELECT DEGREES(1) -- 57.29577951308232
```

### DENSE_RANK

Returns the rank of a value in a group of values.

#### Syntax

```sql
DENSE_RANK() OVER ( [PARTITION BY partition_expression] [ORDER BY order_expression]) → bigint
```

#### Parameters

- `partition_expression` (optional): An expression that groups rows into partitions.
- `order_expression`: An expression that specifies the order of the rows within each partition.

#### Examples

```sql
SELECT "Category", "Descript", "DayOfWeek", DENSE_RANK() OVER ( PARTITION BY "Category" ORDER BY "DayOfWeek") FROM Samples."samples.dremio.com"."SF_incidents2016.json"
-- Category, Descript, DayOfWeek, EXPR$3
-- ARSON, ARSON, Friday, 1
-- ARSON, ARSON, Monday, 2
```

### E

Returns the base of the natural logarithm (e).

#### Syntax

```sql
E() → float
```

#### Examples

```sql
SELECT E() -- 2.718281828459045
```

### EXP

Returns e raised to the power of a specified number.

#### Syntax

```sql
EXP(numeric_expression NUMERIC) → FLOAT
```

#### Parameters

- `numeric_expression`: The exponent value to raise e to. This must be an DOUBLE, INTEGER, or FLOAT.

#### Examples

```sql
SELECT EXP(1) -- 2.718281828459045
SELECT EXP(10.0) -- 22026.465794806718
```

### EXTRACT

Extracts a part of a date, time, or timestamp.

#### Syntax

```sql
EXTRACT(time_unit KEYWORD, date_time_expression DATE, TIME, TIMESTAMP) → INTEGER
```

#### Parameters

- `time_unit`: The time unit to extract (EPOCH, YEAR, MONTH, DAY, HOUR, MINUTE, SECOND).
- `date_time_expression`: The date, time, or timestamp.

#### Examples

```sql
SELECT EXTRACT(HOUR FROM CAST('05:33:44' AS TIME)) -- 5
SELECT EXTRACT(MONTH FROM CAST('2021-03-22 05:33:44.2' AS TIMESTAMP)) -- 3
SELECT EXTRACT(SECOND FROM CAST('2021-03-22 05:33:44.2' AS TIMESTAMP)) -- 44
SELECT EXTRACT(YEAR FROM CAST('2021-03-22' AS DATE)) -- 2021
SELECT EXTRACT(EPOCH FROM CAST('2021-03-22 05:33:44.2' AS TIMESTAMP)) -- 1616391224
SELECT EXTRACT(EPOCH FROM CAST('2021-03-22' AS DATE)) -- 1616371200
```

### FIRST_VALUE

Returns the first value in an ordered set of values.

#### Syntax

```sql
FIRST_VALUE(expression VARCHAR, order_subclause VARCHAR) → VARCHAR
```

#### Parameters

- `expression`: The expression that determines the return value.
- `order_subclause`: A subclause that specifies the order of the rows within each partition of the result set.

#### Examples

```sql
SELECT city, state, pop, FIRST_VALUE(pop) OVER (PARTITION BY state ORDER BY city) FROM Samples."samples.dremio.com"."zips.json";
```

### FLATTEN

Explodes a compound value into multiple rows.

#### Syntax

```sql
FLATTEN(expression list) → list
```

#### Parameters

- `expression`: The expression that will be unpacked into rows. The expression must be of data type LIST.

#### Examples

```sql
SELECT FLATTEN(CONVERT_FROM ('["Ford", "BMW", "Fiat"]', 'json'))
-- Ford
-- BMW
-- Fiat
```

### FLOOR

Returns the largest integer not greater than the argument.

#### Syntax

```sql
FLOOR(numeric_expression NUMERIC) → INTEGER
```

#### Parameters

- `numeric_expression`: The number (DOUBLE, FLOAT, INTEGER) for which you want to compute the floor.

#### Examples

```sql
SELECT FLOOR(0) -- 0
SELECT FLOOR(45.76) -- 45
SELECT FLOOR(-1.3) -- -2
```

### FROM_HEX

Converts a hexadecimal string to a binary value.

#### Syntax

```sql
FROM_HEX(in string) → binary
```

#### Parameters

- `in`: A hexadecimal string

#### Examples

```sql
select from_hex('3fd98a3c') -- P9mKPA==
```

### GREATEST

Returns the largest value from a list of expressions.

#### Syntax

```sql
GREATEST(expression) → same as input type
```

#### Parameters

- `expression`: The arguments must include at least one expression. All the expressions should be of the same type or compatible types.

#### Examples

```sql
SELECT GREATEST(1, 5, 3, 8) -- 8
```

### HASH

Computes a hash value for an expression.

#### Syntax

```sql
HASH(expression any) → numeric
```

#### Parameters

- `expression`: Can be a general expression of any Dremio-supported data type.

#### Examples

```sql
SELECT HASH(host_id) FROM "Samples"."samples.dremio.com"."Dremio University"."airbnb_listings.csv" LIMIT 5
```

### HASH64

Computes a 64-bit hash value for an expression.

#### Syntax

```sql
HASH64(value ANY [, seed BIGINT]) → BIGINT
```

#### Parameters

- `value`: Input value for hash calculation.
- `seed` (optional): Optional seed for hash calculation.

#### Examples

```sql
SELECT HASH64('abc') -- -5434086359492102041
SELECT HASH64(5.127) -- -1149762993205326574
SELECT HASH64(null) -- 0
SELECT HASH64('abc',123) -- 1489494923063836066
```

### HEX

Returns the hexadecimal representation of a value.

#### Syntax

```sql
HEX(expression any primitive) → varchar
```

#### Parameters

- `expression`: The expression to encode.

#### Examples

```sql
SELECT HEX('Dremio') -- 4472656D696F
SELECT HEX(2023) -- 7E7
```

### HOUR

Extracts the hour from a time, timestamp, or date.

#### Syntax

```sql
EXTRACT(HOUR FROM date_timestamp_expression string) → bigint
```

#### Parameters

- `date_timestamp_expression`: A TIME, TIMESTAMP, or DATE expression.

#### Examples

```sql
SELECT EXTRACT(HOUR FROM TIMESTAMP '2019-08-12 01:10:30.123456') -- 1
SELECT EXTRACT(HOUR FROM TIME '01:10:30.123456') -- 1
SELECT EXTRACT(HOUR FROM CAST('2019-08-12 01:10:30' AS TIMESTAMP)) -- 1
```

### IFNULL

Alias for COALESCE or NVL.

### ILIKE

Compares two strings for equality, ignoring case.

#### Syntax

```sql
ILIKE(expression varchar, pattern varchar) → boolean
ILIKE(expression varchar, pattern varchar, escape_character varchar) → boolean
```

#### Parameters

- `expression`: The expression to compare.
- `pattern`: The pattern that is compared to the expression.
- `escape_character`: Putting escape_character before a wildcard in pattern makes ILIKE treat the wildcard as a regular character when it appears in expression.

#### Examples

```sql
SELECT ILIKE ('pancake', '%Cake') -- True
SELECT ILIKE ('50%_Off', '%50!%%','!') -- True
```

### INITCAP

Returns the string with the first letter of each word in uppercase and all other letters in lowercase.

#### Syntax

```sql
INITCAP(expression varchar) → varchar
```

#### Parameters

- `expression`: Input string.

#### Examples

```sql
SELECT INITCAP('a guide to data lakehouses') -- A Guide To Data Lakehouses
SELECT INITCAP('a guide to data lakeHouses') -- A Guide To Data Lakehouses
```

### IS_MEMBER

Checks if the current user is a member of a specific role.

#### Syntax

```sql
IS_MEMBER(expression varchar) → boolean
```

#### Parameters

- `expression`: String expression identfying a role in Dremio.

#### Examples

```sql
SELECT IS_MEMBER ('public') -- True
SELECT IS_MEMBER ('non-role') -- False
```

### IS_UTF8

Checks if a binary string is a valid UTF-8 string.

#### Syntax

```sql
IS_UTF8(in any) → boolean
```

#### Parameters

- `in`: an expression

#### Examples

```sql
select is_utf8('hello') -- True
```

### IS_VARCHAR

Checks if an expression is a VARCHAR.

#### Syntax

```sql
IS_VARCHAR(expression any) → boolean
```

#### Parameters

- `expression`: Input expression.

#### Examples

```sql
SELECT IS_VARCHAR(column_name) -- True
```

### LAG

Returns the value of a column at a specified offset before the current row.

#### Syntax

```sql
LAG(expression, [offset]) OVER ([PARTITION BY partition_expression] [ORDER BY order_expression]) → same as input type
```

#### Parameters

- `expression` (optional): An expression that is returned.
- `offset` (optional): The number of rows before the current row from which to obtain a value.

#### Examples

```sql
SELECT "Category", "Descript", "DayOfWeek", LAG(DayOfWeek, 3) OVER ( PARTITION BY "Category" ORDER BY "DayOfWeek") FROM Samples."samples.dremio.com"."SF_incidents2016.json"
-- Category, Descript, DayOfWeek, EXPR$3
-- ARSON, ARSON, Friday, null
-- ARSON, ARSON, Friday, null
-- ARSON, ARSON OF AN INHABITED DWELLING, Friday, null
-- ARSON, ARSON, Friday, Friday
```

### LAST_DAY

Returns the last day of the month for a given date or timestamp.

#### Syntax

```sql
LAST_DAY(date_timestamp_expression string) → date
```

#### Parameters

- `date_timestamp_expression`: A DATE or TIMESTAMP expression.

#### Examples

```sql
SELECT LAST_DAY('2009-01-12 12:58:59') -- 2009-01-31
```

### LAST_VALUE

Returns the last value in an ordered set of values.

#### Syntax

```sql
LAST_VALUE(expression VARCHAR, order_subclause VARCHAR) → VARCHAR
```

#### Parameters

- `expression`: The expression that determines the return value.
- `order_subclause`: A subclause that specifies the order of the rows within each partition of the result set.

#### Examples

```sql
SELECT city, state, pop, LAST_VALUE(pop) OVER (PARTITION BY state ORDER BY city) FROM Samples."samples.dremio.com"."zips.json"
```

### LCASE

Returns the string in lowercase.

#### Syntax

```sql
LCASE(expression varchar) → varchar
```

#### Parameters

- `expression`: String to convert to lowercase.

#### Examples

```sql
SELECT LCASE('A GUIDE to data Lakehouses') -- a guide to data lakehouses
```

### LEAD

Returns the value of a column at a specified offset after the current row.

#### Syntax

```sql
LEAD(expression, [offset]) OVER ([PARTITION BY partition_expression] [ORDER BY order_expression]) → same as input type
```

#### Parameters

- `expression` (optional): An expression that is returned.
- `offset` (optional): The number of rows after the current row from which to obtain a value.

#### Examples

```sql
SELECT "Category", "Descript", "DayOfWeek", LEAD(DayOfWeek, 3) OVER ( PARTITION BY "Category" ORDER BY "DayOfWeek") FROM Samples."samples.dremio.com"."SF_incidents2016.json"
```

### LEFT

Returns the specified number of characters from the left of a string.

#### Syntax

```sql
LEFT(expression varchar, length int64) → varchar
```

#### Parameters

- `expression`: String input parameter
- `length`: Number of characters on the left to return.

#### Examples

```sql
SELECT "LEFT"('Dremio - SQL Engine', -12) -- Dremio
SELECT "LEFT"('Dremio - SQL Engine', 6) -- Dremio
```

### LENGTH

Returns the length of a string.

#### Syntax

```sql
LENGTH([expression varchar]) → int32
```

#### Parameters

- `expression` (optional): String expression to determine the length of.

#### Examples

```sql
SELECT LENGTH('DREMIO') -- 6
```

### LISTAGG

Concatenates the values of a column for each group.

#### Syntax

```sql
LISTAGG ( [ALL | DISTINCT] measure_expr [, 'delimiter'] ) [WITHIN GROUP ( ORDER BY measure_expr [ASC | DESC] )]
```

#### Parameters

- `ALL` (optional): Keeps duplicate values in the return list. This is the default behavior.
- `DISTINCT` (optional): Removes duplicate values from the return list.
- `measure_expr`: A string column or value.
- `delimiter` (optional): Designates a string literal to separate the measure column values. If a delimiter is not specified, will default to NULL.
- `WITHIN GROUP` (optional): Determines the order in which the concatenated values are returned.

#### Examples

```sql
SELECT LISTAGG(city, '; ') FROM "Samples"."samples.dremio.com"."zips.json"
```

### LN

Returns the natural logarithm of a number.

#### Syntax

```sql
LN(numeric_expression double) → float8
```

#### Parameters

- `numeric_expression`: A number greater than 0.

#### Examples

```sql
SELECT LN(0), LN(.1525), LN(1), LN(5.35), LN(5269853105789632584), LN(-1)
-- null, -1.8805906829346708, 0.0, 1.6770965609079151, 43.10853416239341, null
```

### LOCALTIME

Returns the current time in the local time zone.

#### Syntax

```sql
LOCALTIME() → time
```

#### Examples

```sql
SELECT LOCALTIME() -- 05:07:01
```

### LOCALTIMESTAMP

Returns the current timestamp in the local time zone.

#### Syntax

```sql
LOCALTIMESTAMP() → timestamp
```

#### Examples

```sql
SELECT LOCALTIMESTAMP() -- 2021-06-29 05:17:44.703000
```

### LOCATE

Returns the position of the first occurrence of a substring in a string.

#### Syntax

```sql
LOCATE(substring varchar, expression varchar [, start int32]) → int32
```

#### Parameters

- `substring`: Substring to search for in the expression.
- `expression`: The input expression to search.
- `start` (optional): Position to start the search from.

#### Examples

```sql
SELECT LOCATE('no','banana') -- 0
SELECT LOCATE('an','banana') -- 2
SELECT LOCATE('an','banana', 3) -- 4
```

### LOG

Returns the logarithm of a number.

#### Syntax

```sql
LOG([base_expression float], expression float) → double
LOG([base_expression double], expression double) → double
LOG(expression int64) → double
LOG([base_expression int64], expression int64) → double
LOG(expression int32) → double
LOG([base_expression int32], expression int32) → double
LOG(expression float) → double
LOG(expression double) → double
```

#### Parameters

- `base_expression` (optional): The base to use.
- `expression`: The value for which you want to calculate the log.

#### Examples

```sql
SELECT LOG(20.5, 1.5) -- 0.1342410830900514
SELECT LOG(10) -- 2.302585092994046
SELECT LOG(10, 2) -- 0.30102999566398114
SELECT LOG(12.5) -- 2.5257286443082556
```

### LOG10

Returns the base-10 logarithm of a number.

#### Syntax

```sql
LOG10(expression double) → double
LOG10(expression int64) → double
LOG10(expression int32) → double
LOG10(expression float) → double
```

#### Parameters

- `expression`: The value for which you want to calculate the log.

#### Examples

```sql
SELECT LOG10(20.5) -- 1.3117538610557542
SELECT LOG10(100) -- 2.0
```

### LOWER

Returns the string in lowercase.

#### Syntax

```sql
LOWER(expression varchar) → varchar
```

#### Parameters

- `expression`: String to convert to lowercase.

#### Examples

```sql
SELECT LOWER('A GUIDE to data Lakehouses') -- a guide to data lakehouses
```

### LPAD

Pads a string on the left with a specified character.

#### Syntax

```sql
LPAD(base_expression varchar, length int64) → varchar
LPAD(base_expression varchar, length int64 [, pad_expression varchar]) → varchar
```

#### Parameters

- `base_expression`: The expression to pad.
- `length`: The number of characters to return.
- `pad_expression` (optional): Characters to pad the base_expression with.

#### Examples

```sql
SELECT LPAD('parameter', 11) -- parameter
SELECT LPAD('engineering', 6) -- engine
select LPAD('parameter', 11, '-') -- --parameter
```

### LTRIM

Removes leading characters from a string.

#### Syntax

```sql
LTRIM(expression varchar, trim_expression varchar) → varchar
```

#### Parameters

- `expression`: The expression to be trimmed.
- `trim_expression`: Leading characters to trim. If this parameter is not specified, then spaces will be trimmed from the input expression.

#### Examples

```sql
SELECT LTRIM('pancake', 'pan') -- cake
SELECT LTRIM('pancake', 'abnp') -- cake
SELECT LTRIM(' dremio') -- dremio
```

### MASK_FIRST_N

Masks the first N characters of a string.

#### Syntax

```sql
MASK_FIRST_N(expression varchar [, num_chars int] [, uc_mask varchar] [, lc_mask varchar] [, num_mask varchar]) → varchar
```

#### Parameters

- `expression`: The string to mask.
- `num_chars` (optional): The number of characters to mask.
- `uc_mask` (optional): Controls the mask character for upper case letters.
- `lc_mask` (optional): Controls the mask character for lower case letters.
- `num_mask` (optional): Controls the mask character for numbers.

#### Examples

```sql
SELECT MASK_FIRST_N('abcd-ABCD-1234') -- xxxx-ABCD-1234
SELECT MASK_FIRST_N('abcd-ABCD-1234', 2) -- xxcd-ABCD-1234
SELECT MASK_FIRST_N('Aa12-ABCD-1234', 4, 'U', 'u', '#') -- Uu##-ABCD-1234
SELECT MASK_FIRST_N('abcd-ABCD-1234', 7, '', 'u', '') -- uuuu-XXCD-1234
```

### MASK_LAST_N

Masks the last N characters of a string.

#### Syntax

```sql
MASK_LAST_N(expression varchar [, num_chars int] [, uc_mask varchar] [, lc_mask varchar] [, num_mask varchar]) → varchar
```

#### Parameters

- `expression`: The string to mask.
- `num_chars` (optional): The number of characters to mask.
- `uc_mask` (optional): Controls the mask character for upper case letters.
- `lc_mask` (optional): Controls the mask character for lower case letters.
- `num_mask` (optional): Controls the mask character for numbers.

#### Examples

```sql
SELECT MASK_LAST_N('abcd-ABCD-1234') -- abcd-ABCD-nnnn
SELECT MASK_LAST_N('abcd-ABCD-1234', 2) -- abcd-ABCD-12nn
SELECT MASK_LAST_N('abcd-ABCD-Aa12', 4, 'U', 'u', '#') -- abcd-ABCD-Uu##
SELECT MASK_LAST_N('abcd-ABCD-1234', 7, '', 'u', '') -- abcd-ABXX-nnnn
```

### MASK_SHOW_FIRST_N

Masks all but the first N characters of a string.

#### Syntax

```sql
MASK_SHOW_FIRST_N(expression varchar [, num_chars int] [, uc_mask varchar] [, lc_mask varchar] [, num_mask varchar]) → varchar
```

#### Parameters

- `expression`: The string to mask.
- `num_chars` (optional): The number of characters to unmask.
- `uc_mask` (optional): Controls the mask character for upper case letters.
- `lc_mask` (optional): Controls the mask character for lower case letters.
- `num_mask` (optional): Controls the mask character for numbers.

#### Examples

```sql
SELECT MASK_SHOW_FIRST_N('abcd-ABab-1234') -- abcd-XXxx-nnnn
SELECT MASK_SHOW_FIRST_N('abcd-ABab-1234', 2) -- abxx-XXxx-nnnn
SELECT MASK_SHOW_FIRST_N('Aa12-ABab-1234', 4, 'U', 'u', '#') -- Aa12-UUuu-####
SELECT MASK_SHOW_FIRST_N('abcd-ABCD-1234', 2, '', 'u', '') -- abuu-XXXX-nnnn
```

### MASK_SHOW_LAST_N

Masks all but the last N characters of a string.

#### Syntax

```sql
MASK_SHOW_LAST_N(expression varchar [, num_chars int] [, uc_mask varchar] [, lc_mask varchar] [, num_mask varchar]) → varchar
```

#### Parameters

- `expression`: The string to mask.
- `num_chars` (optional): The number of characters to unmask.
- `uc_mask` (optional): Controls the mask character for upper case letters.
- `lc_mask` (optional): Controls the mask character for lower case letters.
- `num_mask` (optional): Controls the mask character for numbers.

#### Examples

```sql
SELECT MASK_SHOW_LAST_N('ab12-ABab-1234') -- xxnn-XXxx-1324
SELECT MASK_SHOW_LAST_N('ab12-ABab-1234', 2) -- xxnn-XXxx-nn34
SELECT MASK_SHOW_LAST_N('Aa12-ABab-1234', 4, 'U', 'u', '#') -- Uu##-UUuu-1234
SELECT MASK_SHOW_LAST_N('abcd-ABCD-1234', 2, '', 'u', '') -- uuuu-XXXX-nn34
```

### MAX

Returns the maximum value of an expression across all rows.

#### Syntax

```sql
MAX(expression NUMERIC) → NUMERIC
```

#### Parameters

- `expression`: The expression from which to take the maximum value, across all rows.

#### Examples

```sql
SELECT MAX("total_amount") FROM "Samples"."samples.dremio.com"."NYC-taxi-trips"; -- 685908.1
```

### MD5

Computes the MD5 hash of a string.

#### Syntax

```sql
MD5(expression varchar) → varchar
```

#### Parameters

- `expression`: The string to hash.

#### Examples

```sql
SELECT MD5('Dremio') -- 288e0e9ab8b8ac8737afefecf16f61fd
```

### MEDIAN

Computes the median value of a numeric column.

#### Syntax

```sql
MEDIAN(num_col numeric) → double precision
```

#### Parameters

- `num_col`: A numeric column whose median value you want to compute.

#### Examples

```sql
SELECT MEDIAN(pop) FROM Samples."samples.dremio.com"."zips.json" -- 2783.0
```

### MIN

Returns the minimum value of an expression across all rows.

#### Syntax

```sql
MIN(expression NUMERIC) → NUMERIC
```

#### Parameters

- `expression`: The expression from which to take the minimum value, across all rows.

#### Examples

```sql
SELECT MIN("total_amount") FROM "Samples"."samples.dremio.com"."NYC-taxi-trips"; -- -1430.0
```

### MOD

Returns the remainder of a division.

#### Syntax

```sql
MOD(numeric_expression int64, numeric_expression int64) → int64
MOD(numeric_expression int64, numeric_expression int32) → int32
MOD(numeric_expression decimal(0,0), numeric_expression decimal(0,0)) → decimal(0,0)
```

#### Parameters

- `numeric_expression`: The dividend.
- `numeric_expression`: The divisor.

#### Examples

```sql
SELECT MOD(50, 7) -- 1
SELECT MOD(35, 5) -- 0
SELECT MOD(47.6, 5.2) -- 0.8
```

### MONTH

Extracts the month from a time, timestamp, or date.

#### Syntax

```sql
EXTRACT(MONTH FROM date_timestamp_expression string) → bigint
```

#### Parameters

- `date_timestamp_expression`: A DATE or TIMESTAMP expression.

#### Examples

```sql
SELECT EXTRACT(MONTH FROM TIMESTAMP '2019-08-12 01:00:00.123456') -- 8
SELECT EXTRACT(MONTH FROM DATE '2019-08-12') -- 8
SELECT EXTRACT(MONTH FROM CAST('2019-08-12 01:00:00' AS TIMESTAMP)) -- 8
```

### MULTIPLY

Use the `*` operator for multiplication.

### NEAR

Not a supported function.

### NEXT_DAY

Returns the date of the first specified day of the week that occurs after the input date.

#### Syntax

```sql
NEXT_DAY(date_timestamp_expression string, day_of_week string) → date
```

#### Parameters

- `date_timestamp_expression`: A DATE or TIMESTAMP expression.
- `day_of_week`: A string expression identifying a day of the week (e.g., 'SU', 'SUN', 'SUNDAY').

#### Examples

```sql
SELECT NEXT_DAY('2015-01-14 12:05:55', 'TU') -- 2015-01-20
```

### NOW

Returns the current timestamp.

#### Syntax

```sql
NOW() → timestamp
```

#### Examples

```sql
SELECT NOW() -- 2021-07-02 04:55:55.267000
```

### NTILE

Divides an ordered data set into a number of buckets indicated by `buckets` and assigns the appropriate bucket number to each row.

#### Syntax

```sql
NTILE(buckets) OVER (PARTITION BY partition_expression ORDER BY order_expression) → int
```

#### Parameters

- `buckets`: A positive integer literal.
- `partition_expression` (optional): An expression that groups rows into partitions.
- `order_expression`: An expression that specifies the order of the rows within each partition.

#### Examples

```sql
SELECT "Category", "Descript", "DayOfWeek", NTILE(1) OVER ( PARTITION BY "Category" ORDER BY "DayOfWeek") FROM Samples."samples.dremio.com"."SF_incidents2016.json"
```

### NULLIF

Returns NULL if the two expressions are equal, otherwise returns the first expression.

#### Syntax

```sql
NULLIF(expression1, expression2) → same as input type
```

#### Parameters

- `expression1`: The first expression.
- `expression2`: The second expression.

#### Examples

```sql
SELECT NULLIF(user_id, customer_id)
```

### NVL

Returns the first non-null expression. Alias for COALESCE.

#### Syntax

```sql
NVL(expression1, expression2) → same as input type
```

#### Parameters

- `expression1`: The first expression.
- `expression2`: The second expression.

#### Examples

```sql
SELECT NVL(NULL, 2) -- 2
SELECT NVL(5, 2) -- 5
```

### NVL2

Not supported. Use `CASE` or `NVL`/`COALESCE`.

### OCTET_LENGTH

Returns the length of a string in bytes (octets).

#### Syntax

```sql
OCTET_LENGTH(input varchar) → int32
```

#### Parameters

- `input`: The string for which the length is returned.

#### Examples

```sql
SELECT OCTET_LENGTH('abc') -- 3
```

### OVERLAY

Not supported. Use `SUBSTR` or `SUBSTRING`.

### PERCENT_RANK

Calculates the percent rank of a value in a group of values.

#### Syntax

```sql
PERCENT_RANK() OVER ( [PARTITION BY partition_expression] [ORDER BY order_expression]) → double
```

#### Parameters

- `partition_expression` (optional): An expression that groups rows into partitions.
- `order_expression`: An expression that specifies the order of the rows within each partition.

#### Examples

```sql
SELECT "Category", "Descript", "DayOfWeek", PERCENT_RANK() OVER ( PARTITION BY "Category" ORDER BY "DayOfWeek") FROM Samples."samples.dremio.com"."SF_incidents2016.json"
```

### PI

Returns the value of PI.

#### Syntax

```sql
PI() → double
```

#### Examples

```sql
SELECT PI() -- 3.141592653589793
```

### POSITION

Returns the position of a substring within a string.

#### Syntax

```sql
POSITION(substr string IN expression string) → integer
```

#### Parameters

- `substr`: The substring to search for in the expression.
- `expression`: The input expression to search.

#### Examples

```sql
select position('an' in 'banana') -- 2
select position('no' in 'banana') -- 0
```

### POW

Alias for POWER.

### POWER

Returns the value of a number raised to a power.

#### Syntax

```sql
POWER(numeric_expression, power) → double
```

#### Parameters

- `numeric_expression`: The base number.
- `power`: The exponent.

#### Examples

```sql
SELECT POWER(5, 2) -- 25.0
SELECT POWER(10, -2) -- 0.01
```

### QUARTER

Extracts the quarter from a time, timestamp, or date.

#### Syntax

```sql
EXTRACT(QUARTER FROM date_timestamp_expression string) → bigint
```

#### Parameters

- `date_timestamp_expression`: A DATE or TIMESTAMP expression.

#### Examples

```sql
SELECT EXTRACT(QUARTER FROM TIMESTAMP '2019-08-12 01:00:00.123456') -- 3
SELECT EXTRACT(QUARTER FROM DATE '2019-08-12') -- 3
SELECT EXTRACT(QUARTER FROM CAST('2019-08-12 01:00:00' AS TIMESTAMP)) -- 3
```

### RADIANS

Converts degrees to radians.

#### Syntax

```sql
RADIANS(x number) → float
```

#### Parameters

- `x`: The number in degrees.

#### Examples

```sql
select radians(45) -- 0.7853981633974483
```

### RAND

Alias for RANDOM.

### RANK

Returns the rank of a value in a group of values.

#### Syntax

```sql
RANK() OVER ( [PARTITION BY partition_expression] [ORDER BY order_expression]) → bigint
```

#### Parameters

- `partition_expression` (optional): An expression that groups rows into partitions.
- `order_expression`: An expression that specifies the order of the rows within each partition.

#### Examples

```sql
SELECT "Category", "Descript", "DayOfWeek", RANK() OVER ( PARTITION BY "Category" ORDER BY "DayOfWeek") FROM Samples."samples.dremio.com"."SF_incidents2016.json"
```

### REGEXP_COL_LIKE

Matches a string against a regular expression contained in a column.

#### Syntax

```sql
REGEXP_COL_LIKE(input string, regex string) → boolean
```

#### Parameters

- `input`: The string to test.
- `regex`: The column containing the Perl-compatible regular expression (PCRE) to use for the test.

#### Examples

```sql
SELECT Category, REGEXP_COL_LIKE('WARRANTS', Category) FROM Samples."samples.dremio.com"."SF_incidents2016.json" LIMIT 3
```

### REGEXP_LIKE

Matches a string against a regular expression.

#### Syntax

```sql
REGEXP_LIKE(input string, regex string) → boolean
```

#### Parameters

- `input`: The string to test.
- `regex`: The Perl-compatible regular expression (PCRE) to use for the test. Must be a literal.

#### Examples

```sql
SELECT REGEXP_LIKE('the data lakehouse', '.*?\\Qlake\\E.*?') -- True
```

### REGEXP_MATCH

Alias for REGEXP_MATCHES or REGEXP_LIKE.

### REGEXP_REPLACE

Replaces substrings matching a regular expression.

#### Syntax

```sql
REGEXP_REPLACE(input string, regex string, replacement_string string) → string
```

#### Parameters

- `input`: The expression to search for a matching string.
- `regex`: The Perl-compatible regular expression (PCRE) to match against.
- `replacement_string`: The string with which to replace the matching string.

#### Examples

```sql
SELECT REGEXP_REPLACE('8AM-4PM', '\\Q-\\E', ' to ') -- 8AM to 4PM
```

### REGEXP_SPLIT

Splits a string using a regular expression.

#### Syntax

```sql
REGEXP_SPLIT(input string, regex string, keyword string, integer integer) → array
```

#### Parameters

- `input`: The string that you want to split by means of the regular expression.
- `regex`: The regular expression to use to split the string.
- `keyword`: The keyword that determines where or how many times to use the regular expression to split the string. Can be FIRST, LAST, INDEX, or ALL.
- `integer`: The value specified for the keyword.

#### Examples

```sql
SELECT REGEXP_SPLIT('REGULAR AIR', 'R', 'FIRST', -1) AS R_LESS_SHIPMENT_TYPE -- ['', 'EGULAR AIR']
```

### REPEAT

Repeats a string a specified number of times.

#### Syntax

```sql
REPEAT(expression varchar, nTimes int32) → varchar
```

#### Parameters

- `expression`: The input string from which the output string is built.
- `nTimes`: The number of times the input expression should be repeated.

#### Examples

```sql
SELECT REPEAT('abc', 3) -- abcabcabc
```

### REPLACE

Replaces all occurrences of a specified string.

#### Syntax

```sql
REPLACE(string_expression varchar, pattern varchar, replacement varchar) → varchar
```

#### Parameters

- `string_expression`: String expression in which to do the replacements.
- `pattern`: The substring you want replaced in the string_expression.
- `replacement`: The string to replace the occurrences of the pattern substring with.

#### Examples

```sql
SELECT REPLACE('THE CATATONIC CAT', 'CAT', 'DOG')
```

### REVERSE

Reverses a string.

#### Syntax

```sql
REVERSE(expression varchar) → varchar
```

#### Parameters

- `expression`: The string to reverse.

#### Examples

```sql
SELECT REVERSE('Hello, world!'); -- !dlrow ,olleH
```

### RIGHT

Returns the specified number of characters from the right of a string.

#### Syntax

```sql
RIGHT(string varchar, length int64) → varchar
```

#### Parameters

- `string`: String input parameter.
- `length`: Number of characters on the right to return.

#### Examples

```sql
SELECT "RIGHT"('Dremio - SQL Engine', 6) -- Engine
```

### ROUND

Rounds a number to a specified number of decimal places.

#### Syntax

```sql
ROUND(numeric_expression decimal(0,0), scale int32) → decimal(0,0)
ROUND(numeric_expression int32, scale int32) → int32
ROUND(numeric_expression int32) → int32
ROUND(numeric_expression double) → double
```

#### Parameters

- `numeric_expression`: Numeric value to round.
- `scale`: The decimal place to round.

#### Examples

```sql
SELECT ROUND(-24.35, -1) -- -24.4
SELECT ROUND(24.35, 1) -- 24.4
SELECT ROUND(24, 0) -- 0
```

### ROW_NUMBER

Returns the row number for the current row in a partition.

#### Syntax

```sql
ROW_NUMBER() OVER ( [PARTITION BY partition_expression] [ORDER BY order_expression]) → bigint
```

#### Parameters

- `partition_expression` (optional): An expression that groups rows into partitions.
- `order_expression` (optional): An expression that specifies the order of the rows within each partition.

#### Examples

```sql
SELECT "Category", "Descript", "DayOfWeek", ROW_NUMBER() OVER ( PARTITION BY "Category" ORDER BY "DayOfWeek") FROM Samples."samples.dremio.com"."SF_incidents2016.json"
```

### RPAD

Right-pads a string with another string to a specified length.

#### Syntax

```sql
RPAD(base_expression varchar, length int64 [, pad_expression varchar]) → varchar
```

#### Parameters

- `base_expression`: The expression to pad.
- `length`: The number of characters to return.
- `pad_expression` (optional): Characters to pad the base_expression with.

#### Examples

```sql
select RPAD('dremio', 9, '!') -- dremio!!!
select RPAD('base_', 9, 'expression') -- base_expr
select RPAD('dremio', 9) -- dremio
```

### RTRIM

Removes trailing characters from a string.

#### Syntax

```sql
RTRIM(expression varchar [, trim_expression varchar]) → varchar
```

#### Parameters

- `expression`: The expression to be trimmed.
- `trim_expression` (optional): Trailing characters to trim. If this parameter is not specified, then spaces will be trimmed from the input expression.

#### Examples

```sql
SELECT RTRIM('pancake', 'cake') -- pan
SELECT RTRIM('pancake pan', 'abnp') -- pancake
SELECT RTRIM('dremio ') -- dremio
```

### SEARCH

Not a direct function. Use LOCATE or POSITION.

### SEC

Alias for SECOND.

### SECOND

Extracts the second from a time, timestamp, or date.

#### Syntax

```sql
EXTRACT(SECOND FROM date_timestamp_expression string) → bigint
```

#### Parameters

- `timestamp_expression`: A TIME, TIMESTAMP, or DATE expression.

#### Examples

```sql
SELECT EXTRACT(SECOND FROM TIMESTAMP '2019-08-12 01:10:30.123456') -- 1
SELECT EXTRACT(SECOND FROM TIME '01:10:30.123456') -- 1
SELECT EXTRACT(SECOND FROM CAST('2019-08-12 01:10:30' AS TIMESTAMP)) -- 1
```

### SHA1

Computes the SHA-1 hash of a string.

#### Syntax

```sql
SHA1(expression varchar) → varchar
```

#### Parameters

- `expression`: The string to hash.

#### Examples

```sql
SELECT SHA1('Dremio') -- dda3f1ef53d1e82a4845ef5b2893b9d9c04bd3b1
```

### SHA256

Computes the SHA-256 hash of a string.

#### Syntax

```sql
SHA256(expression varchar) → varchar
```

#### Parameters

- `expression`: The string to hash.

#### Examples

```sql
SELECT SHA256('Dremio') -- ffae26c65c486a4d9143cbb1a6829166f17dab711910fdfc5787b1a249bd9921
```

### SIGN

Returns the sign of a number.

#### Syntax

```sql
SIGN(numeric_expression double) → int
SIGN(numeric_expression int32) → int32
SIGN(numeric_expression int64) → int64
SIGN(numeric_expression float) → int
```

#### Parameters

- `numeric_expression`: Input expression.

#### Examples

```sql
SELECT SIGN(10.3) -- 1
SELECT SIGN(-5) -- -1
SELECT SIGN(24) -- 1
SELECT SIGN(0.0) -- 0
```

### SIN

Returns the sine of a number (in radians).

#### Syntax

```sql
SIN(numeric_expression int32) → double
SIN(numeric_expression float) → double
SIN(numeric_expression int64) → double
SIN(numeric_expression double) → double
```

#### Parameters

- `numeric_expression`: The number in radians.

#### Examples

```sql
SELECT SIN(360) -- 0.9589157234143065
SELECT SIN(510.89) -- 0.9282211721815067
```

### SINH

Returns the hyperbolic sine of a number.

#### Syntax

```sql
SINH(numeric_expression int32) → double
SINH(numeric_expression float) → double
SINH(numeric_expression double) → double
SINH(numeric_expression int64) → double
```

#### Parameters

- `numeric_expression`: Input expression.

#### Examples

```sql
SELECT SINH(1) -- 1.1752011936438014
SELECT SINH(1.5) -- 2.1292794550948173
```

### SIZE

Returns the number of entries in a map.

#### Syntax

```sql
SIZE(input map) → int
```

#### Parameters

- `input`: A map expression for which to return the number of entries.

#### Examples

```sql
SELECT SIZE(properties)
```

### SPLIT_PART

Splits a string by a delimiter and returns the specified part.

#### Syntax

```sql
SPLIT_PART(expression varchar, delimiter varchar, part_number int32) → varchar
```

#### Parameters

- `expression`: Input expression.
- `delimiter`: String representing the delimiter to split the input expression by.
- `part_number`: Requested part of the split. Must be an integer greater than zero.

#### Examples

```sql
SELECT SPLIT_PART('127.0.0.1', '.', 1) -- 127
```

### SQRT

Returns the square root of a number.

#### Syntax

```sql
SQRT(numeric_expression double) → double
SQRT(numeric_expression int64) → int64
SQRT(numeric_expression int32) → int32
SQRT(numeric_expression float) → float
```

#### Parameters

- `numeric_expression`: Numeric expression to calculate the square root for.

#### Examples

```sql
SELECT SQRT(25.25) -- 5.024937810560445
SELECT SQRT(-25.25) -- NaN
SELECT SQRT(25) -- 5
```

### STDDEV

Returns the sample standard deviation of a numeric column.

#### Syntax

```sql
STDDEV(col_name NUMERIC) → DOUBLE
```

#### Parameters

- `col_name`: The name of the column for which to return the standard deviation. The values in the column must be numbers, such as INT, DOUBLE, or FLOAT.

#### Examples

```sql
SELECT STDDEV(tip_amount) FROM Samples."samples.dremio.com"."NYC-taxi-trips"; -- 2.2596650338662974
```

### STDDEV_POP

Returns the population standard deviation of a numeric column.

#### Syntax

```sql
STDDEV_POP(col_name NUMERIC) → DOUBLE
```

#### Parameters

- `col_name`: The name of the column for which to return the population standard deviation. The values in the column must be numbers, such as INT, DOUBLE, or FLOAT.

#### Examples

```sql
SELECT STDDEV_POP(tip_amount) FROM Samples."samples.dremio.com"."NYC-taxi-trips" -- 2.259665030506379
```

### STDDEV_SAMP

Returns the sample standard deviation of a numeric column.

#### Syntax

```sql
STDDEV_SAMP(col_name NUMERIC) → DOUBLE
```

#### Parameters

- `col_name`: The name of the column for which to return the sample standard deviation. The values in the column must be numbers, such as INT, DOUBLE, or FLOAT.

#### Examples

```sql
SELECT STDDEV_SAMP(tip_amount) FROM Samples."samples.dremio.com"."NYC-taxi-trips" -- 2.259665033866297
```

### STRING_BINARY

Converts a binary value to a string.

#### Syntax

```sql
STRING_BINARY(bytes BYTES) → STRING
```

#### Parameters

- `bytes`: Bytes to convert to a string.

#### Examples

```sql
SELECT STRING_BINARY(BINARY_STRING('Dremio')) -- Dremio
SELECT STRING_BINARY(FROM_HEX('54455354111213')) -- TEST\x11\x12\x13
```

### SUBSTR

Extracts a substring from a string.

#### Syntax

```sql
SUBSTR(string_expression varchar, offset int64) → varchar
SUBSTR(string_expression varchar, offset int64, length int64) → varchar
SUBSTR(string_expression varchar, pattern varchar) → varchar
```

#### Parameters

- `string_expression`: Base expression to extract substring from.
- `offset`: The offset from which the substring starts.
- `length` (optional): The length limit of the substring.
- `pattern`: Regex pattern to match.

#### Examples

```sql
SELECT SUBSTR('dremio user 1 2 3', 12) -- 1 2 3
SELECT SUBSTR('base expression', 6, 4) -- expr
SELECT SUBSTR('dremio user 123', '[0-9]+') -- 123
```

### SUBSTRING

Extracts a substring from a string.

#### Syntax

```sql
SUBSTRING(string_expression varchar, offset int64) → varchar
SUBSTRING(string_expression varchar FROM offset int64) → varchar
SUBSTRING(string_expression varchar, offset int64, length int64) → varchar
```

#### Parameters

- `string_expression`: Base expression to extract substring from.
- `offset`: The offset from which the substring starts.
- `length` (optional): The length limit of the substring.

#### Examples

```sql
SELECT SUBSTRING('dremio user 1 2 3', 12) -- 1 2 3
SELECT SUBSTRING('dremio user 1 2 3' FROM 12) -- 1 2 3
SELECT SUBSTRING('base expression', 6, 4) -- expr
```

### SUM

Returns the sum of values in a column.

#### Syntax

```sql
SUM(col_name NUMERIC) → same as input except for INT, which returns BIGINT
```

#### Parameters

- `col_name`: The name of the column for which to return the sum. The values in the column must be numbers, such as INT, DOUBLE, or FLOAT.

#### Examples

```sql
SELECT SUM(trip_distance_mi) FROM Samples."samples.dremio.com"."NYC-taxi-trips"; -- 9.858134477692287E8
```

### TAN

Returns the tangent of a number (in radians).

#### Syntax

```sql
TAN(numeric_expression double) → double
TAN(numeric_expression int64) → double
TAN(numeric_expression int32) → double
TAN(numeric_expression float) → double
```

#### Parameters

- `numeric_expression`: The number in radians.

#### Examples

```sql
SELECT TAN(180.8) -- -6.259341891872157
SELECT TAN(1200) -- -0.08862461268886584
```

### TANH

Returns the hyperbolic tangent of a number.

#### Syntax

```sql
TANH(numeric_expression double) → double
TANH(numeric_expression int64) → double
TANH(numeric_expression float) → double
TANH(numeric_expression int32) → double
```

#### Parameters

- `numeric_expression`: Input expression to calculate tanh for.

#### Examples

```sql
SELECT TANH(1.5); -- 0.9051482536448664
SELECT TANH(1); -- 0.7615941559557649
```

### TIMESTAMPADD

Adds a specified number of units to a timestamp.

#### Syntax

```sql
TIMESTAMPADD(unit symbol, count integer, givenTime date or timestamp) → date or timestamp
```

#### Parameters

- `unit`: The unit of the interval. Must be one of the following: YEAR, QUARTER, MONTH, WEEK, DAY, HOUR, MINUTE, SECOND.
- `count`: Number of units to be added (or subtracted) from givenTime. To subtract units, pass a negative number.
- `givenTime`: Value to which to add units (either a database column in DATE or TIMESTAMP format, or literal value explicitly converted to DATE or TIMESTAMP).

#### Examples

```sql
SELECT TIMESTAMPADD(DAY, 1, DATE '2021-04-01') -- 2021-04-02
SELECT TIMESTAMPADD(HOUR, -2, TIMESTAMP '2021-04-01 17:14:32') -- 2021-04-01 15:14:32
```

### TIMESTAMPDIFF

Returns the difference between two timestamps in the specified unit.

#### Syntax

```sql
TIMESTAMPDIFF(unit symbol, giventime1 date or timestamp, givenTime2 date or timestamp) → integer
```

#### Parameters

- `unit`: The unit of the interval. Must be one of the following: YEAR, QUARTER, MONTH, WEEK, DAY, HOUR, MINUTE, SECOND.
- `giventime1`: The first DATE or TIMESTAMP (subtrahend).
- `givenTime2`: The second DATE or TIMESTAMP (minuend).

#### Examples

```sql
SELECT TIMESTAMPDIFF(MONTH, DATE '2021-02-01', DATE '2021-05-01'); -- 3
SELECT TIMESTAMPDIFF(DAY, TIMESTAMP '2003-02-01 11:43:22', TIMESTAMP '2005-04-09 12:05:55'); -- 798
```

### TO_BINARY

Not a direct function. Use `CONVERT_TO` or `BINARY_STRING`.

### TO_CHAR

Converts an expression to a string using a specified format.

#### Syntax

```sql
TO_CHAR(expression time, format varchar) → varchar
TO_CHAR(expression date, format varchar) → varchar
TO_CHAR(expression int32, format varchar) → varchar
TO_CHAR(expression float, format varchar) → varchar
TO_CHAR(expression int64, format varchar) → varchar
TO_CHAR(expression double, format varchar) → varchar
TO_CHAR(expression timestamp, format varchar) → varchar
```

#### Parameters

- `expression`: Expression to convert to a string.
- `format`: Format to use for the conversion.

#### Examples

```sql
SELECT TO_CHAR(CAST('01:02:03' AS TIME) , 'HH:MI'); -- 01:02
SELECT TO_CHAR(CAST('2021-02-11' AS DATE) , 'yyyy.mm.dd'); -- 2021.02.11
SELECT TO_CHAR(10, '#') -- 10
SELECT TO_CHAR(7.5, '#.#') -- 7.5
```

### TO_DATE

Converts an expression to a date.

#### Syntax

```sql
TO_DATE(in timestamp) → date
TO_DATE(numeric_expression int32) → date
TO_DATE(numeric_expression float) → date
TO_DATE(numeric_expression int64) → date
TO_DATE(string_expression varchar, format varchar, replaceErrorWithNull int32) → date
TO_DATE(string_expression varchar, format varchar) → date
TO_DATE(numeric_expression double) → date
```

#### Parameters

- `in`: The date is extracted from the timestamp.
- `numeric_expression`: A Unix epoch timestamp.
- `string_expression`: The string from which to extract the date.
- `format`: String to specify format of the date.
- `replaceErrorWithNull`: If 0, the function will fail when given malformed input. If 1, the function will return NULL when given the malformed input.

#### Examples

```sql
SELECT TO_DATE(TIMESTAMP '2022-05-17 19:15:00.000') -- 2022-05-17
SELECT TO_DATE(1640131200) -- 2021-12-22
SELECT TO_DATE('05/24/22', 'MM/DD/YY') -- 2022-05-24
```

### TO_HEX

Converts a binary value to a hexadecimal string.

#### Syntax

```sql
TO_HEX(in binary) → string
```

#### Parameters

- `in`: A binary value

#### Examples

```sql
select to_hex(binary_string('hello')) -- 68656C6C6F
```

### TO_NUMBER

Converts a string to a number.

#### Syntax

```sql
TO_NUMBER(expression varchar, format varchar) → double
```

#### Parameters

- `expression`: String to convert to a number.
- `format`: Format for number conversion.

#### Examples

```sql
SELECT TO_NUMBER('12374.0023', '#####.###') -- 12374.002
SELECT TO_NUMBER('12374', '#####') -- 12374.0
```

### TO_TIME

Converts an expression to a time.

#### Syntax

```sql
TO_TIME(numeric_expression int32) → time
TO_TIME(numeric_expression int64) → time
TO_TIME(string_expression varchar, format varchar, replaceErrorWithNull int32) → time
TO_TIME(string_expression varchar, format varchar) → time
TO_TIME(numeric_expression double) → time
TO_TIME(numeric_expression float) → time
```

#### Parameters

- `numeric_expression`: A Unix epoch timestamp.
- `string_expression`: The string from which to extract the time.
- `format`: String to specify format of the time.
- `replaceErrorWithNull`: If 0, the function will fail when given malformed input. If 1, the function will return NULL when given malformed input.

#### Examples

```sql
SELECT TO_TIME(1665131223) -- 08:27:03
SELECT TO_TIME('09:15:00', 'HH:MI:SS') -- 09:15:00
```

### TO_TIMESTAMP

Converts an expression to a timestamp.

#### Syntax

```sql
TO_TIMESTAMP(numeric_expression double) → timestamp
TO_TIMESTAMP(string_expression varchar, format varchar [, replaceErrorWithNull int32]) → timestamp
TO_TIMESTAMP(numeric_expression int64) → timestamp
TO_TIMESTAMP(numeric_expression int32) → timestamp
TO_TIMESTAMP(numeric_expression float) → timestamp
```

#### Parameters

- `numeric_expression`: A Unix epoch timestamp.
- `string_expression`: The string from which to extract the timestamp.
- `format`: String to specify format of the timestamp.
- `replaceErrorWithNull` (optional): If 0, the function will fail when given malformed input. If 1, the function will return NULL when given malformed input.

#### Examples

```sql
SELECT TO_TIMESTAMP(52 * 365.25 * 86400) -- 2022-01-01 00:00:00
SELECT TO_TIMESTAMP(1640131200) -- 2021-12-22 00:00:00
```

### TRANSACTION_TIMESTAMP

Returns the timestamp of the start of the current transaction.

#### Syntax

```sql
TRANSACTION_TIMESTAMP() → timestamp
```

#### Examples

```sql
SELECT TRANSACTION_TIMESTAMP() -- 2021-07-13 06:52:10.694000
```

### TRANSLATE

Replaces a sequence of characters in a string with another set of characters.

#### Syntax

```sql
TRANSLATE(base_expression varchar, source_characters varchar, target_characters varchar) → varchar
```

#### Parameters

- `base_expression`: The string to translate.
- `source_characters`: A string with all the characters in the base expression that need translating.
- `target_characters`: A string containing all the characters to replace the original characters with.

#### Examples

```sql
SELECT TRANSLATE('*a*bX*dYZ*','XYZ*','cef'); -- abcdef
```

### TRIM

Removes leading, trailing, or both spaces or specified characters from a string.

#### Syntax

```sql
TRIM(LEADING or TRAILING or BOTH trim_expression varchar FROM expression varchar) → varchar
```

#### Parameters

- `trim_expression` (optional): The characters to trim.
- `expression`: The expression to be trimmed.

#### Examples

```sql
SELECT TRIM(' pancake ') -- pancake
SELECT TRIM(leading 'pan' from 'pancake') -- cake
SELECT TRIM(trailing 'cake' from 'pancake') -- pan
SELECT TRIM(both 'pan' from 'pancake pan') -- cake
```

### TRUNC

Alias for TRUNCATE (numeric) or DATE_TRUNC (date).

### TRUNCATE

Truncates a number to a specified scale.

#### Syntax

```sql
TRUNCATE(numeric_expression float) → int
TRUNCATE(numeric_expression double) → int
TRUNCATE(numeric_expression int32) → int32
TRUNCATE(numeric_expression int64) → int64
TRUNCATE(numeric_expression decimal(0,0) [, scale_expression int32]) → decimal(0,0)
TRUNCATE(numeric_expression float [, scale_expression int32]) → float
TRUNCATE(numeric_expression double [, scale_expression int32]) → double
```

#### Parameters

- `numeric_expression`: The numeric expression to truncate.
- `scale_expression` (optional): The decimal place to round to.

#### Examples

```sql
SELECT TRUNCATE(987.65) -- 987
SELECT TRUNCATE(89.2283211, 2) -- 89.22
SELECT TRUNCATE(2021, -1) -- 2020
```

### UPPER

Converts a string to uppercase.

#### Syntax

```sql
UPPER(expression varchar) → varchar
```

#### Parameters

- `expression`: String to convert to uppercase.

#### Examples

```sql
SELECT UPPER('a guide to data lakehouses') -- A GUIDE TO DATA LAKEHOUSES
```

### VAR_POP

Returns the population variance of a numeric column.

#### Syntax

```sql
VAR_POP(col_name NUMERIC) → NUMERIC
```

#### Parameters

- `col_name`: The name of the column for which to return the population variance. The values in the column must be numbers, such as INT, DOUBLE, or FLOAT.

#### Examples

```sql
SELECT VAR_POP(pop) FROM Samples."samples.dremio.com"."zips.json"; -- 1.5167869917122573E8
```

### VAR_SAMP

Returns the sample variance of a numeric column.

#### Syntax

```sql
VAR_SAMP(col_name NUMERIC) → NUMERIC
```

#### Parameters

- `col_name`: The name of the column for which to return the sample variance. The values in the column must be numbers, such as INT, DOUBLE, or FLOAT.

#### Examples

```sql
SELECT VAR_SAMP(passenger_count) FROM Samples."samples.dremio.com"."NYC-taxi-trips"; -- 1.868747683518558
```

### VARIANCE

Alias for VAR_SAMP.

### WEEK

Extracts the week from a date or timestamp.

#### Syntax

```sql
EXTRACT(WEEK FROM date_timestamp_expression string) → bigint
```

#### Parameters

- `date_timestamp_expression`: A DATE or TIMESTAMP expression.

#### Examples

```sql
SELECT EXTRACT(WEEK FROM TIMESTAMP '2019-08-12 01:00:00.123456') -- 33
SELECT EXTRACT(WEEK FROM DATE '2019-08-12') -- 33
```

### YEAR

Extracts the year from a date or timestamp.

#### Syntax

```sql
EXTRACT(YEAR FROM date_timestamp_expression string) → bigint
```

#### Parameters

- `date_timestamp_expression`: A DATE or TIMESTAMP expression.

#### Examples

```sql
SELECT EXTRACT(YEAR FROM TIMESTAMP '2019-08-12 01:00:00.123456') -- 2019
SELECT EXTRACT(YEAR FROM DATE '2019-08-12') -- 2019
```

