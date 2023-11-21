from flask import Flask, jsonify, request
import json
import os
import openai

s_context = ""

def read_file_to_string(filename):
    """Read the content of a file and return it as a string."""
    with open(filename, 'r') as file:
        return file.read()

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
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, 'context.txt')
    s_context = read_file_to_string(file_path)
    
    # Extract the 'question' field from the JSON request
    s_question = request.json.get('question', 'No question provided')

    t_message1 = [
    {"role": "system", "content": f"Your task is to give SHORT answer to the processed input. If the input IS NOT the question return 'OK'. If the input IS the question first try to answer based on given_context (data collected from the previous conversations with the same person) then try to use your knowledge if necessery"},
    {"role": "user", "content": f"given_context = [{s_context}]; input: '{s_question}';"}
    ]
    
    s_GptAnswer =  getGptAnswer(t_message1,"gpt-4-1106-preview")
    if s_GptAnswer =='OK':
        with open(file_path , 'a') as file:
            file.write(s_question + '\t')
    return jsonify({"reply": s_GptAnswer})

if __name__ == '__main__':
    app.run(debug=True, host='localhost')
