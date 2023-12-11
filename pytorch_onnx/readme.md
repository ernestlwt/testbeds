# Using Onnx on Pytorch

### Compatibility
Tested on a RTX2080ti

- Check onnx compatibility [here](https://onnxruntime.ai/docs/reference/compatibility.html#onnx-opset-support)
- Check onnx runtime compatibilty to cuda & cudnn [here](https://onnxruntime.ai/docs/execution-providers/CUDA-ExecutionProvider.html#requirements)
- The dockerfile should work for most GPU. If you are installing locally, check your cuda, cudnn and driver version [here](https://docs.nvidia.com/deeplearning/cudnn/support-matrix/index.html)

Download sample model [here](https://download.pytorch.org/models/efficientnet_b1-c27df63c.pth). Source [here](https://pytorch.org/vision/main/_modules/torchvision/models/efficientnet.html#EfficientNet_B1_Weights). Labels file converted from source [here](https://s3.amazonaws.com/deep-learning-models/image-models/imagenet_class_index.json)

### Instructions
```
# step 1 build docker
docker build -t pytorch_onnx .

# step 2 run docker. do edit mount volumes in run_docker.sh
bash run_docker.sh

# step 3 go to folder
cd /workspace/testbeds/pytorch_onnx

# step 4 convert pytorch model to onnx
python 1_convert_pytorch_to_onnx.py 

# step 5 run benchmarking. adjust params as u see fit
python 2_benchmarking.py 
```

### Sample Results
```
********** PYTORCH BENCHMARK **********
Time taken for bs 8: 1.700500726699829
Time taken for bs 16: 1.727259635925293
Time taken for bs 32: 2.6443049907684326
Time taken for bs 64: 106.64503884315491

********** ONNX BENCHMARK **********
Time taken for bs 8: 0.8180742263793945
Time taken for bs 16: 1.3896229267120361
Time taken for bs 32: 2.5268664360046387
Time taken for bs 64: 4.882249593734741
Time taken for bs 128: 9.783576726913452
Time taken for bs 256: 19.469582557678223
```

### Insights
- In general, onnx is faster than pytorch
- Onnx uses less GPU RAM. On the results above, pytorch hit limit(12gb ram GPU) at bs 64 which is why it slows down. Onnx can go till batch size 128, 256(uses < 5gb ram) and more no issues.
- Onnx is slow when input batchsize is always changing. Consider padding inputs if using large batch size.
- Testing with fixed vs dynamic batch size onnx model shows negligible performance improvement(<1%). Suggest just using a dynamic batch size conversion for convenience
