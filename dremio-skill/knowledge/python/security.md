# Security


---

## Security Best Practices

Ensuring the security of your data and credentials is paramount. Here are best practices for using DremioFrame securely.

## Credential Management

### Never Hardcode Credentials

**BAD:**
```python
client = DremioClient(pat="my-secret-token")
```

**GOOD:**
Use environment variables. DremioFrame automatically looks for `DREMIO_PAT`, `DREMIO_PROJECT_ID`, etc.

```bash
export DREMIO_PAT="my-secret-token"
```

```python
client = DremioClient() # Reads from env
```

### Using .env Files

For local development, use a `.env` file but **add it to `.gitignore`**.

**.env**
```bash
DREMIO_PAT=...
```

**.gitignore**
```
.env
```

## Network Security

### TLS/SSL

Always use TLS (HTTPS) when connecting to Dremio, especially over public networks.

- **Dremio Cloud**: TLS is enforced (HTTPS/443).
- **Dremio Software**: Enable TLS on the coordinator and set `tls=True` in the client.

```python
client = DremioClient(..., tls=True)
```

### Certificate Verification

Do not disable certificate verification (`disable_certificate_verification=True`) in production. This leaves you vulnerable to Man-in-the-Middle (MITM) attacks.

## Least Privilege

### Personal Access Tokens (PATs)

Create PATs with the minimum necessary expiration time. Rotate them regularly.

### Service Accounts

For production pipelines, use a dedicated Service Account (if available in your Dremio edition) or a dedicated user account with restricted permissions, rather than your personal admin account.

### Role-Based Access Control (RBAC)

Ensure the user/role used by DremioFrame only has access to the datasets and spaces it needs.
- **Read-Only**: If the pipeline only reads data, grant `SELECT` only.
- **Write**: Grant `CREATE TABLE`, `INSERT`, `UPDATE` only on specific target folders/spaces.

## Injection Prevention

### Parameterized Queries

While DremioFrame's builder API generates safe SQL, be careful when using raw SQL with `client.query()`. Avoid f-strings with untrusted user input.

**BAD:**
```python
user_input = "'; DROP TABLE users; --"
client.query(f"SELECT * FROM table WHERE id = '{user_input}'")
```

**GOOD:**
Validate and sanitize inputs before constructing SQL strings, or use the Builder API which handles quoting.

```python
# Builder API handles quoting
client.table("table").filter(f"id = '{sanitized_input}'") 
```
*Note: Dremio Flight currently supports parameter binding in limited contexts; DremioFrame relies on string construction, so input validation is key.*


---

<!-- Source: docs/admin_governance/security_patterns.md -->

---

## Security Patterns

This guide covers advanced security patterns using Dremio's governance features.

## 1. Row-Level Security (RLS) with Lookup Tables

Instead of hardcoding users in RLS policies, use a lookup table to manage permissions dynamically.

### Step 1: Create Lookup Table
Create a table `admin.permissions` mapping users to regions.

| user_email | region |
| :--- | :--- |
| alice@co.com | NY |
| bob@co.com | CA |

### Step 2: Create Policy Function
The function checks if the current user matches the region in the lookup table.

```sql
CREATE FUNCTION check_region_access(r VARCHAR) 
RETURNS BOOLEAN 
RETURN SELECT count(*) > 0 FROM admin.permissions WHERE user_email = query_user() AND region = r;
```

### Step 3: Apply Policy

```python
client.admin.apply_row_access_policy("sales", "check_region_access(region)")
```

## 2. Hierarchy-Based Access

Allow managers to see data for their entire hierarchy.

*   Store the hierarchy in a flattened table or use recursive CTEs (if supported) in the policy function.
*   Common pattern: `path` column (e.g., `/US/NY/Sales`). Policy: `user_path LIKE row_path || '%'`.

## 3. Column Masking Patterns

### Dynamic Masking based on Role

```python
# Mask email for non-HR users
client.admin.create_policy_function(
    "mask_email", 
    "email VARCHAR", 
    "VARCHAR", 
    "CASE WHEN is_member('HR') THEN email ELSE '***@***.com' END"
)

client.admin.apply_masking_policy("employees", "email", "mask_email(email)")
```

### Format Preserving Masking

If downstream tools expect a valid email format, mask the characters but keep the structure.

```sql
-- Simple example
CASE WHEN is_member('HR') THEN email ELSE 'user_' || hash(email) || '@masked.com' END
```


---

<!-- Source: docs/admin_governance/spaces_folders.md -->