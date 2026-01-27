# Check history
print(client.query_history)  # ['SELECT * FROM table1', 'SELECT * FROM table2']
print(client.get_last_query())  # 'SELECT * FROM table2'

