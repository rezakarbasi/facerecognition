# Required Libraries
import requests
import json
import base64
import cv2

def get_embedded(image, image_array=False, url="http://0.0.0.0:5000/represent"):
    if image_array:
        _, buffer = cv2.imencode('.jpg', image)
        encoded_string = "data:image/jpeg;base64," + base64.b64encode(buffer).decode('utf-8')
    else:
        # Read the image file and encode it as base64
        with open(image, "rb") as image_file:
            encoded_string = "data:image/jpeg;base64," + \
                base64.b64encode(image_file.read()).decode("utf8")

    # Prepare the payload data as JSON
    payload = json.dumps({
        "model_name": "Facenet",
        "detector_backend": "mtcnn",
        "img_path": encoded_string
    })

    # Set the request headers
    headers = {
        'Content-Type': 'application/json'
    }

    # Send a POST request to the API endpoint
    response = requests.request("POST", url, headers=headers, data=payload)

    response_dict = json.loads(response.text)

    return response_dict["results"] if "results" in response_dict else []
