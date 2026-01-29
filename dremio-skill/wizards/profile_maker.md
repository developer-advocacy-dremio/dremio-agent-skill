# Wizard: Profile Maker (Connection Setup)

This wizard guides the Agent in helping the user securely set up a connection profile for the Dremio CLI/SDK.

## 1. Discovery Phase (Ask the User - REQUIRED)
**Do not ask for secrets in the chat.**

1.  **Environment**: "Is this for Dremio Cloud or Dremio Software (Self-Managed)?"
2.  **Existing Config**: "Do you already have a `.env` file in this project?"
3.  **Authentication**: "Do you have your PAT (Personal Access Token) ready?"

## 2. Security First Strategy
**NEVER** ask the user to paste their password or PAT into the chat.
**ALWAYS** instruct the user to define these as environment variables in a `.env` file.

### Step 1: Define Environment Variables
Ask the user to add the following to their `.env` file (if not already present):

**For Dremio Cloud:**
```bash
DREMIO_ENDPOINT=https://api.dremio.cloud
DREMIO_PROJECT_ID=your-project-id
DREMIO_PAT=your-secret-pat
```

**For Dremio Software:**
```bash
DREMIO_SOFTWARE_HOST=dremio.company.com
DREMIO_SOFTWARE_PAT=your-secret-pat
# OR for legacy auth
# DREMIO_SOFTWARE_USER=admin
# DREMIO_SOFTWARE_PASSWORD=secret
```

## 3. Execution Steps

### Step 2: Create the Profile (Command Construction)
Construct the CLI command using the environment variables.

**Cloud Command:**
```bash
dremio profile create --name cloud --base-url $DREMIO_ENDPOINT --token $DREMIO_PAT --project-id $DREMIO_PROJECT_ID
```

**Software Command:**
```bash
dremio profile create --name software --base-url $DREMIO_SOFTWARE_HOST --token $DREMIO_SOFTWARE_PAT
```

### Step 3: Validation
Verify the connection immediately.

```bash
# Test the specific profile
dremio query --profile cloud --sql "SELECT 1"
```

If this fails, run the diagnostic tool:
`python dremio-skill/scripts/validate_conn.py`
