import requests
import json
import os
import openai

url1 = 'https://zadania.aidevs.pl/token/embedding'  # Replace with your URL
token = 'none'

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


post_json_to_url(url1)

import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY") 

response = openai.Embedding.create(
    input="Hawaiian pizza",
    model="text-embedding-ada-002"
)
embeddings = response['data'][0]['embedding']

#print(embeddings)

url3 = 'https://zadania.aidevs.pl/answer/'+ token
def post_answ(url):
    payload = {"answer": embeddings}
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


post_answ(url3)

