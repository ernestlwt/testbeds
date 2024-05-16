import torch
from torchvision.io import read_image
from torchvision.models import efficientnet_b1, resnet18
from torchvision.models.feature_extraction import create_feature_extractor
from torchvision import transforms

from PIL import Image
import json

# Step 1: Initialize the model with the best available weights
model = efficientnet_b1(pretrained=True)
model.eval()

# Step 2: Initialize the transforms
transforms = transforms.Compose([
    transforms.Resize(256, interpolation=transforms.InterpolationMode.BICUBIC),
    transforms.CenterCrop(240),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Step 3: Create the feature extractor with the required nodes
return_nodes = {'flatten': 'flatten'}
feature_extractor = create_feature_extractor(model, return_nodes=return_nodes)

# Step 4: Load the image(s) and apply inference preprocessing transforms
image = Image.open("data/cat/cat.28.jpg")
model_input = transforms(image).unsqueeze(0)

# Step 5: Extract the features
features = feature_extractor(model_input)
flatten_fts = features["flatten"].squeeze()
print(flatten_fts.shape)

# test results
class_idx = json.load(open("imagenet_class_index.json"))
idx2label = [class_idx[str(k)][1] for k in range(len(class_idx))]

pred = model(model_input)
_, pred_idx = torch.max(pred.data, 1)
print(pred_idx)
print(idx2label[pred_idx])