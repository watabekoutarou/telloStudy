#server_drone.py
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
import sys
#物体が写る画像1と物体の検出範囲が同一で100mm前進した画像によって距離の推定を行う(ただし物体と同じクラスは検出されないものとする)

M_size = 65535
def square(xmin,xmax,ymin,ymax):
  return (xmax-xmin)*(ymax-ymin)

#model の読み込み
device = torch.device("cuda" if torch.cuda.is_available() else "cpu" )
model = torch.hub.load('ultralytics/yolov5','yolov5s')
model.to(device)
model.eval()

#serverの情報
host = '192.168.11.6'
port = 8080
serverAddress = (host, port)
print("接続待機")
sock = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
print('create socket')
sock.bind(serverAddress)
sock.listen()
client_socket, client_address = sock.accept()
print("接続:",client_address)
A = 0
B = 99999
x = 200

def analyDistance(A,B):
    #print(f"A is {A},B is {B}")
    distance = str(int(B/(B-A)*x))
    print(distance,type(distance))
    return distance

while True:
  try:

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
    print("1komeの処理")
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
        A = ymax-ymin
        #対象があった場合clientに特別なメッセージを送信
        response = "discover"
        client_socket.send(response.encode())
        #対象があった場合distanceの計算のため
        # 2回目の画像送信を受信する
        message = client_socket.recv(M_size)
        data = pickle.loads(message)
        content = data.getvalue()
        #画像を保存
        img = Image.open(io.BytesIO(content))
        img = img.resize((640,480))
        result = model(img)
        result.render()
        result.show()
        print("2komeの処理")
        #obj に推論の結果の集合を代入
        obj = result.pandas().xyxy[0]
        for i in range(len(obj)):
            name = obj.name[i]
            xmin = obj.xmin[i]
            ymin = obj.ymin[i]
            xmax = obj.xmax[i]
            ymax = obj.ymax[i]
            if name =="bottle" :
              print("x軸の基準決定")
              B = ymax-ymin
              break
        if B != 99999:
           distance = analyDistance(A,B)
           #response = distance.encode('utf-8')
           client_socket.send(distance.encode('utf-8'))
           print("1こめのdistanse送信")
        else:
          print("見失いました")
          distance = 0
          client_socket.send(distance.encode('utf-8'))
        #y軸の計算
        B=99999
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
        for i in range(len(obj)):
            name = obj.name[i]
            xmin = obj.xmin[i]
            ymin = obj.ymin[i]
            xmax = obj.xmax[i]
            ymax = obj.ymax[i]
        # 元の物体の高さ（ピくセル）を　A、後をBに
            if name =="bottle" :
              A = ymax-ymin
              message = client_socket.recv(M_size)
              data = pickle.loads(message)
              content = data.getvalue()
              #画像を保存
              img = Image.open(io.BytesIO(content))
              img = img.resize((640,480))
              result = model(img)
              result.render()
              #result.show()
              #obj に推論の結果の集合を代入
              obj = result.pandas().xyxy[0]
              for i in range(len(obj)):
                  name = obj.name[i]
                  xmin = obj.xmin[i]
                  ymin = obj.ymin[i]
                  xmax = obj.xmax[i]
                  ymax = obj.ymax[i]
                  if name =="bottle" :
                      B = ymax-ymin
                      break
                  if B ==99999:
                     response = "end"
                     print("end1")
                     client_socket.send(response.encode('utf-8'))
                     sys.exit()
                  analyDistance(A,B)
        else:
           response = "end"
           print("end2")
           client_socket.send(response.encode('utf-8'))
           sys.exit()
      #画像に対象がなかった場合　clientにNoneを送信
    response="None"
    print(response)
    client_socket.send(response.encode('utf-8'))

  except KeyboardInterrupt:
    print ('\n . . .\n')
    client_socket.close()
    sock.close()
    break
