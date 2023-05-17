import socket
import time
import cv2
import threading


#接続部
#telloへのアクセス

tello_address = ('192.168.10.1', 8889)
#telloからの受信
UDP_IP='0.0.0.0'
UDP_PORT=11111

cap=None
response=None

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sent = sock.sendto(b'stream',tello_address)
udp_video_adress='udp://@'+UDP_IP+':'+str(UDP_PORT)
if cap is None:
    cap=cv2.VideoCapture(udp_video_adress)
if not cap is None:
    cap.open(udp_video_adress)

sent = sock.sendto(b'takeoff',tello_address)
time.sleep(5)

if cv2.waitKey(1) & 0xff == ord('q'):
    sent = sock.sendto(b'land',tello_address)
        

sent=sock.sendto(b'streamoff',tello_address)

""""
socket.sendto('command'.encode('utf-8'),tello_address)#コマンドモードに移行
time.sleep(3)
socket.sendto('takeoff'.encode('utf-8'),tello_address)#離陸
time.sleep(3)
socket.sendto('land'.encode('utf-8'),tello_address)#着陸
"""