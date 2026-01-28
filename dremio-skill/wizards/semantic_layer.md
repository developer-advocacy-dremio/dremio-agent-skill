# Semantic Layer Wizard

Use this wizard when the user wants to organize their data, create views, or build a "Lakehouse" structure.

## 1. Context & Goal
The goal is to move from raw data to business-friendly data using the **Medallion Architecture** (Bronze -> Silver -> Gold) via Virtual Datasets (Views).

## 2. Discovery Phase (Ask the User)
If the user hasn't provided details, ask:
1.  **Sources**: "What are your raw data sources? (S3, Postgres, Snowflake, etc.)"
2.  **Grain**: "What is the primary entity? (e.g., One row per Transaction, per Customer?)"
3.  **Business Logic**: "What cleaning or joins are needed for the 'Silver' layer?"
4.  **Consumption**: "Who will query the 'Gold' layer? (BI Dashboards, Data Scientists?)"

## 3. Implementation Pattern

### A. Space Hierarchy
Recommend creating the following Spaces if they don't exist:
-   `Raw` or `bronze` (SELECT * views of source tables)
-   `Business` or `silver`(Silver - Cleaned, joined, governed)
-   `Application` or `gold`(Gold - Aggregated, report-ready)

### B. Naming Convention
-   **Views**: `Use_Snake_Case` (e.g., `customer_360`, `daily_sales`)
-   **Columns**: Lowercase snake_case.

### C. Folder Structure
```text
Space: Analytics
  └── Folder: Bronze (Raw Refinement)
      └── View: trips_casted (Casts types, standardizes names)
  └── Folder: Silver (Enriched)
      └── View: trips_enriched (Joins with Customer/Weather)
  └── Folder: Gold (Aggregated)
      └── View: trips_by_zone (Aggregates for BI)
```

## 4. Execution Steps (For the Agent)
1.  **Explore**: Use `list_catalog` to find source PDS paths.
2.  **Draft SQL**:
    -   *Bronze*: Create views that just do `CAST(col AS TYPE)` and rename columns.
    -   *Silver*: Perform `JOIN`s and `CASE WHEN` logic.
    -   *Gold*: Perform `GROUP BY` and `SUM/COUNT` logic.
3.  **Validate**: Verify SQL syntax (check `knowledge/sql/sql_commands.md`) before running.
4.  **Create**: Use `create_view(path, sql)` or generate Python code to apply changes.
