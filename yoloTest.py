#server_tcp.py
import socket
import time
from PIL import Image
import io
import pickle
import torch
import torch.cuda

#model の読み込み
device = torch.device("cuda" if torch.cuda.is_available() else "cpu" )
model = torch.hub.load('ultralytics/yolov5','yolov5s')
model.to(device)
model.eval()

img = Image.open('test2.jpg')
# img = img.resize((600, 600))
img.save("test.jpg")
result = model(img)
result.render()
result.show()
