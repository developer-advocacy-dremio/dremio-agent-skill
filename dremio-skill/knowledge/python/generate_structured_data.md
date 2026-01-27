# Generate Structured Data
df.select(
    F.ai_generate(
        "Extract entities", 
        schema="ROW(person VARCHAR, location VARCHAR)"
    ).alias("entities")
)
```

### Raw SQL Usage

You can also use AI functions by writing the SQL string directly in `mutate` or `select`.

```python
df.mutate(
    spice_level="AI_CLASSIFY('Identify the Spice Level:' || ARRAY_TO_STRING(ingredients, ','), ARRAY [ 'mild', 'medium', 'spicy' ])"
)
```

## Available Functions

| Function | Description |
| :--- | :--- |
| `ai_classify(prompt, categories, model_name=None)` | Classifies text into one of the provided categories. |
| `ai_complete(prompt, model_name=None)` | Generates a text completion for the prompt. |
| `ai_generate(prompt, model_name=None, schema=None)` | Generates structured data based on the prompt. Use `schema` to define the output structure (e.g., `ROW(...)`). |

### Examples

#### AI_CLASSIFY

```python
F.ai_classify("Is this email spam?", ["Spam", "Not Spam"])
F.ai_classify("Categorize product", ["Electronics", "Clothing"], model_name="gpt-4")
```

#### AI_COMPLETE

```python
F.ai_complete("Write a SQL query to find top users")
F.ai_complete("Translate to French", model_name="gpt-3.5")
```

#### AI_GENERATE

```python
