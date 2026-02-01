# Dremio CLI Command Reference

## Catalog Operations
```bash
dremio catalog list              # List catalog items
dremio catalog get <id>          # Get item details
dremio catalog get-by-path <path> # Get by path
```

## SQL Operations
```bash
dremio sql execute <query>       # Execute SQL
dremio sql explain <query>       # Show execution plan
dremio sql validate <query>      # Validate syntax
```

## Use Case Guides (Partial)
- **Data Engineering**:
    1. Sources - Connect to data systems
    2. Tables - Configure physical datasets
    3. Views - Create virtual datasets

- **Data Governance**:
    1. Tags & Wiki - Document datasets
    2. Grants - Control access
    3. Users & Roles - Manage users
