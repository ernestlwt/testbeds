# Running deep learning services on triton's python backend
---
### Running default example  
*Referenced from https://github.com/triton-inference-server/python_backend*

1) Run triton server container to start up the service and a client that is calling the service
```
# in seperate terminals
bash run_example_server.sh
bash run_example_client.sh
```
---

### Running a simple example of customizing model and environment
1) Edit docker volume location of `run_simple_server.sh` and `run_simple_client.sh` accordingly
1) Run triton server container to start up the service and a client that is calling the service in seperate terminals
```

bash run_simple_server.sh
bash run_simple_client.sh
```
The model used here is the resnet18 from https://pytorch.org/vision/stable/models.html. Weights are downloaded via setting the pretrained flag and can be found on your system in `~/.cache/torch/hub/checkpoints/` 

### Important notes
If you are using a python version different from python 3.8, you will have to [refer to point 1 "Building Custom Python Backend Stub" of this link](https://github.com/triton-inference-server/python_backend#using-custom-python-execution-environments). 

* Take note that you will have to have a gcc version <= 8. You can refer to [this link](https://linuxconfig.org/how-to-switch-between-multiple-gcc-and-g-compiler-versions-on-ubuntu-20-04-lts-focal-fossa)
* You will also need nvcc so you can get it by installing cudatoolkit on the ***host***. Just `sudo apt-get install cudatoolkit`

If you are using python 3.8 but you have additional libraries required, you will have to [refer to point 2 "Packaging the Conda Environment" of this link](https://github.com/triton-inference-server/python_backend#using-custom-python-execution-environments). 

---

### Useful Links

Source files:  
[pb_utils](https://github.com/triton-inference-server/python_backend/blob/main/src/resources/triton_python_backend_utils.py)  
[http client](https://github.com/bytedance/triton-inference-server/blob/master/docs/model_configuration.md)

Triton configurations:  
[.pbtxt](https://github.com/bytedance/triton-inference-server/blob/master/docs/model_configuration.md)  
[http protocol](https://github.com/kubeflow/kfserving/blob/master/docs/predict-api/v2/required_api.md)

---

### TODOs
figure out how to send image via http form data