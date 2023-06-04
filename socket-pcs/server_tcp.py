#server_tcp.py
import socket
import time
from PIL import Image
import io
import pickle
#https://qiita.com/note-tech/items/c3e1e497d231ea1e7ca7 引用
#pc2側(server)のプログラム
M_size = 65535

#pc1がわの情報
host = '192.168.11.6'
port = 8080
serverAddress = (host, port)

sock = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
print('create socket')

sock.bind(serverAddress)
sock.listen()
print("接続待機")


while True:
    client_socket, client_address = sock.accept()
    message = client_socket.recv(M_size)
    print("接続:",client_address)

    #復元
    data = pickle.loads(message)
    #Bytesloから
    content = data.getvalue()
    #画像を保存
    img = Image.open(io.BytesIO(content))
    # img = img.resize((600, 600))
    img.save("test.jpg")
    img.show()
    #sock.close()
    """
    try :
        # ③Clientからのmessageの受付開始
        print('Waiting message')

        message = sock.recv(M_size)
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
        """
        #sock.sendto('Success to receive message'.encode(encoding='utf-8'), cli_addr)
        #response = "サーバからの返答"
        #client_socket.send(response.encode())
        #print ('\n . . .\n')
    """

        sock.close()
        break
    except KeyboardInterrupt:
        print ('\n . . .\n')
        sock.close()
        break
"""
