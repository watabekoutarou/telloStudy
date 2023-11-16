#角度も推定して動かす、音声認識はコメントアウトしている
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
import speech_recognition as sr
#事前に設定した探索する単語群(vector<str>)
strSet = ["水筒","リモコン","時計"]
#単語と学習モデルのラベリングのペア
dict = {"水筒":"bottle","リモコン":"remote control","時計":"watch","nothing":"nothing","bottle":"bottle"}
dictHigh = {"bottle":0.2}
fov = math.radians(41)#視野角
tan_value = math.tan(fov)

#進む距離
x=1
y=0.4
#flag == true の時move_foward
flag = True
receptionFlag=False
moveX_cnt = 0
moveY_cnt = 0
#探索範囲
ROOMX =3
ROOMY =2
#false=左、True = 右   
LRflag=False
#初めて対象を見つけた時のピクセルすう
A=0
B=0
#ドローンのカメラの焦点距離
fy=894.58
fx=890.97

lcr = 0
#左~中央~右を0~4~8で表す

def isolate_word(text):
    flag = False
    cnt = 0
    for i in range(len(text)-3):
        if text[i:i+4] =="ドローン":
            flag = True
            locate = i+5
    target = "nothing"
    if not flag:
        print(text)
        print("not drone call\n")
        return target
    for x in strSet:
        if len(text)-locate>=0 and x==text[locate:locate+len(x)]:
            #print(x)
            target=x
            break
    print(f'target is{target} ,this label is {dict[target]}\n')
    target=dict[target]
    return target
#実験用の.wavファイルのカウント変数

def speech_reception():
    #wavCnt=1#音声ファイル１〜連続で入力するようのカウント変数
    while True:
            r = sr.Recognizer()

            ###
            #実験用ファイルナンバリング
            """
            if wavCnt ==9:
                sys.exit()
            wavStr=str(wavCnt)
            #.wav実験用
            wavFailName="sample"+wavStr+".wav"
            print(f'{wavFailName}\n')
            wavCnt+=1
            with sr.AudioFile(wavFailName) as source:
                audio = r.record(source)
            """
            ###

            print("\n")
            cnt = 0
            with sr.Microphone() as source:
                print("Say something!")
                audio = r.listen(source)
            
            text = r.recognize_google(audio,language="ja-JP")
            try:
                print("Google Speech Recognition thinks you said " + text)
                lenText = len(text)
                for i in range(int(lenText/2)):
                    if (text[i]=='ス' or text[lenText-1-i]=='プ'):
                        if text[i:i+4]=="ストップ" or text[lenText-4-i:lenText-i-1+1]=="ストップ":
                            print("ストップを検知しました。システムを終了します\n")
                            sys.exit()
                            #改良前のいち
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                continue
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                continue
            target = isolate_word(text)
            if target == "nothing":
                print("Could not request results")
                continue
            #テキスト音声ファイルでの実験時はリターンなしで全ファイルを試してみる
            return target

def move (target):
    #print(target)
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
      if name == target :
        global A
        A = float(ymax-ymin)
        exist = True
        center = int(xmax-xmin)/2+xmin
        if center<60:
            lcr=0
        elif 900<center:
            lcr=8
        else :
            lcr=(center-60)//120+1
        return exist
    print("見つからず、動いて次ループへ")
    time.sleep(5)
    drone.move_forward(x)    
    return exist
def analyDistance(pix,target):
    #print(f"A is {A},B is {B}")
    h=dictHigh[target]#メートル単位
    dis = h*fy/pix #h:dis=pix:fy
    dis = float(dis)
    print(f'pix is {pix}')
    print(f'distanse is {dis}\n')
    return dis
#システム本体
#drone接続
drone = tello.Tello('', 8889)
time.sleep(0.5)

#model の読み込み
model = torch.hub.load('ultralytics/yolov5','yolov5s')
time.sleep(0.5)
target="a"
#print(speech_reception())
#音声認識受付部分　

while True:
    try:
        target = speech_reception()
        print(f"target is {target}")
        break 

    except KeyboardInterrupt:
        print("\n-------input ~c------\n")
        del drone
        sys.exit()

drone.takeoff()
time.sleep(3)
#drone.move_up(0.5)
time.sleep(3)
pix=0

target = "bottle"
while True:
    try:
        #探索範囲を超えていないかを最初に確認
        print(f"moveX_cnt is {moveX_cnt}")
        if moveX_cnt*x>ROOMX:
         moveX_cnt=0
         moveY_cnt+=1
         if flag:
            time.sleep(5)
            drone.move_right(y)
            time.sleep(5)
         else:
            drone.move_left(y)
            time.sleep(5)
         drone.rotate_cw(180)
         time.sleep(5)
         flag ^=1
        if moveY_cnt*y > ROOMY:
           print("見つかりませんでした")
           drone.land()
           sys.exit()

        if move(target):
           print("とりあえず見つけた")
           break
    except KeyboardInterrupt:
        print("\n-------input ~c------\n")
        drone.land()
        del drone
        sys.exit()
time.sleep(3)
if lcr<4:
           lcr=(4-lcr)*10
           print(f"左側,{lcr}度にあります")
           drone.rotate_ccw(lcr)
           move(target)
elif 4<lcr:
           lcr=(lcr-4)*10
           print(f"右側,{lcr}度にあります")
           drone.rotate_cw(lcr)
           move(target)
if lcr ==4:
           print("中央にあります")
dis = analyDistance(A,target)
time.sleep(5)
drone.move_forward(dis)
stopT=int(dis*2)
time.sleep(stopT)
drone.land()

           
