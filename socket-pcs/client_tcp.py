# -*- coding: utf-8 -*-
#client_tcp.py
#ソケット通信によりPC!とPC2を接続
#こちら側がPC1,(cliant) 
from PIL import Image
import socket
import io
import pickle

M_SIZE = 65535
#サーバ側のアドレス

server_address = ('192.168.11.6',8080)
#socket作成　ip6ならAF_INET6似
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(server_address)
print("サーバ接続:",server_address)
while True:
    try:
        # 画像の取得からリサイズ
        img = Image.open("1.jpg").resize((150, 150))
        img_io = io.BytesIO()
        img.save(img_io,format="JPEG")
        #オブジェクトの直列化
        img_bytes = pickle.dumps(img_io)
        #画像送る
        socket.send(img_bytes)
        print('done')
        """
        response = socket.recv(M_SIZE)
        print(f"[Server]: {response.decode(encoding='utf-8')}")
        """
        #socket.close()
        break
        #message = input("enter  message ")
 
    except KeyboardInterrupt:
        print('closing socket')
        socket.close()
        print('done')
        break

        
