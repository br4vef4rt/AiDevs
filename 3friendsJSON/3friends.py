import requests
import json
import os
import openai

s_url = None
s_msg = None
s_answer = None


def getToken(url):
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
    try:
        response = requests.post(url, headers=headers)
        
        if response.status_code == 200:
            print(f'Response: {response.json()}')
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

def getGptAnswer(t_message, model):  
    openai.api_key = os.getenv("OPENAI_API_KEY") 
    completion1 = openai.ChatCompletion.create(
    model= model,
    messages = t_message   
    )
   
    return completion1.choices[0].message['content']


url = 'https://zadania.aidevs.pl/data/3friends.json'
response = requests.get(url)
data = response.json()

def convertLine(name, given_data):
    t_message1 = [
        {"role": "system", "content": f"Rewrite given_data as short as you can in a very short note form. Skip the name = {name}. Do not use polish chars (ą,ę,ś,ć,ó,ż,ź). Make words ultra-short: something -> sth, computer -> comp, ."},
        {"role": "user", "content": f"given_data = {given_data}"}
        ]
    return  getGptAnswer(t_message1,"gpt-4-1106-preview")

#s_GptAnswer = convertLine("zygfryd", data[name][0])
#print(s_GptAnswer)

import json

# Replace 'path/to/your/file.json' with the actual file path
file_path = 'D:/Dev/repos/AiDevs/3friendsJSON/data_v3.json'

# Open the file and read its contents into a string
with open(file_path, 'r') as file:
    json_string = file.read()


getToken('https://zadania.aidevs.pl/token/optimaldb')
get_Task('https://zadania.aidevs.pl/task/'+ token)
s_answer = json_string
post_answ('https://zadania.aidevs.pl/answer/'+ token, s_answer)