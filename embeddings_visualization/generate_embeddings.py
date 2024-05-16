import torch
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torchvision.datasets import ImageFolder
from torchvision.io import read_image
from torchvision.models import efficientnet_b1
from torchvision.models.feature_extraction import create_feature_extractor
from torchvision import transforms

from PIL import Image
import json
import glob
from tqdm import tqdm
import numpy as np

# init model
model = efficientnet_b1(pretrained=True)
model.eval()
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = model.to(device)
return_nodes = {'flatten': 'flatten'}
feature_extractor = create_feature_extractor(model, return_nodes=return_nodes)

# create dataloader
transforms = transforms.Compose([
    transforms.Resize(256, interpolation=transforms.InterpolationMode.BICUBIC),
    transforms.CenterCrop(240),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
catdog_dataset = ImageFolder("data/", transform=transforms)
dataloader = DataLoader(catdog_dataset, batch_size=16, shuffle=True, num_workers=0)

writer = SummaryWriter(comment='embedding_visualization')

features_np = np.empty((0,1280))
initial_size = 0
max_str_length = 10  # Maximum length of each string
image_labels_idx = []
with torch.no_grad():
    for inputs, labels in tqdm(dataloader, total=len(dataloader)):
        inputs = inputs.to(device)
        features = feature_extractor(inputs)
        flatten_fts = features["flatten"].squeeze()
        features_np = np.append(features_np, flatten_fts.detach().cpu().numpy(), axis=0)
        image_labels_idx.extend(labels)

# sanity check
print(features_np.shape)
print(len(image_labels_idx))
image_labels = [catdog_dataset.classes[x] for x in image_labels_idx]

writer.add_embedding(
    features_np,
    metadata=image_labels
)
writer.close()