import os	
import scrapy
if os.path.exists("xs_database.db"):
	os.remove("xs_database.db")

os.system("cmd /k scrapy crawl xosokienthiet")
