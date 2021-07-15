docker run -ti --rm \
    --shm-size=1g \
    --ulimit memlock=-1 \
    --ulimit stack=67108864 \
    -p 8000:8000 \
    -p 8001:8001 \
    -p 8002:8002 \
    --name triton_server \
    -v /home/ernestlwt/workspace/github/testbeds/triton_python_backend/models:/models \
    -v /home/ernestlwt/workspace/github/testbeds/triton_python_backend/pytorch_env.tar.gz:/pytorch_env.tar.gz \
    -v /home/ernestlwt/workspace/github/testbeds/triton_python_backend/models/pytorch_classifier/weights.pth:/weights.pth \
    -v /home/ernestlwt/workspace/github/testbeds/triton_python_backend/models/pytorch_classifier/imagenet_class_index.json:/imagenet_class_index.json \
nvcr.io/nvidia/tritonserver:21.06-py3 tritonserver --model-repository /models
