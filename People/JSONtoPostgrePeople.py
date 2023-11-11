import json
import psycopg2
import uuid
import requests
from psycopg2.extras import execute_batch
import requests
import json

url = "https://zadania.aidevs.pl/data/people.json"
jsonPath = "D:/Dev/repos/AiDevs/People/data.json"

response = requests.get(url)

if response.status_code == 200:
    data = json.loads(response.text)
    with open(jsonPath, 'w') as f:
        json.dump(data, f)
    print("JSON downloaded and saved")
else:
    print(f"Failed to download data from {url}. Status code: {response.status_code}")

# Load JSON data from a file
with open(jsonPath, 'r') as file:
    data = json.load(file)
print("JSON loaded from folder")



# Database connection parameters - modify these with your details
conn_params = {
    'dbname': 'DZDB',
    'user': 'USER1',
    'password': 'Trewq!23',
    'host': 'localhost',
    'port': '5432'
}

# Connect to your postgres DB
conn = psycopg2.connect(**conn_params, client_encoding='utf8')



# Prepare SQL query to insert data
insert_query = 'INSERT INTO people (imie, nazwisko, o_mnie, ulubiona_postac_z_kapitana_bomby, ulubiony_film, ulubiony_kolor, ulubiony_serial, wiek) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'

# Data to be inserted
values_to_insert = [( item['imie'], item['nazwisko'], item['o_mnie'], item['ulubiona_postac_z_kapitana_bomby'], item['ulubiony_film'], item['ulubiony_kolor'], item['ulubiony_serial'], item['wiek']) for item in data]

# Insert data into the database
with conn.cursor() as cursor:
    execute_batch(cursor, insert_query, values_to_insert)
    conn.commit()

conn.close()

