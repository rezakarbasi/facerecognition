# How to initialize the project
### Buile the _deepface_ docker image
_deepface_ is an opensource project which can extract and embed the face images inside an image file or data. Thus, we need to first make the container. So, in order to make the _deepface_ docker image stand in the repo's root and:
- `cd third-party/deepface/`
- `docker build -t deepface .`

### Buile the docker image that main docker image
_my-api_ is the designed api which extracts the embedded vectors for the reference files, splits the incoming video and make the output to say when and where did the person has been seen. So, to build the docker image, stand in the repo's root and:
- `cd docker`
- `docker build -t my-api .`


# In the inference time
In the reference time, we need to specify the video file for _my-api_ container and it do the rest.

First of all run the docker compose file : `docker-compose up` (make sure to replace volume according to your reference's local path).

Check that the two containers are up and ready to be used.

Then follow the procedure in the test.sh file. You may modify the `export` lines and then run `sh run.sh`. The code will send a request to the _my-api_ container and it splits the video into frames, feeds it into the _deepface_, makes dotproduct on the embedded results and returns a dictionary as the output.


# The output dictionary is just like this
```json
[{"time": 22.0, "confidence": 1.0, "area": {"h": 58, "left_eye": [916, 194], "right_eye": [936, 195], "w": 43, "x": 903, "y": 172}, "dot_product": 83.38889444312156}, ...]
```