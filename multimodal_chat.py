######### MULTIMODAL CHAT ##############
# general flow: 
#   - collect voice input and convert to text
#   - capture image from webcam
#   - save prompt (image+text) in history
#   - send the history along with new prompt to chatgpt api
#   - save response in history
#   - send the response over the websocket    
# 
######## INSTRUCTIONS BEFORE USE #############
#   - Install the requirements in llm_requirements.txt (new libraries were included to the original version)
#   - Make sure to have a working webcam and microphone connected to the pc
#   - Run this program in the llm environment
#   - Run the Nao client or no_nao_client in a separate terminal in the nao environment


from openai import OpenAI
import cv2
import base64
from io import BytesIO
import zmq
from unidecode import unidecode
import speech_recognition as sr

client = OpenAI()

# Initialize an empty message history
conversation_history = [
    {"role": "system", "content": "You are a helpful assistant."}
]

# get speech input from mic and convert to text
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

# capturing image from the webcam and resizing to 360p for lower cost prompts
def capture_and_resize_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cap.release()
        # Resize image to 640x360 (360p)
        resized_frame = cv2.resize(frame, (640, 360))
        # cv2.imwrite('demo.jpg', resized_frame) # for checking if camera is working
        return resized_frame
    else:
        cap.release()
        raise Exception("Could not capture image from webcam")
    
# Convert image to base64-encoded string
def image_to_base64(image):
    _, buffer = cv2.imencode('.jpg', image)  # Encode image to jpg format
    base64_image = base64.b64encode(buffer).decode('utf-8')
    return base64_image

# Prepare the prompt and image to send
def get_response_with_image(user_input, image):
    # Convert image to base64
    base64_image = image_to_base64(image)

    # add the new prompt to history
    conversation_history.append({
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": user_input
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        })

    # get chatgpt response with input as text and an image (including history)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages = conversation_history,
        # max_tokens = 300
    )
    # Get the reply
    assistant_reply = completion.choices[0].message.content
    # save the reply in history
    conversation_history.append({"role": "assistant", "content": assistant_reply})
    
    return assistant_reply


if __name__ == "__main__":

    # initiate a socket
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    # keep listening for input
    while True:
        print("Say something (or say 'exit' to quit): ")
        
        prompt = get_speech_input()

        if prompt and prompt.lower() == 'exit':
            print("Exiting...")
            break

        # send an api call if a proper voice input is received
        if prompt:
            image = capture_and_resize_image() # capture an image from webcam
            response = get_response_with_image(prompt, image)
            response = unidecode(response)
            
            # send the response into the socket to Nao robot
            socket.send_string(response)
            message = socket.recv_string()
            print(f"Received back from NAO: {message}")
