# -*- coding: utf-8 -*-
#!/usr/bin/python
import sqlite3
from threading import Thread
import socket
import time
import os
import Database.xskt.query_database as database

import Database.xskt.crawling_data as cr
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
	client.send(bytes("Các tên tỉnh thành đều phải viết liền, không dấu và viết hoa mỗi từ.", "utf-8"))
	client.send(bytes("Truy vấn thứ nhất: <Tên tỉnh thành> \n 	Ví dụ: LongAn \n", "utf-8"))
	client.send(bytes("Truy vấn thứ hai: <Tên tỉnh thành>  <Vé số> \n 	Ví dụ: LongAn 1234\n", "utf-8"))
	client.send(bytes("Các tỉnh thành hiện mở: " ,"utf-8"))
	client.send(bytes(cities[0], "utf-8"))
	for i in range(1, len(cities)):
		client.send(bytes(", " + str(cities[i]), "utf-8"))

def handle_client(client):# Takes client socket as argument.
	"""Handles a single client connection."""	
	
	while True:
		try:
			client_msg = client.recv(1024).decode("utf-8")

			result = database.get_result(client_msg)
			if result == 0: 
				client.send(bytes("Không có dữ liệu, xin mời nhập lại theo đúng cú pháp! Gõ 'h' để xem cách truy vấn", "utf-8"))
			else:
				if len(result)  == 1:
					# Dò theo truy vấn <tỉnh thành> <vé số>
					client.send(bytes(result[0], "utf-8"))
				elif client_msg == "h":
					# Gửi yêu cầu hướng dẫn truy vấn
					send_help(client, result)
				else:
					# Truy vấn <tỉnh thành> 
					client.send(bytes("Kết quả xổ số %s" % client_msg, "utf-8"))
					for giai, ve_so in result.items():
						client.send(bytes("%s: %s\n" % (giai,", ".join((ve_so))),"utf-8"))

							
			
		except OSError as e:
			print("%s:%s has left." % addresses[client])
			
			client.close()
			break;
	


if __name__ == '__main__':
	current_dir = os.getcwd()
	try:
		cr_thread = Thread(target = cr.crawling())
		cr_thread.start()
		cr_thread.join()
	except Exception as e:
		print("Error when trying to update database")
	server.listen(5)
	os.chdir(current_dir)

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



	
