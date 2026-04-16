docker run \
    -it --rm --gpus all --privileged --shm-size=2g \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v /mnt/wslg:/mnt/wslg \
    -e DISPLAY=$DISPLAY \
    -v /home/ernestlwt/workspace/github/testbeds/depth_estimation:/workspace/depth_estimation \
ernestlwt/testbeds:depth_estimation bash