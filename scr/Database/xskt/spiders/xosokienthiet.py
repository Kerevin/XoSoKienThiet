# -*- coding: utf-8 -*-
import scrapy
import calendar
import datetime
import unicodedata
from scrapy.spiders import CrawlSpider
from ..items import XsktItem

class XoSoKienThietSpider(CrawlSpider):
	name = 'xosokienthiet'
	allowed_domains = ['https://xsmn.me']

	start_urls = []

	month_to_scrap = 5
	year_to_scrap = 2018
	

	start_urls= ["https://xsmn.me/xsmn-sxmn-kqxsmn-kqsxmn-ket-qua-xo-so-mien-nam.html"]
	
	def parse(self, response):
		xs_item = XsktItem()
		tmp_data = {}
		data_resp = scrapy.Selector(response)

		xs_item['xs_info'] =[
			# Ngày tháng năm của xổ số
			data_resp.xpath("//div[@class='title-bor clearfix']/h2[1]/text()").extract_first(),

		]
	
		for table_index in range(0, 5):
			# Bảng xổ số, mỗi bảng có 3 tỉnh
			for i in range(2, 5):
				# Các tỉnh trong bảng xổ số
				tmp_location = data_resp.xpath("//div[@id='load_kq_mn_{0}']//tr/th[{1}]/text()".format(table_index, i)).extract_first()
				#tmp_location = unicodedata.normalize('NFKD', tmp_location.replace("Đ", "D")).encode('ascii','ignore').decode().replace(" ","") # Chuyển từ có dấu sang không dấu
				tmp_data[tmp_location] = {}
				for j in range(2, 11):
					# Cột các giải từ giải 8 đến giải đặc biệt
					tmp_giai = data_resp.xpath("//div[@id='load_kq_mn_{0}']//tr[{1}]/td[1]/text()".format(table_index,j)).extract_first()
					tmp_giai = tmp_giai.replace("G","Giai").replace("ĐB", "DB") # Chuyển từ có dấu sang không dấu

					# Các số trúng thưởng trong cột theo tỉnh
					tmp_number = data_resp.xpath("//div[@id='load_kq_mn_{0}']//tr[{1}]/td[{2}]//text()".format(table_index,j, i)).extract()

					tmp_data[tmp_location][tmp_giai] = ",".join(tmp_number)

		xs_item['xs_data'] = tmp_data 

		yield xs_item 
