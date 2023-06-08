
#server_tcp.py
import socket
import time
from PIL import Image
import io
import pickle
import torch
import torch.cuda
#tcp通信のサーバ側で受け取った画像の物体検出を行う
#client側の画像のresizeを(600 480)にしないと検出できない
#pc2側(server)のプログラム
M_size = 65535
def square(xmin,xmax,ymin,ymax):
  return (xmax-xmin)*(ymax-ymin)

#pc1がわの情報
host = '192.168.11.6'
port = 8080
serverAddress = (host, port)

sock = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
print('create socket')

sock.bind(serverAddress)
sock.listen()


#model の読み込み
device = torch.device("cuda" if torch.cuda.is_available() else "cpu" )
model = torch.hub.load('ultralytics/yolov5','yolov5s')
model.to(device)
model.eval()
print("接続待機")
client_socket, client_address = sock.accept()

print("接続:",client_address)
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
      if name in dic:
        dic[name] += square(xmin,xmax,ymin,ymax)
      else:
        area = square(xmin,xmax,ymin,ymax)
        dic[name] = area
    maxArea = 0
    flagKey = ''
    for key in dic.keys():
      if maxArea < dic[key]:
        flagKey = key
        maxArea = dic[flagKey]
    print(f"この画像のメインは{flagKey}で{maxArea}ピクセルあります")
    response = flagKey.encode('utf-8')
    client_socket.send(response)
  except KeyboardInterrupt:
      print ('\n . . .\n')
      client_socket.close()
      sock.close()
      break
