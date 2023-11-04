import requests
import json
import re
import openai

token = None
url_1 = 'https://zadania.aidevs.pl/token/functions'  # Replace with your URL

def post_json_to_url(url):
    payload = {'apikey': '261aab06-4a16-4bf7-ad7f-f7fceb3a150b'}
    headers = {'Content-Type': 'application/json'}
    global token
    global taskMsg   

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


post_json_to_url(url_1)
url_2 = 'https://zadania.aidevs.pl/task/'+ token

def get_Task(url):
    headers = {'Content-Type': 'application/json'}
    global mp3_url
    try:
        response = requests.post(url, headers=headers)
        
        if response.status_code == 200:
            print(f'Response: {response.json()}')           
        else:
            print(f'Failed to post data. Status code: {response.status_code}')
            print(f'Response: {response.text}')
            
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')

get_Task(url_2)

s_function = {
            "name": "addUser",
            "description": "select name, surname and year of born for the user, based on given prompt. I will use this function like this: addUser({'Adam','Nowak',1984})",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "user name"
                    },
                    "surname": {
                        "type": "string",
                        "description": "user surname"
                    },
                    "year": {
                        "type": "integer",
                        "description": "user year of birth"
                    }
                }
            }
        }




url3 = 'https://zadania.aidevs.pl/answer/'+ token
def post_answ(url):
    payload = {"answer": s_function}
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