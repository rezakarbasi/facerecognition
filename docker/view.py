from flask import Flask, render_template, request
from get_embed import get_embedded
import os
import cv2
import numpy as np
import json

reference_embeddeds = []
url = ""

app = Flask(__name__)

@app.route('/up', methods=['GET'])
def api_up():
    return "API is up and running"

@app.route('/process_video', methods=['POST'])
def process_video():
    print("Processing video===============================")
    global reference_embeddeds, url

    video_path = request.form.get('video_path')
    split_interval = int(request.form.get('split_interval', 2))

    print(video_path, split_interval)

    last_frame_time = 0

    # Read video file
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    fps = 14 if fps == 0 else fps
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    # Iterate over each frame
    output = []
    for frame_num in range(total_frames):
        # Calculate the exact time of the frame
        frame_time = frame_num / fps

        # Read the frame
        ret, frame = cap.read()

        # if frame_time < 24:
        #     continue
        # frame_path = f"frame_{frame_num}.jpg"
        # cv2.imwrite(frame_path, frame)
        # break

        # Skip if the frame is not in the split interval
        if frame_time - last_frame_time < split_interval:
            continue

        last_frame_time = frame_time

        # # # Convert the frame to a jpg file
        # frame_path = f"frame_{frame_num}.jpg"
        # cv2.imwrite(frame_path, frame)

        faces = get_embedded(frame, image_array=True, url=url)
        for face in faces:
            for ref in reference_embeddeds:
                # print(np.dot(face['embedding'], ref['embedding']), face['face_confidence'], face['facial_area'])
                if face['face_confidence']<0.2:
                    continue
                dot_product = np.dot(face['embedding'], ref['embedding'])
                if dot_product > 60:
                    output.append({
                        "time": frame_time,
                        "confidence": face['face_confidence'],
                        "area": face['facial_area'],
                        "dot_product": dot_product
                    })
                    # frame_path = f"frame_{frame_time}.jpg"
                    # cv2.imwrite(frame_path, frame)
                break


    # Release the video capture object
    cap.release()
    return json.dumps(output)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 6000))
    reference_path = os.environ.get('REFERENCE_PATH', "/app/reference")
    url = os.environ.get('URL', "http://0.0.0.0:5000/represent")

    _, _, files = next(os.walk(reference_path))
    reference_embeddeds = []
    for file in files:
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
            file_path = os.path.join(reference_path, file)
            faces = get_embedded(file_path, url=url)
            if len(faces):
                the_face = sorted(faces, key=lambda x: x['face_confidence'], reverse=True)[0]
                reference_embeddeds.append(the_face)

    app.run(debug=True, host='0.0.0.0', port=port)