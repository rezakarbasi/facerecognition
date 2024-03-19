export LOCAL_PATH="/path/to/the/video/directory/"
export VIDEO_NAME="task-video.mp4"
export LOCAL_VIDEO_PATH="${LOCAL_PATH}${VIDEO_NAME}"

export CONTAINER_PATH="/app/video-folder/"
export CONTAINER_VIDEO_PATH="${CONTAINER_PATH}${VIDEO_NAME}"

export CONTAINER_ID="facerecognition-my-api-1"

docker cp $LOCAL_VIDEO_PATH $CONTAINER_ID:$CONTAINER_VIDEO_PATH
curl --location 'http://0.0.0.0:6000/process_video' --form "video_path=${CONTAINER_VIDEO_PATH}"
docker exec $CONTAINER_ID rm $CONTAINER_VIDEO_PATH
