# -*- coding: utf-8 -*-
"""Coding Challenge (building model)

Automatically generated by Colaboratory.

Original file is located at

"""

from google.colab import drive
drive.mount('/content/drive')

# path='/MyDrive/AICodingChallenge'

!ls "/content/drive/My Drive"

import torch
from torchvision import transforms , datasets
from torch.utils.data import DataLoader

import os
dataset_path = '/content/drive/My Drive/AICodingChallege'

if os.path.exists(dataset_path):
  print(f"The directory '{dataset_path}' exists")

else:
  print(f"The directory '{dataset_path}' does not exists'")

transform = transforms.Compose([
    transforms.Resize((224,224)),transforms.ToTensor(),
])

dataset = datasets.ImageFolder(root=dataset_path,transform=transform)

classes = dataset.classes
print(classes)

print(dataset.class_to_idx)

batch_size=32
data_loader = DataLoader(dataset,batch_size=batch_size,shuffle=True)

for images,labels in data_loader:
  print("Image batch shape",images.shape)
  print("Label batch shape",labels.shape)
  break;

heritage_sites_urls = {
    "Krishna Mandir":"https://saarang.com.np/story/krishna-mandir/",
    "Kal Bhairav":"https://saarang.com.np/story/kal-bhairav/",
    "Rani Pokhari":"https://saarang.com.np/story/rani-pokhari/",
     "Baudhanath":"https://saarang.com.np/story/baudanath/",
     "Dharahara":" https://saarang.com.np/story/dharahara/",


}

for class_name,url in heritage_sites_urls.items():
  print(f"Heritage Site:{class_name}, URL:{url}")

import torch.nn as nn
class MultiClassCNN(nn.Module):
  def __init__(self,num_classes):
    super(MultiClassCNN,self).__init__()
    self.conv1 = nn.Conv2d(4,16,kernel_size=3,stride=1,padding=1)
    self.relu = nn.ReLU()
    self.pool = nn.MaxPool2d(kernel_size=2,stride=2)
    self.flatten = nn.Flatten()
    self.fc = nn.Linear(16*112*112,num_classes)
    self.softmax = nn.Softmax(dim=1)
  def forward(self,x):
    x = self.pool(self.relu(self.conv1(x)))
    x = self.flatten(x)
    x = self.fc(x)
    x = self.softmax(x)
    return x

import torch
from torchvision.models import (resnet18,ResNet18_Weights)
from torchvision import transforms
weights = ResNet18_Weights.DEFAULT
model = resnet18(weights = weights)
transforms = weights.transforms()

data_path = '/content/drive/My Drive/AICodingChallege/RaniPokhari/RaniPokhari/'
from PIL import Image

model.eval()

for filename in os.listdir(data_path):
  if filename.endswith((".jpg",".png")):
    filepath = os.path.join(data_path,filename)
    image =Image.open(filepath)
    image = image.convert('RGB')
    image_tensor = transform(image)
    image_reshaped = image_tensor.unsqueeze(0)


    with torch.no_grad():
      pred = model(image_reshaped).squeeze(0)

    pred_cls = pred.softmax(0)
    cls_id = pred_cls.argmax().item()
    cls_name = weights.meta['categories'][cls_id]

    print(cls_name)

data_path = '/content/drive/My Drive/AICodingChallege/RaniPokhari/RaniPokhari/'

if os.path.exists(data_path):
  print(f"The path '{data_path}' exists")
else:
  print(f"The path '{data_path}' does not exists")

from torchvision.transforms import  transforms
transform = transforms.Compose([transforms.Resize(224),transforms.PILToTensor()])
image_tensor = transform(image)

from torchvision.utils import draw_bounding_boxes
x_min, y_min, x_max, y_max = 10, 10, 100, 100
bbox = torch.tensor([x_min,y_min,x_max,y_max])
bbox = bbox.unsqueeze(0)
bbox_image = draw_bounding_boxes(image_tensor,bbox,width=3,colors="red")

transform = transforms.Compose([transforms.ToPILImage()])
pil_image = transform(bbox_image)

import matplotlib.pyplot as plt

plt.imshow(pil_image)

!pip -qqq install torchvision

from torchvision.models.detection.rpn import AnchorGenerator
anchor_generator = AnchorGenerator(
sizes=((32, 64, 128),),
aspect_ratios=((0.5, 1.0, 2.0),),
)

from torchvision.ops import MultiScaleRoIAlign
roi_pooler = MultiScaleRoIAlign(
featmap_names=["0"],
output_size=7,
sampling_ratio=2,
)

from torchvision.models.detection import FasterRCNN
import torchvision

backbone  = torchvision.models.mobilenet_v2(weights="DEFAULT").features
backbone.out_channels = 1200
num_classes=20
model = FasterRCNN(backbone = backbone,
                   num_classes=num_classes,
                   rpn_anchor_generator= anchor_generator,
                   box_roi_pool = roi_pooler,
                   )

from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights="DEFAULT")

num_classes = 20
in_features = model.roi_heads.box_predictor.cls_score.in_features

model.roi_heads.box_predictor = FastRCNNPredictor(in_features,num_classes)

