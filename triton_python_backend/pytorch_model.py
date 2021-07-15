import torchvision.models as models
import torch
from torchvision import transforms

from PIL import Image
import numpy as np
import json

model = models.resnet18(pretrained=True)
model.eval()

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


image = Image.open("./models/pytorch_classifier/dog.jpg")
image = transform(image)
batch_t = torch.unsqueeze(image, 0)

if torch.cuda.is_available():
    batch_t = batch_t.to('cuda')
    model = model.to('cuda')

out = model(batch_t)

with open("./imagenet_class_index.json") as f:
    classes_file = json.load(f)
    classes = [classes_file[str(i)][1] for i in range(0, 1000)]

probabilities = torch.nn.functional.softmax(out[0], dim=0)

top_5_p, top_5_i = torch.topk(probabilities, 5)
print(top_5_p)
print(classes[top_5_i[0]])
