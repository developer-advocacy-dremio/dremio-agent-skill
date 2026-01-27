# Update a view (fetches latest version tag automatically)
```python
catalog.update_view(
    id="view-id-uuid",
    path=["Space", "MyView"],
    sql="SELECT * FROM source.table WHERE id > 100"
)
```

## Collaboration (Wikis & Tags)

Manage documentation and tags for any catalog entity (dataset, source, space, folder).

### Wikis

```python
# Get Wiki
wiki = catalog.get_wiki("entity-id")
print(wiki.get("text"))

# Update Wiki (fetch version first to avoid conflict)
try:
    current_wiki = catalog.get_wiki("entity-id")
    version = current_wiki.get("version")
except:
    version = None

catalog.update_wiki(
    id="entity-id",
    content="# My Dataset\n\nThis is a documented dataset.",
    version=version
)
```

### Tags

```python
# Get Tags
tags = catalog.get_tags("entity-id")
print(tags)

# Set Tags (Overwrites existing tags)
catalog.set_tags("entity-id", ["production", "marketing"])
```


---

<!-- Source: docs/admin_governance/lineage.md -->

