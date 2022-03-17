import scrapy
import json
from InvestData.items import DailyStockItem
from InvestData.settings import ROOT_FOLDER
from datetime import datetime, timedelta
import csv
import logging
import time

class StockSpider(scrapy.Spider):
    name = 'stock'
    allowed_domains = ['investing.com']
    start_url = 'https://www.investing.com/instruments/HistoricalDataAjax'
    fieldnames = [
        'date',
        'price',
        'open_price',
        'high',
        'low',
        'vol',
        'change',
        'currId',
    ]
    file_name = 'stocks'

    body = {
        'curr_id': '',
        'st_date': '',
        'end_date': '',
        'header': "Historical Data",
        'interval_sec': 'Daily',
        'sort_col': 'date',
        'sort_ord': 'DESC',
        'action': 'historical_data',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    def feed(self):
        # Open country list and parse one by one
        with open(ROOT_FOLDER + "companies.csv", 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                logging.info(f">>>>> Getting data for {row['short_name']}, currId: {row['currId']}")
                yield row['currId']

    def start_requests(self):
        for currId in self.feed():
            body = self.body.copy()

            today = datetime.today()
            ago = today - timedelta(days=1)
            body.update({
                'curr_id': currId,
                'st_date': ago.strftime("%m/%d/%Y"),
                'end_date': today.strftime("%m/%d/%Y")
            })
            yield scrapy.FormRequest(url=self.start_url, callback=self.parse, headers=self.headers, formdata=body,
                                        cb_kwargs={'currId': currId, 'st_date': ago})

    def parse(self, response, currId, st_date):
        rows = response.xpath("//table[@id='curr_table']/tbody/tr")
        for data in rows:
            if 'No results' in data.extract():
                break
            item = {}
            item['date'] = data.xpath('./td[1]').attrib['data-real-value']
            item['price'] = data.xpath('./td[2]').attrib['data-real-value']
            item['open_price'] = data.xpath(
                './td[3]').attrib['data-real-value']
            item['high'] = data.xpath('./td[4]').attrib['data-real-value']
            item['low'] = data.xpath('./td[5]').attrib['data-real-value']
            item['vol'] = data.xpath('./td[6]').attrib['data-real-value']
            item['change'] = data.xpath('./td[7]/text()').get()
            item['currId'] = currId
            yield item
