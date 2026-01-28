# Wizard: Access Control & Security Model

This wizard guides the Agent in designing and implementing a robust Role-Based Access Control (RBAC) and row/column security model in Dremio.

## 1. Discovery Phase (Ask the User - REQUIRED)
**Do not recommend specific grants** until you understand the organizational hierarchy.

1.  **Persona Groups**: "What are the major user groups? (e.g., DataEngineers, BusinessAnalysts, HR, Executives)"
2.  **Auth Provider**: "Are you syncing users/groups from LDAP, Azure AD, or Okta?"
3.  **Granularity**: "Do you need Row-Level Security (e.g., Sales Reps only see their region)?"
4.  **Sensitive Data**: "Are there PII columns (SSN, Email) that need masking?"
5.  **Environment**: "Is this a Read-Only reporting environment or a Sandbox for analysts?"

## 2. Strategic Patterns

### A. The "Least Privilege" Layering
Recommend this structure:
1.  **Bronze/Raw Space**: Accessed ONLY by `DataEngineers`.
2.  **Silver/Business Space**: Read-Only for `Analysts`, Read-Write for `Data Stewards`.
3.  **Gold/App Space**: Read-Only for BI Tools/`Executives`.

### B. Row Level Security (RLS)
If the user answered "Yes" to Granularity (Q3), use a `Row Access Policy`.
*Requirement*: A lookup table mapping `user_name` to `allowed_region`.

### C. Column Masking
If the user answered "Yes" to Sensitive Data (Q4), use a `Column Masking Policy`.

## 3. Implementation Steps

### Step A: Granting Space Privileges
```sql
-- Engineering needs full control on Raw
GRANT ALL ON SPACE "Raw" TO ROLE "DataEngineers";

-- Analysts can only QUERY Business layer
GRANT SELECT ON SPACE "Business" TO ROLE "Analysts";
```

### Step B: Implementing Row Access Policy
1.  Create the rules function.
    ```sql
    CREATE FUNCTION "Business".security.check_region(region_val VARCHAR)
    RETURNS BOOLEAN
    RETURN SELECT 1 FROM "Business".security.user_region_map m
           WHERE m.user = query_user() AND m.region = region_val;
    ```
2.  Apply to the table.
    ```sql
    ALTER TABLE "Business".sales_data
    ADD ROW ACCESS POLICY "Business".security.check_region(region);
    ```

### Step C: Implementing Column Masking
1.  Create the masking UDF.
    ```sql
    CREATE FUNCTION "Business".security.mask_ssn(ssn VARCHAR)
    RETURNS VARCHAR
    RETURN CASE
        WHEN is_member('HR') THEN ssn
        ELSE 'XXX-XX-XXXX'
    END;
    ```
2.  Apply to the column.
    ```sql
    ALTER TABLE "Business".employees
    ADD MASKING POLICY "Business".security.mask_ssn(ssn);
    ```
