# Testing & Verification Guide

This guide explains how to verify the installation and functionality of the Dremio Agent Skill.

## 1. Environment Setup

Ensure your `.env` file is configured correctly.
Run the self-correction tool:

```bash
python dremio-skill/scripts/validate_conn.py
```

**Expected Output:**
- ✅ Environment Variables Present
- ✅ Connection Successful!
- ✅ 'Samples' source found (Optional but recommended)

## 2. Running Examples

### Python Examples
Run the `data_quality_check.py` to verify query execution and Pandas integration.

```bash
python dremio-skill/examples/python/data_quality_check.py
```

**Expected Output:**
- "Running measures on Samples..."
- "All Checks Passed" (or a list of issues if the data has changed)

### SQL Validation
To test SQL capabilities, you can copy the content of `dremio-skill/examples/sql/iceberg_maintenance.sql` and ask the Agent to explain or execute it (if using a Client with SQL execution capabilities).

## 3. Knowledge Base Verification

The Agent should be able to index the knowledge tree.
Check the tree map:

```bash
cat dremio-skill/knowledge/knowledge-tree.md
```

Ensure the file lists documentation for Python, SQL, and CLI.

## 4. Troubleshooting

- **401 Unauthorized**: Check your `DREMIO_PAT`.
- **404 Endpoint Not Found**: Ensure `DREMIO_ENDPOINT` does not have a trailing slash and points to the correct API base (e.g. `https://api.dremio.cloud`).
- **Missing Module**: Ensure you installed dependencies: `pip install dremio-simple-query pandas dremioframe`.
