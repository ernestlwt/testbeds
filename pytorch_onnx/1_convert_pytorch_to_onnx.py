import torch
import torchvision.transforms as transforms
from torchvision.models import efficientnet_b1

import numpy as np

with open("imagenet_classes.txt", "r") as f:
    classes = f.readlines()

# Use CPU for converting model
device = torch.device("cpu")
model = efficientnet_b1()
model.load_state_dict(torch.load("./efficientnet_b1-c27df63c.pth"))
model.eval().to(device)

batch_size = 1 # does not matter since we will be making this dynamic during conversion
w = 224
h = 224
x = torch.randn(batch_size, 3, h, w, requires_grad=True).to(device)
torch_out = model(x)

torch.onnx.export(
    model,
    x,
    "model.onnx",
    export_params=True,
    opset_version=16,
    do_constant_folding=True,
    input_names = ['input'],
    output_names = ['output'],
    dynamic_axes={'input' : {0 : 'batch_size'}, 'output' : {0 : 'batch_size'}} # dynamic batch size
)
print("model converted to onnx")

import onnx
import onnxruntime

onnx_model = onnx.load("model.onnx")
onnx.checker.check_model(onnx_model)
print("onnx model checked")
providers = ["CPUExecutionProvider"]
ort_session = onnxruntime.InferenceSession("model.onnx", providers=providers)

def to_numpy(tensor):
    return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()

# compute ONNX Runtime output prediction
ort_inputs = {ort_session.get_inputs()[0].name: to_numpy(x)}
ort_outs = ort_session.run(None, ort_inputs)

# compare ONNX Runtime and PyTorch results
np.testing.assert_allclose(to_numpy(torch_out), ort_outs[0], rtol=1e-03, atol=1e-05)

print("Exported model has been tested with ONNXRuntime, and the result looks good!")

