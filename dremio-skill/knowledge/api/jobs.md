# Jobs API

## Submit a Job (SQL)
```http
POST /v0/projects/{project_id}/sql
```
Body: `{"sql": "SELECT * FROM ...", "context": ["space", "folder"]}`

## Get Job Status
```http
GET /v0/projects/{project_id}/job/{job_id}
```

## Get Job Results
```http
GET /v0/projects/{project_id}/job/{job_id}/results
```
Parameters: `offset`, `limit`
