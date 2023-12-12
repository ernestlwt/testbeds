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
Time taken for bs 1: 1.735076904296875
Time taken for bs 4: 1.723475456237793
Time taken for bs 8: 1.7585182189941406
Time taken for bs 16: 1.7889375686645508
Time taken for bs 24: 2.145313024520874
Time taken for bs 32: 2.628380060195923
Time taken for bs 40: 11.467475175857544

********** ONNX BENCHMARK **********
Time taken for bs 1: 0.5265777111053467
Time taken for bs 4: 0.6996495723724365
Time taken for bs 8: 0.9364244937896729
Time taken for bs 16: 1.4502336978912354
Time taken for bs 24: 2.013993501663208
Time taken for bs 32: 2.5413014888763428
Time taken for bs 40: 3.0846469402313232
Time taken for bs 64: 4.815320253372192
Time taken for bs 128: 9.49012565612793
Time taken for bs 256: 19.187354564666748
```

### Insights
- In general, onnx is faster than pytorch
- Onnx uses less GPU RAM. On the results above, pytorch hit limit(12gb ram GPU) at bs 64 which is why it slows down. Onnx can go till batch size 128, 256(uses < 5gb ram) and more no issues.
- Onnx is slow when input batchsize is always changing. Consider padding inputs if using large batch size.
- Testing with fixed vs dynamic batch size onnx model shows negligible performance improvement(<1%). Suggest just using a dynamic batch size conversion for convenience
