#main3.py
#droneの画像から"bottle"が最も近い場所を一つ過ぎたら止まる
#ただし、ドローン自体は人間が動かす
import tello
from PIL import Image
from PIL import ImageTk
import threading
import datetime
import cv2
import os
import time
import platform
import socket
import io
import pickle
M_SIZE = 65535
#サーバ側のアドレス
server_address = ('192.168.11.6',8080)
#socket作成ip6ならAF_INET6似
socketWin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketWin.connect(server_address)
drone = tello.Tello('', 8889)
time.sleep(0.5)
tmp = 0
while True:
    time.sleep(0.5)
    frame = drone.read()
    if frame is None or frame.size == 0:
        print("frame is nothing")
        continue
    image = Image.fromarray(frame)
    image_re = image.resize((640,480))
    img_io = io.BytesIO()
    image_re.save(img_io,format="JPEG")
    img_bytes = pickle.dumps(img_io)
    socketWin.send(img_bytes)
    print('done')
    response = socketWin.recv(M_SIZE)
    if response is None:
        break
    res = response.decode(encoding='utf-8')
    print(f"[Server]: {res}")
    if res == "bottle" :
        print("It's bottle!")
        area = socketWin.recv(M_SIZE)
        """
        if area is None:
            while True:
                area = socketWin.recv(M_SIZE)
                if area is None:
                    continue
                else:
                    break
        """
        areaNum = int.from_bytes(area, 'big')
        #areaNum = int.from_bytes(area,'little')
        area = area.decode(encoding='utf-8')
        
        print(area)
        if areaNum > tmp:
            tmp = areaNum
        else:
            print("One previous is the nearest location")
            socketWin.close()
            break
    else:
        continue
