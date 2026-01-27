# Check that there are exactly 0 rows where amount is negative
df.quality.expect_row_count("amount < 0", 0, "eq")

