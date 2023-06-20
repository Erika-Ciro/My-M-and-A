import sqlite3
import pandas as pd
from io import StringIO

def sql_to_csv(database, table_name):
    # Connect to the database and execute the SELECT query
    conn = sqlite3.connect(database)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    
    # Get the column names and data
    column_names = df.columns.tolist()
    rows = df.values.tolist()
    
    # Construct the CSV string
    csv_string = ','.join(column_names) + '\n'
    csv_string += '\n'.join(','.join(str(r) for r in row) for row in rows)

    df.to_csv(f"{table_name}.csv", index=False)

    conn.close()
    return csv_string

# Convert SQL to CSV
print(sql_to_csv('all_fault_line.db', 'fault_lines'))

# Read and print the contents of the CSV file
with open('fault_lines.csv', newline='') as csv_file:
     print(csv_file.read())

def csv_to_sql(csv_content, database, table_name):
    df = pd.read_csv(csv_content)
    conn = sqlite3.connect(database)
    quoted_cols = ['"{}"'.format(col.replace('_', ' ')) for col in df.columns]
    col_string = ','.join(quoted_cols)

    # Create a table with the same columns as the DataFrame
    query = 'CREATE TABLE IF NOT EXISTS {} ({});'.format(table_name, col_string)
    conn.execute(query)
    
    # Insert each row into the table
    for row in df.itertuples(index=False):
        query = f"INSERT INTO {table_name} VALUES ({','.join('?'*len(row))})"
        conn.execute(query, row)
    
    conn.commit()
    conn.close()

with open('list_volcano.csv', 'r') as csv_file:
    csv_content = StringIO(csv_file.read())
csv_to_sql(csv_content, 'list_volcanos.db', 'volcanos')
