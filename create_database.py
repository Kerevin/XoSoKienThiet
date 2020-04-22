# -*- coding: utf-8 -*-
#!/usr/bin/python
import sqlite3
import pandas as pd
def create_table(conn):

	conn.execute('''CREATE TABLE "VeXoSo" (
	"VeSo"	INTEGER NOT NULL,
	"ThanhPho"	TEXT NOT NULL,
	"LoaiGiai"	TEXT NOT NULL,
	"GiaiThuong"	TEXT);''')


reward = {"DacBiet": '2.000.000.000đ', 'Giai1':'30.000.000đ', 'Giai2':'15.000.000đ',
		'Giai3': '10.000.000đ', 'Giai4':'3.000.000đ', 'Giai5':'1.000.000đ', 'Giai6':'400.000đ',
		'Giai7': '200.000đ',  'Giai8': '100.000đ'}


df = pd.read_csv('xosokienthiet.csv', header=0, index_col = 0, encoding='utf8') 
conn = sqlite3.connect('test.db')
create_table(conn)
for thanh_pho, thuong in df.to_dict().items():
	for loai_giai, ve_so in thuong.items():
		conn.execute("INSERT INTO VeXoSo (VeSo,ThanhPho,LoaiGiai,GiaiThuong) \
      	VALUES (?, ?, ?, ?)", (ve_so, thanh_pho, loai_giai, reward[loai_giai])); 
conn.commit()
conn.close()