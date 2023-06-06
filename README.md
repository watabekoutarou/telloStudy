# telloStudy
## プログラム
### socket-pcs
https://qiita.com/note-tech/items/c3e1e497d231ea1e7ca7 を参考にしています
server側がデスクトップ、cliantをラップトップで想定してIPアドレスを書いています。
ルーティングはグローバルを除いてpowerpoint6/1分の場所に記載しているのでそれを参考に。

C:\Users\Mrkou>netstat -nao|find "8080"

C:\Users\Mrkou>netstat -nao|find "8080"
  UDP         0.0.0.0:8080           *:*                                    6684
  
 C:\Users\Mrkou>ping 192.168.11.7

192.168.11.7 に ping を送信しています 32 バイトのデータ:
192.168.11.7 からの応答: バイト数 =32 時間 =1ms TTL=64
192.168.11.7 からの応答: バイト数 =32 時間 =1ms TTL=64
192.168.11.7 からの応答: バイト数 =32 時間 =1ms TTL=64
192.168.11.7 からの応答: バイト数 =32 時間 =1ms TTL=64

192.168.11.7 の ping 統計:
    パケット数: 送信 = 4、受信 = 4、損失 = 0 (0% の損失)、
ラウンド トリップの概算時間 (ミリ秒):
    最小 = 1ms、最大 = 1ms、平均 = 1ms

###tello-python3

###　yoloで遊ぶ案
def square(xmin,xmax,ymin,ymax):
    return (xmax-xmin)*(ymax-ymin)
#obj に推論の結果の集合を代入
obj = result.pandas().xyxy[0]
#推論の結果のバウンディングボックスのクラスネームと座標を出力
dic = {}

for i in range(len(obj)):
    name = obj.nam[1]
    xmin = obj.xmin[1]
    ymin = obj.ymin[1]
    xmax = obj.xmax[1]
    ymax = obj.ymax[1]
    if name in dic:
        dic[name] += square(xmin,xmax,ymin,ymax)
    else:
        area = square
        dic.update(name = area)
maxArea = 0
flagKey = '' 
for key in dic.keys():
    if maxArea < dic[flagKey]:
        flagKey = key
        maxArea = dic[flagKey]

print(f"この画像のメインは{flagKey}で{maxArea}ピクセルあります")
