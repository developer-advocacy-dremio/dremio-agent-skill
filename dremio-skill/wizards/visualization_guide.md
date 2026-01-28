# Wizard: Visualization & Dashboard Guide

This wizard guides the Agent in helping the user design effective effective visualizations, ask the user for the following information before proceeding to build out and run the python scripts to build out the desired visualizations:

## 1. Discovery Phase (Ask the User - REQUIRED)
**Do not recommend chart types** until you know the audience.

1.  **Audience**: "Who is looking at this? (Executives need KPIs, Analysts need Tables/Drill-downs)"
2.  **Decision**: "What decision are they trying to make? (e.g., 'Which region to fund?' or 'Is the server down?')"
3.  **Tool**: "Are you using Tableau, PowerBI, Superset, or something else?"
4.  **Latency**: "Does this need to be real-time (Direct Query) or is an extract okay?"

## 2. Data Structure Strategy

### The "One Big Table" (OBT) vs Star Schema
*   **Dremio Recommendation**: Dremio handles **OBT** (wide, denormalized tables) extremely well due to Columnar storage and Reflections. This is often easier for BI tools than complex Star Schemas.
*   *Action*: Recommend creating a single "Dashboard View" in the Gold layer that pre-joins all lookups.

### Semantic Layer Alignment
Ensure column names are "Business Ready".
-   `cust_id_val_12` -> `Customer ID`
-   `amt` -> `Total Sales Amount ($)`

## 3. Chart Selection Guide

### A. Comparisons (Ranking)
*Metric*: "Who is the best salesperson?"
*Chart*: **Bar Chart** (Horizontal allows for long names).

### B. Trends (Time Series)
*Metric*: "Are sales growing?"
*Chart*: **Line Chart** or Area Chart.
*Dremio Tip*: Pre-aggregate data by Day/Month in a Reflection to make these instant.

### C. Parts-to-Whole (Composition)
*Metric*: "What share of revenue is Tech?"
*Chart*: **Stacked Bar** (Better than Pie charts for comparison over time).

### D. Correlations
*Metric*: "Does discount drive volume?"
*Chart*: **Scatter Plot**.

## 4. Performance Checklist
Before publishing the dashboard:
1.  Is the BI tool using **Direct Query**? (Leverages Dremio engine).
2.  Is there an **Aggregate Reflection** covering the main `GROUP BY` dimensions of the charts?
3.  Are high-cardinality filters (like User ID) backed by a **Raw Reflection** (sorted)?
