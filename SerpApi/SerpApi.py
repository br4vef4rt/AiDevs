import requests
import json
import os
import openai
from serpapi import GoogleSearch

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


def convertLine(name, given_data):
    t_message1 = [
        {"role": "system", "content": f"Rewrite given_data as short as you can in a very short note form. Skip the name = {name}. Do not use polish chars (ą,ę,ś,ć,ó,ż,ź). Make words ultra-short: something -> sth, computer -> comp, ."},
        {"role": "user", "content": f"given_data = {given_data}"}
        ]
    return  getGptAnswer(t_message1,"gpt-4-1106-preview")

def search_google(query):
    params = {
        "engine": "google",
        "q": query,
        "api_key": "Your_SerpApi_API_Key"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    return results


getToken('https://zadania.aidevs.pl/token/optimaldb')
get_Task('https://zadania.aidevs.pl/task/'+ token)
# s_answer = ''
# post_answ('https://zadania.aidevs.pl/answer/'+ token, s_answer)