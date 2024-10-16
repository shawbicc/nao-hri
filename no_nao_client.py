import zmq
from gtts import gTTS
import os
# from playsound import playsound
import pygame


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


while True:

    message = socket.recv_string()
    print("Received message: {}".format(message))

    print("gtts called")
    tts = gTTS(text=message, lang='en')
    print("gtts saving audio")
    try:
        tts.save("message.mp3")
    except InsecureRequestWarning:
        pass
    # Initialize the pygame mixer
    pygame.mixer.init()

    # Load and play the sound
    pygame.mixer.music.load('message.mp3')
    pygame.mixer.music.play()

    # Keep the program running until the sound finishes playing
    while pygame.mixer.music.get_busy():
        pass
    
    socket.send_string("Message received and spoken on laptop")
    os.remove("message.mp3")
