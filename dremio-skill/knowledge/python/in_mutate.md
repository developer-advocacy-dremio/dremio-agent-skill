# In mutate
df.mutate(
    upper_city="UPPER(city)",
    total_salary="SUM(salary) OVER (PARTITION BY dept)"
)

