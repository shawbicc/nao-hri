import zmq
from gtts import gTTS
import os
from playsound import playsound


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


while True:

    message = socket.recv_string()
    print(f"Received message: {message}")

    tts = gTTS(text=message, lang='en')
    tts.save("message.mp3")
    playsound("message.mp3")
    
    socket.send_string("Message received and spoken on laptop")
    os.remove("message.mp3")
