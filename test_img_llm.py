from openai import OpenAI
import cv2
import base64
from io import BytesIO

client = OpenAI()

# Capture image from the webcam and resize to 360p
def capture_and_resize_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cap.release()
        # Resize image to 640x360 (360p)
        resized_frame = cv2.resize(frame, (640, 360))
        cv2.imwrite('demo.jpg', resized_frame)
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

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages = [
        {
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
        }
        ],
        max_tokens = 300
    )
    # Get the assistant's reply
    assistant_reply = completion.choices[0].message.content
    return assistant_reply


if __name__ == "__main__":
    # Capture, resize image, and send it along with a prompt
    image = capture_and_resize_image()
    user_prompt = input("Ask any question here: ")
    response = get_response_with_image(user_prompt, image)
    print(f"Assistant: {response}")