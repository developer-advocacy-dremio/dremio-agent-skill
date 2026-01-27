# Run a native Postgres query
df = client.external_query("Postgres", "SELECT * FROM users WHERE active = true")

