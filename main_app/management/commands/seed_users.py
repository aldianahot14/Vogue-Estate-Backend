import json

def load_json_data(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

def generate_insert_for_users(users_data):
    insert_commands = []
    for user in users_data:
        command = f"INSERT INTO auth_user (first_name, last_name, username, email, password, is_staff, is_active, is_superuser, date_joined) VALUES ('{user['first_name']}', '{user['last_name']}', '{user['username']}', '{user['email']}', '{user['password']}', {user['is_staff']}, {user['is_active']}, {user['is_superuser']}, '{user['date_joined']}');"
        insert_commands.append(command)
    return insert_commands

def write_sql_file(commands, filename):
    with open(filename, 'w') as file:
        for command in commands:
            file.write(command + '\n')

if __name__ == "__main__":
    users_data = load_json_data('dummy_users.json')
    users_commands = generate_insert_for_users(users_data)
    write_sql_file(users_commands, 'seed_user_data.sql')
