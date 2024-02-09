
import json

def json_to_sql(json_file_path, table_name):
    # Read the JSON data
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    
    # SQL insert statements
    sql_inserts = []
    
    for entry in data:
        listing = entry['Listing']
        columns = ', '.join(listing.keys())
        values = ', '.join([f"'{str(value).replace("'", "''")}'" if isinstance(value, str) 
                            else str(value) if not isinstance(value, list) 
                            else ', '.join(f"'{str(v).replace("'", "''")}'" for v in value)
                            for value in listing.values()])
        sql_insert = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
        sql_inserts.append(sql_insert)
    
    return sql_inserts

# Convert the JSON to SQL and print the result
table_name = 'listings'  # Replace with your actual table name
sql_insert_statements = json_to_sql('dummy_data.json', table_name)
for statement in sql_insert_statements:
    print(statement)
