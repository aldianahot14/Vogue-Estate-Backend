# generate_images.py
import json

def load_json_data(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

def generate_insert_for_images(images_data):
    insert_commands = []
    for image in images_data:
        # Assuming each image is tied to a listing by listing's address or another unique field
        property_id_subquery = f"(SELECT id FROM main_app_listing WHERE address = '{image['listing_address']}')"
        command = f"INSERT INTO main_app_listingimage (property_id, image) VALUES ({property_id_subquery}, '{image['image_url']}');"
        insert_commands.append(command)
    return insert_commands

def write_sql_file(commands, filename):
    with open(filename, 'w') as file:
        for command in commands:
            file.write(command + '\n')

if __name__ == "__main__":
    images_data = load_json_data('dummy_images.json')
    images_commands = generate_insert_for_images(images_data)
    write_sql_file(images_commands, 'seed_images.sql')
