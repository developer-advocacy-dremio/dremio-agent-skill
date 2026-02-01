# Catalog API

## Catalog Attributes
*   `data`: Array of container objects.
*   `stats`: Object containing `datasetCount`.

## Endpoints

### Retrieve a Catalog
```http
GET /v0/projects/{project_id}/catalog
```

### Create a Source
```http
POST /v0/projects/{project_id}/catalog
```
Body: `{"entityType": "source", ...}`

### Retrieve Entity by ID
```http
GET /v0/projects/{project_id}/catalog/{id}
```

### Retrieve Entity by Path
```http
GET /v0/projects/{project_id}/catalog/by-path/{path}
```

### Update Entity
```http
PUT /v0/projects/{project_id}/catalog/{id}
```

### Delete Entity
```http
DELETE /v0/projects/{project_id}/catalog/{id}
```
