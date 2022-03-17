# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
from .settings import ROOT_FOLDER
import csv

class DataPipeline:
    file_name = 'stocks.csv'
   
    def open_spider(self, spider):
        now = datetime.now().strftime('%Y%m%d %H%M%S')
        file_name = f"{ROOT_FOLDER}{spider.file_name}-{now}.csv"
        self.file = open(file_name, 'a')
        self.writer = csv.DictWriter(self.file, fieldnames=spider.fieldnames)
        self.writer.writeheader()

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.writer.writerow(ItemAdapter(item).asdict())
        return item

