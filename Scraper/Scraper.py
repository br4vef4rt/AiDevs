import requests
import json
import re
import openai
import os

token = None
s_answer = None
s_task = None
s_inputUrl = None
s_question = None
s_inputTxt = None
status = None

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
    global s_task, s_inputUrl, s_question
    try:
        response = requests.post(url, headers=headers)
        
        if response.status_code == 200:
            print(f'Response: {response.json()}')
            s_task =   response.json()["msg"] 
            s_inputUrl =   response.json()["input"]   
            s_question =   response.json()["question"]          
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


def getTxt(url):
    global s_inputTxt, status
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        status = response.status_code
        if response.status_code == 200:
            s_inputTxt = response.text
            print("Content read successfully")
        else:
            print(f"Failed to retrieve content, status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def getGptAnswer(s_task,s_question,s_inputTxt):
    openai.api_key = os.getenv("OPENAI_API_KEY") 

    completion1 = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": s_task},
        {"role": "user", "content": f"question = {s_question}; input = {s_inputTxt}"}
    ]    
    )
    return completion1.choices[0].message['content']

#s_answer = f"Use placeholders %imie%, %nazwisko%, %zawod% and %miasto% to say something about you."

post_json_to_url('https://zadania.aidevs.pl/token/scraper')
get_Task('https://zadania.aidevs.pl/task/'+ token)

getTxt(s_inputUrl)
if status == 500:
    getTxt(s_inputUrl)

if status == 200:
    s_answer = getGptAnswer(s_task,s_question,s_inputTxt)
    post_answ('https://zadania.aidevs.pl/answer/'+ token, s_answer)


#post_answ('https://zadania.aidevs.pl/answer/'+ token, s_answer)