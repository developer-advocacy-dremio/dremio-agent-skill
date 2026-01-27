# Convert from JSON
df.select(F.convert_from("json_col", "JSON"))

