# Coalesce
df.select(F.coalesce(F.col("phone"), F.col("email"), F.lit("Unknown")))

