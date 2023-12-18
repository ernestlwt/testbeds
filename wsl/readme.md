# WSL Tips

# Table of Contents
1. [Using GPU on docker-compose](#using-gpu-on-docker-compose)
1. [Using Webcam](#using-Webcam)

# Using GPU on docker-compose
- Expose gpu to containers spawned from docker-compose. From [here](https://docs.docker.com/compose/gpu-support/)
```
services:
  test:
    image: nvidia/cuda:10.2-base
    command: nvidia-smi
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

# Using Webcam
This was much harder than it needed to be. 

Following this [video](https://www.youtube.com/watch?v=t_YnACEPmrM) helped but it is not all the steps required. Below are the required steps:
- Install the [wsl tool](https://learn.microsoft.com/en-us/windows/wsl/connect-usb) to attach USB from host to your wsl instances. Make sure to check all the pre-requisites
- Install the WSL Kernel from source with the required settings and restart WSL to use the new kernel. You can follow the [video](https://www.youtube.com/watch?v=t_YnACEPmrM) from 3min to 7:20min or till 8:20min to make sure your wsl can detect USB webcam

### Debugging Common Errors
- check permission of /dev/video*. chown rot:video and chmod 666 it
```
ernestlwt@Desk:~/workspace/github/testbeds$ ls -al /dev/video*
crw-rw-rw- 1 root video 81, 0 Dec 18 14:48 /dev/video0
crw-rw-rw- 1 root video 81, 1 Dec 18 14:48 /dev/video1
```
- Using webcam in docker in wsl. Below is the standard command you will need
```
docker run \
    --rm -it --gpus all \ 
    --privileged \                            # required to access webcam
    -v /tmp/.X11-unix:/tmp/.X11-unix \        # Required to link gui in docker to linux
    -v /mnt/wslg:/mnt/wslg \                  # Required to show gui from wsl to windows
    -v /dev:/dev \                            # your webcam are here
    -e DISPLAY=$DISPLAY \                     # Required to link gui in docker to linux
    <your container> bash
```