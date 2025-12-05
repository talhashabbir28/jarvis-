from openai import OpenAI
 
# pip install openai 
# if you saved the key under a different environment variable name, you can do something like:
client = OpenAI(
  api_key="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",
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
    {"role": "user", "content": "what is coding"}
  ]
)

print(completion.choices[0].message.content)