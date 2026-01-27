# Classify
df.select(
    F.ai_classify(F.col("review"), ["Positive", "Negative"]).alias("sentiment")
)

