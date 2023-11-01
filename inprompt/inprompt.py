import requests
import json
import os
import openai

url1 = 'https://zadania.aidevs.pl/token/inprompt'  # Replace with your URL
token = 'none'
taskInput = 'none'
taskQuestion = 'none'

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
url2 = 'https://zadania.aidevs.pl/task/'+ token

def get_Task(url):
    headers = {'Content-Type': 'application/json'}
    global taskInput
    global taskQuestion

    try:
        response = requests.post(url, headers=headers)
        
        if response.status_code == 200:
            #print(f'Response: {response.json()}')
            taskInput = response.json()["input"]
            taskQuestion = response.json()["question"]
        else:
            print(f'Failed to post data. Status code: {response.status_code}')
            print(f'Response: {response.text}')
            
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')

get_Task(url2)

def get_first_words(taskInput):
    return [sentence.split(' ')[0] for sentence in taskInput]

names = get_first_words(taskInput)
dicNameInfo = dict(zip(names, taskInput))
#print(tblNameInfo)
#print(dicNameInfo['Klemens'])


openai.api_key = os.getenv("OPENAI_API_KEY") 

completion1 = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "Your task is to return the name of the person in given input, nothing else. Do not return dots, commas or other whitespaces"},
    {"role": "user", "content": taskQuestion}
  ]
)
chosenName = completion1.choices[0].message['content']

print(taskQuestion)
print(chosenName)
print(dicNameInfo[chosenName])

completion2 = openai.ChatCompletion.create(
  model="gpt-4",
  messages=[
    {"role": "system", "content": f'Answer the question based on the given context. Context|||{dicNameInfo[chosenName]}|||'},
    {"role": "user", "content": taskQuestion}
  ]
)
answer = completion2.choices[0].message['content']
json_answ = json.dumps({"answer": completion2.choices[0].message['content'] })
print (answer)
print(json_answ)

url3 = 'https://zadania.aidevs.pl/answer/'+ token
def post_answ(url):
    payload = {"answer": answer}
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