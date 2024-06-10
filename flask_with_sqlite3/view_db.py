import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('database.db')

# Read the table into a DataFrame
df = pd.read_sql_query("SELECT * FROM tasks", conn)

# Close the connection
conn.close()

# Display the DataFrame
print(df)