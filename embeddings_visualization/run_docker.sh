docker run -it --rm --gpus all \
    -v /home/ernestlwt/workspace/github/testbeds/:/workspace/testbeds/ \
    -p 6006:6006 \
embedding_visualization bash