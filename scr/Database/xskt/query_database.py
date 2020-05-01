import sqlite3
import os
import unicodedata
import sqlite3



reward = {"DB": '2.000.000.000đ', 'Giai1':'30.000.000đ', 'Giai2':'15.000.000đ',
        'Giai3': '10.000.000đ', 'Giai4':'3.000.000đ', 'Giai5':'1.000.000đ', 'Giai6':'400.000đ',
        'Giai7': '200.000đ',  'Giai8': '100.000đ'}
def convert_string_to_dict(cursor):

	ve_so_dict = eval(list(cursor)[0][0])


	for giai_thuong, ve_so in ve_so_dict.items():	
		ve_so_dict[giai_thuong] = [num for num in ve_so.split(",") if len(num) > 0]
	return ve_so_dict

def get_data_from_db(inp):
	conn = sqlite3.connect('./Database/xskt/xs_database.db')

	city_names = tuple((conn.execute("SELECT distinct(thanh_pho) from kq_xs")))
	normalized_name = [unicodedata.normalize('NFKD', name[0].replace("Đ", "D")).encode('ascii','ignore').decode().replace(" ","")  for name in city_names]	

	name = ""
	for i in range(len(normalized_name)):
		#print(city_names)
		if inp[0] == normalized_name[i]:
			name = city_names[i][0]

	cursor = conn.execute("SELECT ve_so from kq_xs where thanh_pho = '"+ name+ "' ")
	
	return cursor



def input_is_valid(inp):
	
	conn = sqlite3.connect('./Database/xskt/xs_database.db')
	city_names = conn.execute("SELECT distinct(thanh_pho) from kq_xs")
	city_names = [unicodedata.normalize('NFKD', name[0].replace("Đ", "D")).encode('ascii','ignore').decode().replace(" ","")  for name in city_names]	
	conn.close()
	if inp[0] in city_names:
		return True
	return False

def get_cities():

	conn = sqlite3.connect('./Database/xskt/xs_database.db')
	city_names = conn.execute("SELECT distinct(thanh_pho) from kq_xs")
	city_names = [name[0] for name in city_names]
	return city_names 

def get_result(inp):
	global reward
	inp = inp.split()

	# Gửi tên các thành phố chỉ cách truy vấn
	if inp[0]=="h":
		return get_cities()
	if (not input_is_valid(inp)):		
		return 0

	# Nếu gửi theo cú pháp <Tỉnh thành> <Vé Số>
	if (len(inp) == 2):
		if not("0" <= inp[1] <="9"):
			return 0
		data_ve_so = convert_string_to_dict(get_data_from_db(inp))
		is_win_lottery = ()
		for giai_thuong, ve_so in data_ve_so.items():
			for num in ve_so:
				if num in inp[1]:
					is_win_lottery = (giai_thuong, reward[giai_thuong])
		if len(is_win_lottery) > 0:
			return 	["Chúc mừng bạn đã trúng %s trị giá %s" % (is_win_lottery[0], is_win_lottery[1])]
		return ["Xin lỗi, bạn không trúng giải nào cả!"]
	
	# Nếu gửi theo cú pháp <Tỉnh thành>
	elif (len(inp) == 1):
		cursor = convert_string_to_dict(get_data_from_db(inp))
		#cursor = list(get_data_from_db(inp))
		return cursor



if __name__ == '__main__':

	
	print((get_result("H")))
	input("Press any key to stop")

