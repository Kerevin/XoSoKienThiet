#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tkinter import *
from threading import Thread
import socket
import os, sys


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"
port = 8080
class Interface(Tk):
	def __init__(self):
		super().__init__()
		self.title("Customer")
		self.width = 700
		self.height = 800
		self.canvas = Canvas(self, width = self.width, height = self.height)
		self.canvas.pack()

		self.create_input_frame()
		self.create_output_frame()

		self.input_field.bind("<Return>", (lambda event: self.get_data_from_input()))
		
		self.protocol("WM_DELETE_WINDOW", self.on_closing)

	def create_input_frame(self):
		# Hàm tạo một box riêng dành cho client để nhập
		
		# Bộ khung ngoài cho phần input 
		input_frame = LabelFrame(self.canvas, text="Customer: ", borderwidth=4)
		input_frame.place(x=10, y=self.height-100, width = self.width - 10, height = 70)

		# Box để nhập input 
		self.input_field = Entry(input_frame, text=StringVar(), font = ("Times New Roman", 16))
		self.input_field.pack(fill = BOTH)
		self.input_field.focus_set()	# Khi mở app lên thì con trỏ tự động nhảy vào ô input

	def create_output_frame(self):		
		# Hàm tạo một box riêng dành cho output -kết quả
		
		# Bộ khung ngoài cho phần output
		output_frame = LabelFrame(self.canvas, text="Screen", borderwidth=2)
		output_frame.place(x=10, y=20, width=self.width-18, height=600)

		# Tạo vùng text để hiện các output 
		self.text_field = Text(output_frame,state='disabled', font = ("Times New Roman", 16))
		self.text_field.pack()
		self.text_field.tag_configure("right", justify='right')
		self.text_field.tag_configure("left", justify="left")

		# Tạo cái scroll lăn lên xuống cho phần output 
		scroll = Scrollbar(orient= "vertical", command = self.text_field.yview)
		scroll.place(x=self.width - 10, y=25, width = 10, height=600)
		self.text_field.configure(yscrollcommand=scroll.set)

	def put_string_to_text_field(self, input_get, side):
		# Put string to text_field 
		self.text_field.configure(state='normal')
		self.text_field.insert('end', input_get + "\n", side)
			
		self.text_field.see('end')
		self.text_field.configure(state='disabled')

		self.input_field.delete(0, END)

	def get_data_from_input(self):
		# Nhận data từ client ở input_field

		# Get string from Entry
		input_get = self.input_field.get()
		if input_get == "":
			return
		# Put string to text_field 
		self.put_string_to_text_field(input_get, "right")

		self.input_field.delete(0, END)
		s.sendall(input_get.encode())

	def receive_data(self):
		while 1:
			try:
				incoming_message = s.recv(1024).decode("utf-8")
				self.put_string_to_text_field(incoming_message, "left")		
				
			except OSError:
				break
				

	def on_closing(self):
		try:
			s.close()
			self.quit()
			sys.exit()
		except:
			pass
if __name__ == '__main__':	
	try:
		print("Connecting to host...")
		s.connect((host, port))
		print("Connected!")
	except:
		print("Error from trying to connect to host...")
		print("About to exit!")
		sys.exit()
	gui = Interface()
	t1 = Thread(target = gui.receive_data)
	t1.start()
	gui.mainloop()

	t1.join()
	sys.exit()
	
