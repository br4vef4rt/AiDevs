import psycopg2
import os
import openai
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct

def getEmbedding(input):
    openai.api_key = os.getenv("OPENAI_API_KEY") 
    response = openai.Embedding.create(
        input= input,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

def insEmbToQdrant(id,vector,url):
    embedding_vector = vector
    payload = {"url": url}  

    client = QdrantClient(host="localhost", port=6333)  
    point = PointStruct(id=id,  
                        vector=embedding_vector,
                        payload=payload)

    client.upsert(
        collection_name="unknown_collection",
        wait=True,
        points=[point]
    )
    print(f"Data - {url} - inserted successfully.")


try:
    conn = psycopg2.connect(
        dbname='DZDB',
        user='USER1',
        password='Trewq!23',
        host='localhost',
        port='5432'
    )
except psycopg2.Error as e:
    print("Error: Could not make the connection to the postgres database")
    print(e)


try:
    cur = conn.cursor()
    query = """
    SELECT id, info, url FROM datafromunknow WHERE id = %s;
    """
    cur.execute(query, ('25294200-2d30-4108-8812-893dee50c1ba',))
    row = cur.fetchone()   
    #print(f"{row[0]} ' - ' {getEmbedding(row[3])}")
    insEmbToQdrant(row[0],getEmbedding(row[1]),row[2])
    cur.close()
except psycopg2.Error as e:
    print("Error: Could not execute the query")
    print(e)


# try:
#     cur = conn.cursor()
#     query = "SELECT id, info FROM datafromunknow;"
#     cur.execute(query)
#     rows = cur.fetchall()
#     for row in rows:
#         print(row)
#     cur.close()
# except psycopg2.Error as e:
#     print("Error: Could not execute the query")
#     print(e)



