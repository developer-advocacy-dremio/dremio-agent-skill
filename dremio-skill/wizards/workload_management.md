# Wizard: Workload Management (WLM) Strategy

This wizard guides the Agent in configuring Dremio's Workload Management to ensure cluster stability and meet SLAs.

## 1. Discovery Phase (Ask the User - REQUIRED)
**Do not recommend specific rules** until you understand the traffic patterns.

1.  **Workload Types**: "Do you have distinct workloads? (e.g., Fast Operational Dashboards vs. Slow Data Science Queries)"
2.  **Peak Times**: "When is your 'Rush Hour'? Do you see contention then?"
3.  **Bully Queries**: "Do specific users or tools often crash the system with massive `SELECT *` queries?"
4.  **Priorities**: "Which team's queries *must* always succeed? (e.g., C-Suite Dashboards)"

## 2. Queue Design Strategy

### A. The "Fast Lane / Slow Lane" Model
Recommend at least two custom queues:
-   **Dashboard Queue**: High concurrency, Low max-cost, Short timeout. (For sub-second interaction).
-   **Analyst Queue**: Low concurrency, High max-cost, Longer timeout. (For deep dives).

### B. Concurrency Limits
-   *Rule of Thumb*: Total slots across all queues should usually not exceed `Number of Executors * cores_per_executor`.
-   *Oversubscription*: It's okay to oversubscribe if queries are I/O bound, but be careful with CPU-heavy aggregation queries.

## 3. Implementation Steps

### Step 1: Define Queues (JSON/UI)
Guide the user to the WLM UI or API to create:
-   **Queue Name**: `Interactive_Dashboards`
-   **Max Concurrency**: `30` (Example)
-   **Max Query Cost**: `5,000,000` (Prevent expensive queries)

### Step 2: Establish Routing Rules
Rules determine which queue a query lands in.
-   **Rule 1 (High Priority)**: `IF User IS_MEMBER_OF('Execs') THEN Route To 'Interactive_Dashboards'`
-   **Rule 2 (Tool Based)**: `IF Client Tool LIKE '%Tableau%' THEN Route To 'Interactive_Dashboards'`
-   **Rule 3 (Catch-All)**: `Route To 'Default Queue'`

### Step 3: Job Limits (The Safety Net)
-   **Max Query Field Size**: 8000 (Prevents massive text blobs found in some CSVs).
-   **Max Planning Time**: 60s (Prevents planner from hanging on impossible SQL).
