# Complete
df.select(
    F.ai_complete("Summarize this text: " + F.col("text")).alias("summary")
)

