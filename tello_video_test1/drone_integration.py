#drone_integration.py
#全ての処理をmacbook内で済ませる
#yoloを入れておくこと
import tello
from PIL import Image
import socket
import io
import pickle
import math
import sys
import time
from PIL import Image,ImageTk
import tkinter as tk
import torch
import numpy as np
import cv2

fov = math.radians(41)
tan_value = math.tan(fov)

#進む距離
x=1
y=0.5
#flag == true の時move_foward
flag = True
moveX_cnt = 0
moveY_cnt = 0
ROOMX =2000
ROOMY =1000
#drone接続
drone = tello.Tello('', 8889)
time.sleep(0.5)
#初めて対象を見つけた時のピクセルすう
A=0
B=0
#model の読み込み
model = torch.hub.load('ultralytics/yolov5','yolov5s')
time.sleep(0.5)


def move ():
    print("move呼び出し")
    time.sleep(0.5)
    exist = False
    frame=drone.read()
    if frame is None or frame.size == 0:
        print("frame is None")
        return exist
    result = model(frame)
    result.render()
    result.show()
    global moveX_cnt
    moveX_cnt +=1 

    #drone.move_forward(x)
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
        A = float(ymax-ymin)
        exist = True
        return exist
    print("見つからんかった、動いて次ループへ")
    time.sleep(5)
    drone.move_forward(x)
       
    return exist
def analyDistance(A,B):
    #print(f"A is {A},B is {B}")
    distance = B/(B-A)*x
    distanse = float(distanse)
    print(distance,type(distance))
    return distance
def final_move(A):
   time.sleep(3)
   print("もう少し")
   drone.move_forward(x)
   time.sleep(5)
   drone.move_down(x*tan_value)
   time.sleep(5)
   frame = drone.read()
   drone.move_up(x*tan_value)
   result = model(frame)
   result.render()
   result.show()
   #drone.move_forward(x)
   #obj に推論の結果の集合を代入
   obj = result.pandas().xyxy[0]
   #推論の結果のバウンディングボックスのクラスネームと座標を出力
   dic = {}
   B=0
   for i in range(len(obj)):
     name = obj.name[i]
     xmin = obj.xmin[i]
     ymin = obj.ymin[i]
     xmax = obj.xmax[i]
     ymax = obj.ymax[i]
     # 元の物体の高さ（ピくセル）を　A、後をBに
     if name =="bottle" :
       B= ymax-ymin
   if B==0:
      print("見失いました,近辺にある...ってこと？")
      drone.land()
      sys.exit()
   time.sleep(5)
   drone.move_forward(analyDistance(A,B))
   print("見つけました？、システムを終了します")
   drone.land()
   return 0
drone.takeoff()
time.sleep(5)
drone.move_up(0.5)
"""
drone.move_forward(3)
time.sleep(5)
drone.land()
"""
while True:
   try:
      time.sleep(3)
      #範囲ないかを確認
      if moveX_cnt*x>ROOMX:
         moveX_cnt=0
         moveY_cnt+=1
         if flag:
            drone.move_right(y)
         else:
            drone.move_left(y)
         drone.rotate_cw(180)
         flag ^=1
      if moveY_cnt*y > ROOMY:
         print("見つかりませんでした")
         drone.land()
         sys.exit()
        
      if move():
         print("とりあえず見つけた")
         time.sleep(3)
         drone.move_forward(x)
         time.sleep(3)
         drone.move_down(x*tan_value)
         time.sleep(3)
         frame = drone.read()
         result = model(frame)
         result.render()
         result.show()
         moveX_cnt+=1
         #drone.move_forward(x)
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
             result.show()
             B= float (ymax-ymin)
             break
         if B==0:
            print("見失いました,近辺にある...ってこと？")
            drone.land()
            sys.exit()
         else:
            distanse = analyDistance(A,B)
            print(distanse)
            drone.move_forward(distanse)
            break
      else:
         continue
       
   except KeyboardInterrupt:
    print ('\n . . .\n')
    del drone
    break
print("while抜けました")
time.sleep(5)
drone.rotate_cw(90)
time.sleep(3)
frame = drone.read()
result = model(frame)
result.render()
#result.show()
moveX_cnt+=1
#drone.move_forward(x)
#obj に推論の結果の集合を代入
obj = result.pandas().xyxy[0]
#推論の結果のバウンディングボックスのクラスネームと座標を出力
dic = {}
flag2 = False
for i in range(len(obj)):
  name = obj.name[i]
  xmin = obj.xmin[i]
  ymin = obj.ymin[i]
  xmax = obj.xmax[i]
  ymax = obj.ymax[i]
  # 元の物体の高さ（ピくセル）を　A、後をBに
  if name =="bottle" :
     A = ymax-ymin
     flag2 = True
if flag2 :
   final_move(A)
else:
   drone.rotate_cw(180)
   for i in range(len(obj)):
    name = obj.name[i]
    xmin = obj.xmin[i]
    ymin = obj.ymin[i]
    xmax = obj.xmax[i]
    ymax = obj.ymax[i]
    # 元の物体の高さ（ピくセル）をA、後をBに
    if name =="bottle" :
       A = ymax-ymin
       flag2 = True
       final_move(A)
    
if flag==False:
   print("見失いました,近くにあるはずです")
   drone.land()


