# Wizard: Data Quality & Validation

This wizard guides the Agent in establishing trust in the data through automated quality checks and validation layers.

## 1. Discovery Phase (Ask the User - REQUIRED)
**Do not write validation code** until you know what "Good Data" looks like.

1.  **Critical Columns**: "Which columns *must* never be NULL? (IDs, Timestamps?)"
2.  **Business Logic**: "Are there specific rules? (e.g., 'Discount cannot be greater than Price', 'Age must be > 0')"
3.  **Freshness**: "How old is 'too old' for this data? (e.g., Data must be from Today)"
4.  **Action**: "If a row fails, should we: Filter it out? or Fail the pipeline?"

## 2. Implementation Patterns

### Pattern A: "Valid" Views (Filtering Strategy)
Use this when you want to show *only* good data to users, but keep the bad data in the background for debugging.

1.  Create a view that flags rows.
    ```sql
    CREATE VIEW "Silver".trans_validated AS
    SELECT *,
      CASE
        WHEN txn_amount < 0 THEN 'Negative Amount'
        WHEN customer_id IS NULL THEN 'Missing ID'
        ELSE 'OK'
      END as quality_status
    FROM "Bronze".transactions;
    ```
2.  Create the "Clean" view for consumers.
    ```sql
    CREATE VIEW "Gold".clean_transactions AS
    SELECT * FROM "Silver".trans_validated
    WHERE quality_status = 'OK';
    ```

### Pattern B: Pipeline Blocking (Assertion Strategy)
Use this in an Airflow/Python script to stop processing if data is bad.

```python
# Using dremioframe (Conceptual)
df = client.query("SELECT count(*) as bad_rows FROM table WHERE amount < 0")
bad_count = df['bad_rows'][0]

if bad_count > 0:
    raise Exception(f"Data Quality Check Failed! Found {bad_count} negative transactions.")
else:
    print("Data Integrity Verified. Proceeding.")
```

### Pattern C: Constraint Enforcement (Iceberg)
(If supported by the specific catalog/version)
-   `ALTER TABLE t ADD CONSTRAINT pk PRIMARY KEY (id)`
-   *Note*: Dremio often enforces these at read-time or metadata usage, not always strict write prevention depending on the source. Check version capabilities.
