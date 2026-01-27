# Check that 'customer_id' is never NULL
df.quality.expect_not_null("customer_id")

