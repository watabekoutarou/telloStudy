#between_pcs2.py
import socket
import time
from PIL import Image
import io
import pickle
#https://qiita.com/note-tech/items/c3e1e497d231ea1e7ca7 引用
#pc2側(server)のプログラム
M_size = 65535

#pc1がわの情報
host = ''
port = 8080
pc1Adrres = (host, port)

sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
print('create socket')

sock.bind(pc1Adrres)

while True:
    try :
        # ③Clientからのmessageの受付開始
        print('Waiting message')
        #~ここまでできている
        message, cli_addr = sock.recvfrom(M_size)
        #復元
        data = pickle.loads(message)
        #Bytesloから
        content = data.getvalue()
        #画像を保存
        img = Image.open(io.BytesIO(content))
        # img = img.resize((600, 600))
        img.save("test.jpg")
        img.show()

        #message = message.decode(encoding='utf-8')
        #print(f'Received message is [{message}]')

        # Clientが受信待ちになるまで待つため
        time.sleep(1)

        # ④Clientへ受信完了messageを送信
        print('Send response to Client')
        sock.sendto('Success to receive message'.encode(encoding='utf-8'), cli_addr)
        print ('\n . . .\n')
        sock.close()
        break
    except KeyboardInterrupt:
        print ('\n . . .\n')
        sock.close()
        break
