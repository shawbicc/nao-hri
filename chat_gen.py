import zmq
from openai import OpenAI
from unidecode import unidecode

client = OpenAI()

def get_openai_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a NAO Robot. Answer users question in a friendly way in single sentence."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

while True:
    prompt = input("Enter your question (or type 'exit' to quit): ")
    
    if prompt.lower() == 'exit':
        print("Exiting...")
        break
    
    openai_response = get_openai_response(prompt)
    openai_response = unidecode(openai_response)
    socket.send_string(openai_response)
    message = socket.recv_string()
    print(f"Received ack from NAO: {message}")
