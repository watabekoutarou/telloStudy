#client_Img_dis.py
#ソケット通信によりPC!とPC2を接続
#こちら側がPC1,(cliant) 
#100mm前した画像とその前の画像2枚で距離を推定するclient側のコード
from PIL import Image
import socket
import io
import pickle
import time
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
        img = Image.open("disTestImg/120.jpg").resize((640, 480))
        img_io = io.BytesIO()
        img.save(img_io,format="JPEG")
        #オブジェクトの直列化
        img_bytes = pickle.dumps(img_io)
        #画像送る
        socket.send(img_bytes)

        print('120 done')
        time.sleep(5)

        img = Image.open("disTestImg/110.jpg").resize((640, 480))
        img_io = io.BytesIO()
        img.save(img_io,format="JPEG")
        #オブジェクトの直列化
        img_bytes = pickle.dumps(img_io)

        #画像送るX
        socket.send(img_bytes)

        print("110 done")

        response = socket.recv(M_SIZE)
        print(f"distance1: {response.decode(encoding='utf-8')}")
        socket.close()
        break
        
 
    except KeyboardInterrupt:
        print('closing socket')
        socket.close()
        print('done')
        break
