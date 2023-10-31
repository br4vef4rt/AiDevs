import requests
import json

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
print(names)



#print(taskQuestion)
#print(taskInput)