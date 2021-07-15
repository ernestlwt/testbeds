docker run -ti --rm \
    --net host \
    --name triton_client \
    -v /home/ernestlwt/workspace/github/testbeds/triton_python_backend/models/add_sub/client.py:/client.py \
nvcr.io/nvidia/tritonserver:21.06-py3-sdk python3 /client.py