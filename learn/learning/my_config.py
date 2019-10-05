import os
import torch
from torchvision import transforms

# sets device for model and PyTorch tensors
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

frdir = "../fr/"
undir = "../un/"
uprdir= "../pro/"
famdir= "../fa/"
fridir= "../fd/"
kndir = "../kn/"
knpkl = "../kn/knval.pkl"

transformer=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])


