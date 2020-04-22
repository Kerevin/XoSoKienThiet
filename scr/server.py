# -*- coding: utf-8 -*-
#!/usr/bin/python
import sqlite3
from threading import Thread
import socket
import time
import xu_ly_yeu_cau

host = "localhost"
port = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))


clients = {}
addresses = {}
def accept_incoming_connections():
	"""Sets up handling for incoming clients."""
	while True:
		client, client_address = server.accept()
		print("%s:%s has connected." % client_address)
		client.send(bytes("Chào mừng đến với xổ số kiến thiết! Gửi 'h' để được hướng dẫn", "utf8"))
		addresses[client] = client_address
		Thread(target=handle_client, args=(client,)).start()


def send_help(client, cities):
	client.send(bytes("Truy vấn thứ nhất: <Tên tỉnh thành> \n 	Ví dụ: LongAn", "utf-8"))
	client.send(bytes("Truy vấn thứ hai: <Tên tỉnh thành>  <Vé số> \n 	Ví dụ: LongAn 12\n", "utf-8"))
	client.send(bytes("Các tỉnh thành hiện mở: " ,"utf-8"))
	client.send(bytes(cities[0], "utf-8"))
	for i in range(1, len(cities)):
		client.send(bytes(", " + str(cities[i]), "utf-8"))

def handle_client(client):# Takes client socket as argument.
	"""Handles a single client connection."""	
	
	while True:
		try:
			client_msg = client.recv(1024).decode("utf-8")

			result = xu_ly_yeu_cau.get_result(client_msg)
			if result == 0: 
				client.send(bytes("Không có dữ liệu, xin mời nhập lại", "utf-8"))
			else:
				if len(result)  == 1:
					client.send(bytes(result[0], "utf-8"))
				elif len(result) == 7:
					send_help(client, result)
				else:
					client.send(bytes("Kết quả xổ số %s" % client_msg, "utf-8"))
					for row in result:
						client.send(bytes("%s: %s \n" % (row[2], row[0]), "utf-8"))
			
		except OSError as e:
			print("%s:%s has left." % addresses[client])
			
			client.close()
			break;
			
if __name__ == '__main__':

	server.listen(3)

	print("Waiting for connection...")
	try:
		ACCEPT_THREAD = Thread(target=accept_incoming_connections)
		ACCEPT_THREAD.start()
		ACCEPT_THREAD.join()
	except:
		server.close()
		
		sys.exit()

	server.close()
	sys.exit()
	
