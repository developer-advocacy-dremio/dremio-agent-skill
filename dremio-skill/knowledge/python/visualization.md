# Visualization


---

## Charting

DremioFrame integrates with Matplotlib and Pandas to allow quick visualization of your data.

## Prerequisites

Ensure `matplotlib` is installed:
```bash
pip install matplotlib
```
(It is installed by default with `dremioframe`)

## Creating Charts

The `chart()` method collects data to a Pandas DataFrame and uses `df.plot()` to generate a chart.

```python
# Create a bar chart
df.chart(kind="bar", x="category", y="count", title="Sales by Category")

# Save chart to file
df.chart(kind="line", x="date", y="sales", save_to="sales_trend.png")
```

### Supported Kinds
- `line`
- `bar`
- `barh`
- `hist`
- `box`
- `kde`
- `density`
- `area`
- `pie`
- `scatter`
- `hexbin`

### Customization
You can pass any argument supported by `pandas.DataFrame.plot()`:
```python
df.chart(kind="scatter", x="age", y="income", c="red", s=50)
```


---

<!-- Source: docs/analysis/plotting.md -->

---

## Interactive Plotting with Plotly

DremioFrame supports interactive charts using [Plotly](https://plotly.com/python/).

## Usage

Specify `backend="plotly"` in the `chart()` method.

```python
# Create an interactive scatter plot
fig = df.chart(
    kind="scatter",
    x="gdpPercap",
    y="lifeExp",
    color="continent",
    size="pop",
    hover_name="country",
    log_x=True,
    title="Life Expectancy vs GDP",
    backend="plotly"
)

# Display in notebook
fig.show()

# Save to HTML
df.chart(..., backend="plotly", save_to="chart.html")
```

## Supported Chart Types

- `line`
- `bar`
- `scatter`
- `pie`
- `histogram`
- `box`
- `violin`
- `area`

## Dependencies

Requires `plotly` and `pandas`.
For static image export (e.g., `.png`), `kaleido` is required.


---

<!-- Source: docs/analysis/profiling.md -->