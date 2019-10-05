import os
import torch
from torchvision import transforms

# sets device for model and PyTorch tensors
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

frdir = "../fresh/"
undir = "../unknown/"
uprdir= "../unpro/"
famdir= "../family/"
fridir= "../friends/"
kndir = "../known/"
knpkl = "../known/knval.pkl"

transformer=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])


