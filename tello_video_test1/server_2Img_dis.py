#server_img_dis.py
import socket
import time
from PIL import Image,ImageTk
import tkinter as tk
import io
import pickle
import torch
import torch.cuda
import numpy as np
import cv2
#物体が写る画像1と物体の検出範囲が同一で100mm前進した画像によって距離の推定を行う(ただし物体と同じクラスは検出されないものとする)
M_size = 65535
def square(xmin,xmax,ymin,ymax):
  return (xmax-xmin)*(ymax-ymin)

#pc1がわの情報
host = '192.168.11.6'
port = 8080
serverAddress = (host, port)

sock = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
print('create socket')
sock.bind(serverAddress)
sock.listen()


#model の読み込み
device = torch.device("cuda" if torch.cuda.is_available() else "cpu" )
model = torch.hub.load('ultralytics/yolov5','yolov5s')
model.to(device)
model.eval()
print("接続待機")

client_socket, client_address = sock.accept()

print("接続:",client_address)
A = 0
B = 0
x = 100
cnt = 0
while True:
  try:

    if cnt ==2 :
      break
    cnt+=1
    message = client_socket.recv(M_size)
    #復元
    data = pickle.loads(message)
    #Bytesloから
    content = data.getvalue()
    #画像を保存
    img = Image.open(io.BytesIO(content))
    img = img.resize((640,480))
    #img.save("test3.jpg")
    result = model(img)
    result.render()
    result.show()
    #obj に推論の結果の集合を代入
    obj = result.pandas().xyxy[0]
    #推論の結果のバウンディングボックスのクラスネームと座標を出力
    dic = {}
    for i in range(len(obj)):
      name = obj.name[i]
      xmin = obj.xmin[i]
      ymin = obj.ymin[i]
      xmax = obj.xmax[i]
      ymax = obj.ymax[i]
      # 元の物体の高さ（ピくセル）を　A、後をBに
      if name =="bottle" :
        if cnt ==1:
          A = ymax-ymin

        if cnt ==2:
          B =ymax -ymin
    #"bottle"でじっけん
    if cnt == 2:
      #距離推定の式
      print(f"A is {A},B is {B}")
      distance = str(int(B/(B-A)*x))
      print(distance,type(distance))
      response = distance.encode('utf-8')
      client_socket.send(response)
  except KeyboardInterrupt:
    print ('\n . . .\n')
    client_socket.close()
    sock.close()
    break
