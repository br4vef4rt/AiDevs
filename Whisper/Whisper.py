import requests
import json
import re
import openai

token = None
url_1 = 'https://zadania.aidevs.pl/token/whisper'  # Replace with your URL
mp3_url = None

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
    url_pattern = r'https?://\S+'
    try:
        response = requests.post(url, headers=headers)
        
        if response.status_code == 200:
            print(f'Response: {response.json()}')           
            urls = re.findall(url_pattern, response.json()['msg'])
            mp3_url = urls[0] if urls else None
        else:
            print(f'Failed to post data. Status code: {response.status_code}')
            print(f'Response: {response.text}')
            
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')

get_Task(url_2)

# The local path where you want to save the MP3 file
local_filename = r'D:\Dev\repos\AiDevs\Whisper\downloaded_file.mp3'

response = requests.get(mp3_url)

if response.status_code == 200:
    # Open the local file in write-binary mode
    with open(local_filename, 'wb') as file:
        file.write(response.content)
    print(f"Downloaded '{local_filename}' from '{mp3_url}'")
else:
    print(f"Failed to download '{mp3_url}'")


audio_file= open(local_filename, "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)   
#print(transcript["text"])

url3 = 'https://zadania.aidevs.pl/answer/'+ token
def post_answ(url):
    payload = {"answer": transcript["text"]}
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