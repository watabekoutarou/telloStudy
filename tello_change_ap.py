import socket
from time import sleep
import curses
#telloをwifi子機にさせる
wifi_ssid = input("Enter the SSID:")
print()
wifi_pass = input("Enter the pass:")

tello_ip = '192.168.10.1'
tello_port = 8889
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = (tello_ip , tello_port)
socket.sendto('command'.encode('utf-8'),tello_address)
wifi_config = "ap "+ wifi_ssid + " " +wifi_pass
socket.sendto("ap Buffalo-8660 5pbr4figxp3".encode('utf-8'),tello_address)