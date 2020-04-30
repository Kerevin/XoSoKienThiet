# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from sqlite3 import dbapi2 as sqlite 

"""
Lưu dữ liệu crawl được vào Database
"""
class XsktPipeline:
    def __init__(self):
        self.connection = sqlite.connect('./xs_database.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS kq_xs '
                            '(thanh_pho TEXT, ve_so TEXT)')

    def process_item(self, item, spider):
        ""
        # item là một dictionary có 2 phần tử
        # item['xs_info']: Ngày xổ
        # item['xs_data']: dictionary về thông tin xổ số gồm:
        # keys là tỉnh thành
        # values là dictionay lưu trữ giải và vé số  {"Giải" : Số}
        f = open("log.txt", "w")
        f.write(str(item['xs_info'][0].split()[-1]))

        self.cursor.execute("select * from kq_xs")
        
        result = self.cursor.fetchone()
        if not result:
            for tinh_thanh, xoso in item['xs_data'].items():
                for giai, ve_so in xoso.items():
                    splitted_ve_so = ve_so.split(",")
                    splitted_ve_so = [so +"," for so in splitted_ve_so if len(so) > 1]
                    xoso[giai] = "".join(splitted_ve_so)
                self.cursor.execute(
                    "insert into kq_xs (thanh_pho, ve_so) values (?, ?)",
                    (tinh_thanh, str(xoso)))

            self.connection.commit()
       
        return item