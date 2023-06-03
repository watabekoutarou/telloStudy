# -*- coding: utf-8 -*-
#between_pcs.py
#ソケット通信によりPC!とPC2を接続
#こちら側がPC1,(cliant) 
import socket
M_SIZE = 65535
#pc2側のアドレス

pc2_address = ('127.0.0.1',8080)
#socket作成　ip6ならAF_INET6似
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    try:
        message = ("send message from mac")
        #  
        if message != 'end':
            #送る側
            #メッセージを送る部分
            #send_len = socket.sendto(message.encode(),pc2_address)
            socket.sendto(message.encode(),pc2_address)
            print("Wait response")
            rx_mes, addr = socket.recvfrom(M_SIZE)
            print(f"[Server]: {rx_mes.decode(encoding='utf-8')}")
            
        else:
            print('closing socket')
            socket.close()
            print('done')
            break

    except KeyboardInterrupt:
        print('closing socket')
        socket.close()
        print('done')
        break


