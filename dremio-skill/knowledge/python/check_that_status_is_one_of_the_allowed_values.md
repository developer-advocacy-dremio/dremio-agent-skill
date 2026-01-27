# Check that 'status' is one of the allowed values
df.quality.expect_values_in("status", ["completed", "pending", "cancelled"])

