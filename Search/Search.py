import requests
import json
import os
import openai
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct


token = None
s_answer = None
s_question = None


def post_json_to_url(url):
    payload = {'apikey': '261aab06-4a16-4bf7-ad7f-f7fceb3a150b'}
    headers = {'Content-Type': 'application/json'}
    global token

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print(f'Successfully posted data: {json.dumps(payload)}')
            print(f'Response: {response.json()}')
            token = response.json()["token"]
        else:
            print(f'Successfully posted data: {json.dumps(payload)}')
            print(f'Failed to post data. Status code: {response.status_code}')
            print(f'Response: {response.text}')
            

    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')


def get_Task(url):
    headers = {'Content-Type': 'application/json'}
    global s_question
    try:
        response = requests.post(url, headers=headers)
        
        if response.status_code == 200:
            print(f'Response: {response.json()}')
            s_question = response.json()["question"]      
        else:
            print(f'Failed to post data. Status code: {response.status_code}')
            print(f'Response: {response.text}')
            
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')


def post_answ(url, s_answer):
    payload = {"answer": s_answer}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print(f'Successfully posted data: {json.dumps(payload)}')
            print(f'Response: {response.json()}')
        else:
            print(f'Successfully posted data: {json.dumps(payload)}')
            print(f'Failed to post data. Status code: {response.status_code}')
            print(f'Response: {response.text}')
            
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')

def getEmbedding(input):
    openai.api_key = os.getenv("OPENAI_API_KEY") 
    response = openai.Embedding.create(
        input= input,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

post_json_to_url('https://zadania.aidevs.pl/token/search')
get_Task('https://zadania.aidevs.pl/task/'+ token)

client = QdrantClient("localhost", port=6333)



search_result = client.search(
    collection_name="unknown_collection", query_vector=getEmbedding(s_question), limit=1
)
url = search_result[0].payload['url']
print(url)

post_answ('https://zadania.aidevs.pl/answer/'+ token, url)