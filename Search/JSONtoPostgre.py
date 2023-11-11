import json
import psycopg2
import uuid
import requests
from psycopg2.extras import execute_batch
import requests
import json

url = "https://unknow.news/archiwum.json"
jsonPath = "D:/Dev/repos/AiDevs/Search/data.json"

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
insert_query = 'INSERT INTO datafromunknow (id, title, url, info, date) VALUES (%s, %s, %s, %s, %s)'

# Data to be inserted
values_to_insert = [(str(uuid.uuid4()), item['title'], item['url'], item['info'], item['date']) for item in data]

# Insert data into the database
with conn.cursor() as cursor:
    execute_batch(cursor, insert_query, values_to_insert)
    conn.commit()

conn.close()
