import scrapy
import json
from InvestData.items import CompanyItem
from InvestData.settings import LOG_COUNTRY, ROOT_FOLDER
import urllib.parse


class CompanySpider(scrapy.Spider):
    name = 'company'
    allowed_domains = ['investing.com']
    fieldnames = [
        'name',
        'currId',
        'short_name',
        'avg_volume',
        'market_cap',
        'revenue',
        'p_e_ratio',
        'beta',
        'smlId',
    ]
    url = 'https://www.investing.com/equities/StocksFilter?'

    def feed(self):
        # Open country list and parse one by one
        with open(ROOT_FOLDER + "countries.csv", 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield row['smlId']

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        params = {
            'noconstruct': '1',
            'smlID': None,
            'tabletype': 'fundamental',
            'index_id': 'all',
            'sid': "",
        }

        for smlId in self.feed():
            params['smlID'] = smlId[0]
            params_str = urllib.parse.urlencode(params)
            
            yield scrapy.Request(url=self.url + params_str, callback=self.parse, headers=headers, cb_kwargs={'smlId': smlId})

    def parse(self, response, smlId):
        item = CompanyItem()
        for data in response.xpath("//table[@id='fundamental']/tbody/tr"):
            item['name'] = data.xpath('./td[2]/span').attrib['data-name']
            item['currId'] = data.xpath('./td[2]/span').attrib['data-id']
            item['short_name'] = data.xpath('./td[2]/a/text()').get()
            item['avg_volume'] = data.xpath('./td[3]/text()').get()
            item['market_cap'] = data.xpath('./td[4]/text()').get()
            item['revenue'] = data.xpath('./td[5]/text()').get()
            item['p_e_ratio'] = data.xpath('./td[6]/text()').get()
            item['beta'] = data.xpath('./td[7]/text()').get()
            item['smlId'] = smlId

            yield item
