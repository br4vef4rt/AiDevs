import requests
import json

token = 'none'
taskMsg = 'none'
url = 'https://zadania.aidevs.pl/token/helloapi'  # Replace with your URL

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
            taskMsg = response.json()["msg"]
        else:
            print(f'Successfully posted data: {json.dumps(payload)}')
            print(f'Failed to post data. Status code: {response.status_code}')
            print(f'Response: {response.text}')
            

    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')

    
post_json_to_url(url)

print(token)
print(taskMsg)
