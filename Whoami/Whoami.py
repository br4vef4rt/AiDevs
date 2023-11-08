import requests
import json
import re
import openai
import os

token = None
s_answer = None
s_task = None
s_hint = None
s_gptAnswer = None

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
    global s_task, s_hint
    try:
        response = requests.post(url, headers=headers)
        
        if response.status_code == 200:
            print(f'Response: {response.json()}')
            s_task =   response.json()["msg"]  
            s_hint =   response.json()["hint"]       
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

def getGptAnswer(t_message):
    openai.api_key = os.getenv("OPENAI_API_KEY") 
    completion1 = openai.ChatCompletion.create(
    model="gpt-4",
    messages = t_message
    )
    return completion1.choices[0].message['content']

post_json_to_url('https://zadania.aidevs.pl/token/whoami')
get_Task('https://zadania.aidevs.pl/task/'+ token)
t_message = [
        {"role": "system", "content": "I will give you hints about who is the person. If you know the answer and you are sure, give me the name and nothing else. If you need more hints answer 'NO' and nothing else"},
        {"role": "user", "content": f"hint: {s_hint}"}
    ]  
s_gptAnswer =  getGptAnswer(t_message)
print(s_gptAnswer)

while s_gptAnswer == 'NO':
    post_json_to_url('https://zadania.aidevs.pl/token/whoami')
    get_Task('https://zadania.aidevs.pl/task/'+ token)
    t_message.append({"role": "system", "content":  s_gptAnswer})
    t_message.append({"role": "user", "content":  f"hint: {s_hint}"})
    s_gptAnswer =  getGptAnswer(t_message)
    print(s_gptAnswer)

post_answ('https://zadania.aidevs.pl/answer/'+ token, s_gptAnswer)