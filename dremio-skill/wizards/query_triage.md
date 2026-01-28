# Wizard: Query Performance Triage

This wizard guides the Agent in diagnosing and resolving slow query performance issues in Dremio.

## 1. Discovery Phase (Ask the User - REQUIRED)
Before recommending any fixes, ask the following questions to understand the context. **Do not proceed** until you have these answers.

1.  **Symptom**: "Is the query slow during 'Planning', 'Execution', or 'Queueing'?" (If unknown, ask for a Job ID to check the profile).
2.  **Frequency**: "Is this a consistent slowness or intermittent?"
3.  **Scope**: "Is it a specific query, or are all queries against this dataset slow?"
4.  **Changes**: "Did this query work well before? Did the data volume change recently?"
5.  **Target**: "What is the target response time (SLA)?"

## 2. Analysis Phase (Agent Actions)
Once the user provides the context (or a Job ID), guide them through analyzing the Query Profile.

### A. Phase Timing
-   **High Planning Time**: Suggest checking for too many reflections to match, or metadata operations.
-   **High Queue Time**: Suggest checking Workload Management (WLM) limits (see `workload_management.md`).
-   **High Execution Time**: Proceed to Operator Analysis.

### B. Operator Analysis (The Critical Path)
Ask the user to look at the "Longest Path" in the profile.
-   **Slow Scan**:
    -   *Cause*: Reading too many small files or non-pruned partitions.
    -   *Fix*: Suggest **Partitioning** the source, running **`OPTIMIZE`** (Compaction), or creating a **Raw Reflection** sorted by filter columns.
-   **Slow Aggregation (HashAgg/Sort)**:
    -   *Cause*: Heavy computation on raw data.
    -   *Fix*: Suggest an **Aggregation Reflection** covering the dimensions and measures.
-   **Slow Exchange (Network)**:
    -   *Cause*: Moving large data between nodes.
    -   *Fix*: Check if **Broadcast Join** is being forced erroneously, or if data skew exists.

## 3. Implementation Patterns

### Pattern A: Creating a Raw Reflection (For Scans)
If Scans are the bottleneck:
```sql
ALTER DATASET "space"."dataset"
CREATE RAW REFLECTION "raw_acceleration"
USING DISPLAY (col1, col2, col3)
PARTITION BY (date_col)
LOCALSORT BY (filter_col);
```

### Pattern B: Creating an Aggregation Reflection (For Dashboards)
If Aggregations are the bottleneck:
```sql
ALTER DATASET "space"."dataset"
CREATE AGGREGATE REFLECTION "agg_acceleration"
USING
DIMENSIONS (region, product_type)
MEASURES (amount (SUM, COUNT), distinct_users (COUNT));
```

### Pattern C: Query Optimization
-   Avoid `SELECT *` in production dashboards.
-   Use `approx_distinct_count()` instead of `count(distinct)` if 100% precision isn't strictly required.
