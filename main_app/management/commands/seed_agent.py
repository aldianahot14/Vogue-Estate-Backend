# generate_agents.py
import json

def load_json_data(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

def generate_insert_for_agents(agents_data, user_ids):
    insert_commands = []
    for agent, user_id in zip(agents_data, user_ids):
        command = f"INSERT INTO main_app_agent (name, email, license, user_id) VALUES ('{agent['name']}', '{agent['email']}', '{agent['license']}', {user_id});"
        insert_commands.append(command)
    return insert_commands

def write_sql_file(commands, filename):
    with open(filename, 'w') as file:
        for command in commands:
            file.write(command + '\n')

if __name__ == "__main__":
    agents_data = load_json_data('dummy_agents.json')
    # Assuming user IDs are from 1 to 7
    user_ids = range(1, 8)
    agents_commands = generate_insert_for_agents(agents_data, user_ids)
    write_sql_file(agents_commands, 'seed_agents.sql')
