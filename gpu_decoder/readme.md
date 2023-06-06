# OPENCV Solution

GPU slower then CPU. This also seems to be the behavior at https://github.com/chenxinfeng4/ffmpegcv

## Build
```
docker build -t erenstlwt/opencv_reader:gpu_h265 opencv/.
docker build -t erenstlwt/opencv_reader:gpu_h264 --build-arg CODEC="h264"  opencv/.

docker build -t erenstlwt/opencv_reader:cpu -f opencv/Dockerfile.cpu opencv/.

```

## Run Container
```
# on terminal 1

# gpu
# change container tag depending on codec version
docker run --gpus all -it --net host \
    -v /home/ernestlwt/workspace/github/testbeds/gpu_decoder/:/repo \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v /mnt/wslg:/mnt/wslg \
    -v /usr/lib/wsl:/usr/lib/wsl \
    --device=/dev/dxg -e DISPLAY=$DISPLAY \
    -e WAYLAND_DISPLAY=$WAYLAND_DISPLAY -e XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR \
    -e PULSE_SERVER=$PULSE_SERVER \
    erenstlwt/opencv_reader:gpu_h265 bash

# cpu
docker run -it --net host \
    -v /home/ernestlwt/workspace/github/testbeds/gpu_decoder/:/repo \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v /mnt/wslg:/mnt/wslg \
    -v /usr/lib/wsl:/usr/lib/wsl \
    --device=/dev/dxg -e DISPLAY=$DISPLAY \
    -e WAYLAND_DISPLAY=$WAYLAND_DISPLAY -e XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR \
    -e PULSE_SERVER=$PULSE_SERVER \
    erenstlwt/opencv_reader:cpu bash

# for cpu only
pip install opencv-python

```

# Simulate stream
```
# on terminal 2

docker run --rm -it -e MTX_PROTOCOLS=tcp -p 8554:8554 -p 1935:1935 -p 8888:8888 -p 8889:8889 aler9/rtsp-simple-server


# on terminal 3

# h264
ffmpeg -re -stream_loop -1 -i /mnt/c/Users/ernes/Videos/people_walking.mp4 -c copy -f rtsp rtsp://localhost:8554/mystream
# h265/hevc
ffmpeg -re -stream_loop -1 -i /mnt/c/Users/ernes/Videos/people_walking.mp4 -c copy -f rtsp -c:v libx265 rtsp://localhost:8554/mystream


```