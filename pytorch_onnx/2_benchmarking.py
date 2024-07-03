import torch
import torchvision.transforms as transforms
from torchvision.models import mobilenet_v3_large

import numpy as np
import time

import onnx
import onnxruntime

with open("imagenet_classes.txt", "r") as f:
    classes = f.readlines()

device = torch.device("cuda")

def run_python_benchmark(batchsizes=[1], warmup_iter=5, benchmark_iter=100):
    model = mobilenet_v3_large(num_classes=4)
    model.load_state_dict(torch.load("./model.pt"))
    model.eval().to(device)


    print("********** PYTORCH BENCHMARK **********")

    for bs in batchsizes:
        # warmup
        warmup_x = torch.randn(bs, 3, 224, 224).to(device)
        for i in range(warmup_iter):
            torch_out = model(warmup_x)
        torch.cuda.synchronize() # wait for warmup to finish

        x = torch.randn(bs, 3, 224, 224).to(device)
        torch.cuda.synchronize()
        start_t = time.time()
        for i in range(benchmark_iter):
            torch_out = model(x)
        torch.cuda.synchronize()
        end_t = time.time()
        print("Time taken for bs {}: {}".format(bs, end_t - start_t))

def run_onnx_benchmark(batchsizes=[1], warmup_iter=5, benchmark_iter=100):
    providers = [("CUDAExecutionProvider", {"cudnn_conv_use_max_workspace": '1'})]
    ort_session = onnxruntime.InferenceSession("model.onnx", providers=providers)

    def to_numpy(tensor):
        return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()


    print("********** ONNX BENCHMARK **********")
    for bs in batchsizes:
        # warmup
        warmup_x = torch.randn(bs, 3, 224, 224, requires_grad=True).to(device)
        ort_inputs = {ort_session.get_inputs()[0].name: to_numpy(warmup_x)}
        for i in range(warmup_iter):
            ort_outs = ort_session.run(None, ort_inputs)
        torch.cuda.synchronize() # wait for warmup to finish

        x = torch.randn(bs, 3, 224, 224, requires_grad=True).to(device)
        ort_inputs = {ort_session.get_inputs()[0].name: to_numpy(x)}
        torch.cuda.synchronize()
        start_t = time.time()
        for i in range(benchmark_iter):
            ort_outs = ort_session.run(None, ort_inputs)
        torch.cuda.synchronize()
        end_t = time.time()
        print("Time taken for bs {}: {}".format(bs, end_t - start_t))


BATCHSIZES = [1, 4, 8, 16, 24, 32, 40, 64, 128, 256]
NUM_INTERATIONS = 100

# run_python_benchmark(BATCHSIZES, benchmark_iter=NUM_INTERATIONS)
run_onnx_benchmark(BATCHSIZES, benchmark_iter=NUM_INTERATIONS)