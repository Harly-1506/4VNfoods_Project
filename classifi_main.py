
from __future__ import print_function, division
import os
import torch
from torch.utils.data import Dataset, DataLoader
import PIL

import torch.nn as nn
import torchvision

from utils.processing import *
from utils.vnfood_ds import *
from utils.trainer import *
from model.mlp import *
from model.cnn import *
from model.vggnet import *
from model.resnet import *

os.system("pip install wandb")
"""## Processing data"""

train_paths, train_labels, val_paths, val_labels, test_paths, test_labels = getAllDataset()

train_dataset = FoodVNDs(train_paths, train_labels, transform = train_transform )
val_dataset = FoodVNDs(val_paths, val_labels, transform = test_transform )
test_dataset = FoodVNDs(test_paths, test_labels, transform = test_transform )

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers = 2, pin_memory= True)
valid_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers = 2, pin_memory= True)
test_loader = DataLoader(test_dataset, batch_size=1, shuffle=False, num_workers = 2, pin_memory= True)

# plot_images(train_loader)

from torchsummary import summary
device='cuda' if torch.cuda.is_available() else 'cpu'
model = miniVGG()
# model = vgg16(pretrained = True)
# model = resnet18(pretrained = True)


model.cuda()
summary(model, ((3,224,224)), batch_size = 32)

fit(model,train_loader,valid_loader, test_loader,max_epochs = 50, max_plateau_count = 15, wb = False)

# import matplotlib.pyplot as plt 
# from torchvision import transforms
# Name_food = {
#     0:"Banh mi",
#     1:"Com tam",
#     2:"Hu tieu",
#     3:"Pho"
# }
# loader = test_transform = transforms.Compose([
#     transforms.Resize((224,244)),
#     transforms.ToTensor(),
# ])


# def predict_signal_img(model, image_path, target = " "):

#   img = PIL.Image.open(image_path)
#   image = loader(img)
#   image = image.cuda()
#   image = image.unsqueeze(0) 
#   model.eval()
#   with torch.no_grad():

#     output = model(image)
#     _, predicted = output.max(1)
#     # Predicted class value using argmax
#     # Show result
#     # print(predicted)
#     plt.imshow(img)
#     plt.title(f'Prediction: {Name_food[predicted.item()]} - Actual target: {target}')
#     plt.show()

# predict_signal_img(model,"/content/download.jpg", "banhs mif" )
