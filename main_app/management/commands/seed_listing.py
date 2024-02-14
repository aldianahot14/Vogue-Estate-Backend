# generate_listings.py
import json

def load_json_data(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

def generate_insert_for_listings(listings_data):
    insert_commands = []
    for listing in listings_data:
        command = f"INSERT INTO main_app_listing (address, city, state, zipcode, description, price, bedrooms, bathrooms, sqft, agent_id) VALUES ('{listing['address']}', '{listing['city']}', '{listing['state']}', '{listing['zipcode']}', '{listing['description']}', {listing['price']}, {listing['bedrooms']}, {listing['bathrooms']}, {listing['sqft']}, {listing['agent_id']});"
        insert_commands.append(command)
    return insert_commands

def write_sql_file(commands, filename):
    with open(filename, 'w') as file:
        for command in commands:
            file.write(command + '\n')

if __name__ == "__main__":
    listings_data = load_json_data('dummy_listings.json')
    listings_commands = generate_insert_for_listings(listings_data)
    write_sql_file(listings_commands, 'seed_listings.sql')
