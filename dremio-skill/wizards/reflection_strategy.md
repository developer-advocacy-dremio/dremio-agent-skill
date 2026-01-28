# Reflection Strategy Wizard

Use this wizard when the user complains about slow queries or asks to "optimize" performance.

## 1. Context & Goal
Reflections are Dremio's query accelerators (materialized views). The goal is to speed up workloads without changing user SQL.

## 2. Discovery Phase (Ask the User)
1.  **Workload Type**: "Are the slow queries mostly Aggregations (Dashboards) or Row-Level lookups?"
2.  **Freshness**: "How often does the underlying data change? (Real-time, Hourly, Daily?)"
3.  **Pain Point**: "Is there a specific dashboard or table that is slow?"

## 3. Analysis & Recommendation

### Scenario A: Slow BI Dashboards (GROUP BY / SUM)
-   **Solution**: **Aggregation Reflection**
-   **Target**: The physical table (PDS) or the lowest-level view closer to the source.
-   **Config**:
    -   *Dimensions*: Columns used in `GROUP BY`.
    -   *Measures*: Columns used in `SUM`, `COUNT`, `AVG`.

### Scenario B: Slow Point Lookups (WHERE id = X)
-   **Solution**: **Raw Reflection**
-   **Target**: The PDS or Silver view.
-   **Config**:
    -   *Display*: Columns selected in the final output.
    -   *Partition*: Columns frequently filtered (date, region).
    -   *Sort*: High-cardinality filter columns (user_id).

## 4. Execution Steps (For the Agent)
1.  **Analyze**: Use `get_job_details` or `optimize_sql(query)` to see query cost.
2.  **Identify Dataset**: Find the source PDS/VDS being queried.
3.  **Propose**:
    ```python
    # Example Recommendation
    client.catalog.create_reflection(
        dataset_id="...",
        type="AGGREGATION",
        name="agg_dashboard_accel",
        dimensions=["region", "date"],
        measures=["sales"]
    )
    ```
4.  **Verify**: Check `sys.reflections` to see if it refreshes successfully.
