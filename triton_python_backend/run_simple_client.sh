docker run -ti --rm \
    --net host \
    --name triton_client \
    -v /home/ernestlwt/workspace/github/testbeds/triton_python_backend/models/pytorch_classifier/client.py:/client.py \
    -v /home/ernestlwt/workspace/github/testbeds/triton_python_backend/models/pytorch_classifier/dog.jpg:/dog.jpg \
nvcr.io/nvidia/tritonserver:21.06-py3-sdk python3 /client.py