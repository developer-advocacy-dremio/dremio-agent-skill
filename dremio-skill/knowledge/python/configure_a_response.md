# Configure a response
users_df = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie']
})

client.add_response("SELECT * FROM users", users_df)

