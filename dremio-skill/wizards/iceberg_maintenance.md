# Wizard: Iceberg Maintenance Strategy

This wizard guides the Agent in establishing a maintenance routine for Iceberg tables in Dremio to ensure long-term performance and storage efficiency.

## 1. Discovery Phase (Ask the User - REQUIRED)
Before generating scripts, understand the table's behavior. **Do not proceed** until you have these answers.

1.  **Churn Rate**: "How frequently is this table updated? (Streaming, Hourly, Daily?)"
2.  **File Counts**: "Do you suspect you have 'Small File' issues? (e.g., thousands of files < 10MB?)"
3.  **Retention Policy**: "How far back do you need to 'Time Travel'? (Days, Weeks?)"
4.  **Partitioning**: "How is the table partitioned? (Year, Month, Day, Bucket?)"

## 2. Maintenance Concepts

### A. Optimization (Compaction)
*Goal*: Merge small data files into larger, optimally sized files for read performance.
*Trigger*: High file count, slow scan times.

### B. Vacuum (Snapshot Expiration & Orphan Cleanup)
*Goal*: Delete old data files that are no longer referenced by active snapshots to free up storage.
*Trigger*: Bloated storage costs, long metadata history.

## 3. Execution Steps

### Step 1: Manual Assessment
Ask user to check current snapshot count:
```sql
SELECT count(*) as history_depth FROM TABLE(table_history('source.table_name'));
```

### Step 2: Running OPTIMIZE (Bin-Packing)
Generate a script to compact files. Rcommend running this **Daily** for high-churn tables.

```sql
-- Standard Compaction (Default target size ~256MB/512MB)
OPTIMIZE TABLE "source"."table_name";

-- For massive tables, limit scope
OPTIMIZE TABLE "source"."table_name"
  REWRITE DATA (MIN_INPUT_FILES=5);
```

### Step 3: Running VACUUM (Cleanup)
Generate a script to expire snapshots suitable for the user's retention needs (e.g., keep last 7 days).

```sql
-- Expire snapshots older than 7 days
VACUUM TABLE "source"."table_name"
  EXPIRE SNAPSHOTS OLDER_THAN '2023-10-27 00:00:00.000'; -- Calculate this timestamp dynamically
```

**Agent Tip**: When generating this for the user, calculate the specific timestamp for them based on their answer to Question 3 (Retention Policy).

### Step 4: Automating (Optional)
If the user asks "How do I automate this?", recommend:
1.  **Dremio Cron Syntax** (if available in their version).
2.  **External Orchestrator** (Airflow, Python script using `dremioframe`).
