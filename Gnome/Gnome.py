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
    global s_url, s_msg
    try:
        response = requests.post(url, headers=headers)
        
        if response.status_code == 200:
            print(f'Response: {response.json()}')
            s_url = response.json()["url"]  
            s_msg = response.json()['msg']  
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


def getGptVisionAnswer(model):  
    openai.api_key = os.getenv("OPENAI_API_KEY") 
    completion1 = openai.ChatCompletion.create(
    model= model,
    messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": f"{s_msg}"},
        {
          "type": "image_url",
          "image_url": {
            "url": f"{s_url}",
          },
        },
      ],
    }
  ],  
    )
   
    return completion1.choices[0].message['content']

getToken('https://zadania.aidevs.pl/token/gnome')
get_Task('https://zadania.aidevs.pl/task/'+ token)
s_answer = getGptVisionAnswer('gpt-4-vision-preview')
print(s_answer)
post_answ('https://zadania.aidevs.pl/answer/'+ token, s_answer)
