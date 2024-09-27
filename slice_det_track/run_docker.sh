docker run -it --rm --gpus all \
    --privileged \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v /mnt/wslg:/mnt/wslg \
    -e DISPLAY=$DISPLAY \
    -v /home/ernestlwt/workspace/github/testbeds/slice_det_track:/workspace \
ernestlwt/inference_pipeline bash