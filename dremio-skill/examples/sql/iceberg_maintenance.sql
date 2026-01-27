-- Iceberg Table Maintenance Script
-- Reference: knowledge/sql/sql_commands.md

-- 1. Optimize (Compaction)
-- Merges small files into larger ones for better read performance.
-- 'MIN_INPUT_FILES' prevents churning if there are only a few files.
OPTIMIZE TABLE "Spaces"."Analytics"."Silver"."Taxi_Summary"
REWRITE DATA (MIN_INPUT_FILES=5);

-- 2. Remove Orphan Files
-- Cleans up files not referenced by any snapshot (e.g. from failed writes).
VACUUM TABLE "Spaces"."Analytics"."Silver"."Taxi_Summary"
EXPIRE SNAPSHOTS OLDER_THAN '2025-01-01';

-- 3. Rollback (if needed)
-- Identify snapshots
SELECT * FROM TABLE(table_history('"Spaces"."Analytics"."Silver"."Taxi_Summary"'));

-- Rollback to a specific snapshot ID
-- ALTER TABLE "Spaces"."Analytics"."Silver"."Taxi_Summary"
-- ROLLBACK TO SNAPSHOT '123456789';
