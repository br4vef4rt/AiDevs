from flask import Flask, jsonify, request
import json
import os
import openai

def getGptAnswer(t_message, model):  
    openai.api_key = os.getenv("OPENAI_API_KEY") 
    completion1 = openai.ChatCompletion.create(
    model= model,
    messages = t_message   
    )
   
    return completion1.choices[0].message['content']

app = Flask(__name__)

@app.route('/ownapi_1', methods=['POST'])
def ownapi_1():
    # Extract the 'question' field from the JSON request
    s_question = request.json.get('question', 'No question provided')

    t_message1 = [
    {"role": "system", "content": "Your task is to answwer the processed question ultra concisely. Return the short answer and nothing else. If there is no question return 0."},
    {"role": "user", "content": f"Question to process: {s_question}"}
    ]
    s_GptAnswer =  getGptAnswer(t_message1,"gpt-4-1106-preview")
    # You can now use the 'question' variable as needed
    # For demonstration, we'll just return it in the response
    return jsonify({"reply": s_GptAnswer})

if __name__ == '__main__':
    app.run(debug=True, host='localhost')
