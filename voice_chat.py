import zmq
from openai import OpenAI
from unidecode import unidecode
import speech_recognition as sr

client = OpenAI()


def get_openai_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a NAO Robot. Answer users question in a friendly way in a single sentence."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def get_speech_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Speech Recognition service is not available.")
            return None

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

while True:
    print("Say something (or say 'exit' to quit): ")
    
    prompt = get_speech_input()

    if prompt and prompt.lower() == 'exit':
        print("Exiting...")
        break


    if prompt:
        openai_response = get_openai_response(prompt)
        openai_response = unidecode(openai_response)
        
        socket.send_string(openai_response)
        message = socket.recv_string()
        print(f"Received ack from NAO: {message}")
