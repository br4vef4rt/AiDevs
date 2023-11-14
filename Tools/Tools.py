import requests
import json
import os
import openai

s_question = None
s_msg = None
s_date = None


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
    global s_question, s_msg
    try:
        response = requests.post(url, headers=headers)
        
        if response.status_code == 200:
            print(f'Response: {response.json()}')
            s_question = response.json()["question"]  
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

def getGptTool(t_message, model, tools):
    openai.api_key = os.getenv("OPENAI_API_KEY") 
    completion1 = openai.ChatCompletion.create(
    model= model,
    tools = tools,
    messages = t_message
    )
    return completion1.choices[0].message['content']

def getGptAnswer(t_message, model):  
    openai.api_key = os.getenv("OPENAI_API_KEY") 
    completion1 = openai.ChatCompletion.create(
    model= model,
    messages = t_message   
    )
   
    return completion1.choices[0].message['content']



tools = [
    {
        "type": "function",
        "function": {
            "name": "ToDoList",
            "description": "ToDoList",
            "parameters": {
                "type": "object",
                "properties": {
                    "tool": {
                        "type": "string",
                        "description": "ToDo",
                    },
                    "desc": {
                        "type": "string",
                        "description": "Event Description",
                    },
                },
                "required": ["tool", "desc"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calendar",
            "description": "information that will be add to calendar",
            "parameters": {
                "type": "object",
                "properties": {
                    "tool": {
                        "type": "string",
                        "description": "Calendar",
                    },
                    "desc": {
                        "type": "string",
                        "description": "Task Description",
                    },
                    "date": {
                        "type": "string",
                        "description": "YYYY-MM-DD",
                    }
                },
                "required": ["tool", "desc", "date"]
            },
        }
    },
]




getToken('https://zadania.aidevs.pl/token/tools')
get_Task('https://zadania.aidevs.pl/task/'+ token)
print(s_question)

t_message1 = [
        #{"role": "system", "content": "If the request conserns certain date (or jutro or pojutrze) return the date in format YYYY-MM-DD, in other case return 0. Remember that 'jutro' is a date and is 2023-11-15, 'pojutrze' is a date and  2023-11-16, so it is calendar action and you can return date"},
        {"role": "system", "content": "Verify if process request contains date (or jutro or pojutrze or poniedziałek). If yes return this date and nothing else, if else return 0. Jutro is a date and is 2023-11-15, pojutrze is a date 2023-11-16, poniedziałek is a date 2023-11-20."},
        {"role": "user", "content": f"request to process: {s_question}"}
    ]  

s_gptAnswer =  getGptAnswer(t_message1, "gpt-4-1106-preview")
print(s_gptAnswer)

if s_gptAnswer != 0:
    s_date = s_gptAnswer

t_message_ToDo = [
        {"role": "system", "content": """Your task is, based on processed request,to return the answer in format (change only X):  {"tool":"ToDo","desc":"X"} and nothing else, where X is summary information based on request and it goes to ToDo list """},
        {"role": "user", "content": f"request to process: '{s_question}'"}
    ]  

t_message_Calendar = [
        {"role": "system", "content": """Your task is, based on processed request,to return the answer  in format (change only X and given_date): {"tool":"Calendar","desc":"X","date": "given_date"} and nothing else, where X is summary information based on request and it goes to Calendar """},
        {"role": "user", "content": f"given_date = {s_date}; request to process: {s_question}"}
    ]  

if s_gptAnswer == "0":
    s_gptAnswer =  getGptAnswer(t_message_ToDo, "gpt-4-1106-preview")
else:
    s_gptAnswer =  getGptAnswer(t_message_Calendar, "gpt-4-1106-preview")
print(s_gptAnswer)
j_gptAnswer = json.loads(s_gptAnswer)

post_answ('https://zadania.aidevs.pl/answer/'+ token, j_gptAnswer)