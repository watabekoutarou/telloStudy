# -*- coding: utf-8 -*-
#between_pcs.py
#ソケット通信によりPC!とPC2を接続
#こちら側がPC1,(cliant) 
import socket
M_SIZE = 1024
#pc2側のアドレス
pc2_address = ('192.168.11.6',8890)
#socket作成　ip6ならAF_INET6似
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    try:
        message = ("send message")
        #
        if message != 'end':
            send_len = socket.sendto(message.encode('utf-8'),pc2_address)
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


