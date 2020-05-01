import os
try:
	import scrapy
except Exception as e:
	pass
import datetime
import time


def crawling():
	
	if "Database\\xskt" not in os.getcwd():
		os.chdir("Database/xskt")
	
	f = open("log.txt", "r")
	# Kiểm tra xem lần cuối cập nhật database có phải là ngày hôm nay và qua 5h không?
	# Nếu không sẽ cập nhật
	current_time = list(time.localtime())
	if current_time[3] < 17:
		current_time[2] -= 1
	if not( list(time.strptime(f.readline(), '%d-%m-%Y'))[0:3] == current_time[0:3]):
		print("Updating database")
		if os.path.exists("xs_database.db"):
			os.remove("xs_database.db")
		os.system("start cmd /c scrapy crawl xosokienthiet")

	else:	
		print("Your data is up-to-date")
		

if __name__ == '__main__':
	f = open("log.txt", "r")
	log_time = list(time.strptime(f.readline(), '%d-%m-%Y'))
	current_time = list(time.localtime())
	print(log_time)
	print(current_time)

	#crawling()

	



