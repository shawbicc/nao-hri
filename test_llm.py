from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a helpful assistant. Answer in a single sentence."},
    {"role": "user", "content": "What is a Robot?"}
  ]
)

print(response.choices[0].message.content)