import naoqi
from naoqi import ALProxy


DESTINY = "192.168.1.69"
ROBOT_IP = DESTINY
PORT = 9559

tts = ALProxy("ALAnimatedSpeech",ROBOT_IP, PORT)
message= "I'm working fine! Thanks for checking me."
message_str = "\\style=didactic\\ \\vol=90\\ \\wait=5\\" + message
tts.say(message_str)