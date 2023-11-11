import requests
import json
import os
import openai
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
import psycopg2


token = None
s_answer = None
s_question = None
s_gptAnswer = None
s_o_mnie = None
s_bomba = None
s_film = None
s_kolor = None
s_serial = None
s_wiek = None

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
    global s_question
    try:
        response = requests.post(url, headers=headers)
        
        if response.status_code == 200:
            print(f'Response: {response.json()}')
            s_question = response.json()["question"]      
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

def getInfofromSQL(imie,nazwisko):
    global s_o_mnie,s_bomba,s_film,s_kolor,s_serial,s_wiek
    try:
        conn = psycopg2.connect(
        dbname='DZDB',
        user='USER1',
        password='Trewq!23',
        host='localhost',
        port='5432'
        )

        cur = conn.cursor()
        query = f"SELECT o_mnie,  ulubiona_postac_z_kapitana_bomby, ulubiony_film, ulubiony_kolor, ulubiony_serial, wiek FROM people WHERE imie = '{imie}' and nazwisko = '{nazwisko}';"
        print(query)
        cur.execute(query)
        row = cur.fetchone() 
        s_o_mnie = row[0]
        s_bomba = row[1]
        s_film = row[2]
        s_kolor = row[3]
        s_serial = row[4]
        s_wiek = row[5]

        cur.close()
    except psycopg2.Error as e:
        print("Error: Could not execute the query")
        print(e)

post_json_to_url('https://zadania.aidevs.pl/token/people')
get_Task('https://zadania.aidevs.pl/task/'+ token)

t_message1 = [
        {"role": "system", "content": """Process given question as in example: IN: "co lubi jeść Tomek Bzik?" ANS: {"imie": "Tomek", "nazwisko": "Bzik"};  IN: "Czy wiesz kim jest Adam Małysz?" ANS: {"imie": "Adam", "nazwisko": "Małysz'"};  IN: "Czy Renata Pizza lubi jeść pizzę?" ANS: {"imie": "Renata", "nazwisko": "Pizza"};"""},
        {"role": "user", "content": f"Question to process: {s_question}"}
    ]  
s_gptAnswer =  getGptAnswer(t_message1, "gpt-3.5-turbo")
print(s_gptAnswer)
dict_gptAnswer = json.loads(s_gptAnswer)
getInfofromSQL(dict_gptAnswer['imie'],dict_gptAnswer['nazwisko'])
print(s_o_mnie)

t_message2 = [
        {"role": "system", "content": f"Your task is answer the given question based on the context, context = '{dict_gptAnswer['imie']} {dict_gptAnswer['nazwisko']}: {s_o_mnie}, ulubiona postac z kapitana bomby: {s_bomba}, ulubiony film: {s_film}, ulubiony kolor {s_kolor}, ulubione serial: {s_serial}, wiek: {s_wiek}"},
        {"role": "user", "content": f"Question to answer: {s_question}"}
    ]  

post_answ('https://zadania.aidevs.pl/answer/'+ token, getGptAnswer(t_message2, "gpt-4"))

