
import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY") 

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": ""},
    {"role": "user", "content": "Return 'OK', nothing else"}
  ]
)

print(completion.choices[0].message)