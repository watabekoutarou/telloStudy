#ドローンで撮影した画像の中で対象が右、左のどこらへんか、中央か　で合計9パターンの領域のどれに該当するかを検証する
import tello
from PIL import Image
import socket
import io
import pickle
import math
import time
from PIL import Image,ImageTk
import tkinter as tk
import torch
import numpy as np
import cv2
import sys
A=0

#ドローンのカメラの焦点距離
fy=894.58
fx=890.97
def analyDistance(pix):
    #print(f"A is {A},B is {B}")
    h=0.2#メートル単位
    dis = h*fy/pix #h:dis=pix:fy
    dis = float(dis)
    print(f'pix is {pix}')
    print(f'distanse is {dis}\n')
    return dis
#システム本体
#drone接続
#drone = tello.Tello('', 8889)
#time.sleep(0.5)

#model の読み込み
model = torch.hub.load('ultralytics/yolov5','yolov5s')
time.sleep(0.5)
while True:  
    #frame = drone.read()
    frame = Image.open('sampledrone2.PNG')
    #frame=frame.resize((640,480))
    result = model(frame)
    result.render()
    obj = result.pandas().xyxy[0]
    dic = {}
      # 元の物体の高さ（ピくセル）を　A、後をBに
    for i in range(len(obj)):
      name = obj.name[i]
      xmin = obj.xmin[i]
      ymin = obj.ymin[i]
      xmax = obj.xmax[i]
      ymax = obj.ymax[i]
      # 元の物体の高さ（ピくセル）を　A、後をBに
      if name == "bottle" :
        print(f"ymin is {ymin},ymax is {ymax},xmin is {xmin},xmax is {xmax}\n")
        A = float(ymax-ymin)
        center = int(xmax-xmin)/2+xmin
        print(f"center si {center}")
        angle=int(center/(960/9))
        print(f"an si {angle}")
        #対象の角度を右、左10,20,30,40度と中央の９種類に分別
        if angle<4:
           angle=8/(angle+2)*10
           print(f"左側,{angle}度にあります")
        elif 4<angle:
           angle=(angle-4)*10
           print(f"右側,{angle}度にあります")
        if angle ==4:
           print("中央にあります")
    result.show()
    analyDistance(A)
    time.sleep(5)
    break
