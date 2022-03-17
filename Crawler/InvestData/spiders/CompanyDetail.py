import scrapy
from InvestData.items import CompanyDetailItem, DailyStockItem
from InvestData.settings import LOG_COMPANY, ROOT_FOLDER
from datetime import datetime, timedelta
import csv
import logging
import time
import re
import urllib

class CompanydetailSpider(scrapy.Spider):
    name = 'CompanyDetail'
    allowed_domains = ['investing.com']
    url = 'https://www.investing.com/equities/StocksFilter?'
    file_name = "company_detail"
    fieldnames = [
        'symbol',
        'curr_id',
        'industry',
        'sector',
        'employees',
        'equity_type',
        'isin',
        "description"
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }


    def feed(self):
        # Open country list and parse one by one
        with open(ROOT_FOLDER + "countries.csv", 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield row['smlId']


    def start_requests(self):
        params = {
            'noconstruct': '1',
            'smlID': None,
            'tabletype': 'fundamental',
            'index_id': 'all',
            'sid': "",
        }

        for smlId in self.feed():
            params['smlID'] = smlId
            params_str = urllib.parse.urlencode(params)
            
            yield scrapy.Request(url=self.url + params_str, callback=self.parse, headers=self.headers, cb_kwargs={'smlId': smlId})

    def parse(self, response, smlId):
        for data in response.xpath("//table[@id='fundamental']/tbody/tr"):
            url = data.xpath('./td[2]/a').attrib['href'] + "-company-profile"
            curr_id = data.xpath('./td[2]/span').attrib['data-id']
            yield response.follow(url, callback=self.parse_detail, headers=self.headers, cb_kwargs={'curr_id': curr_id})

    def parse_detail(self, response, curr_id):
        item = CompanyDetailItem()
        try:
            title = response.xpath('//div[@class="instrumentHead"]/h1/text()').get().strip()
        except:
            title = response.xpath('//h1[contains(@class, "instrument-header_title")]/text()').get().strip()

        logging.info("Processing: " + title)
        try:
            item['symbol'] = re.match(r".*\((.*)\)$", title).group(1)
            item['curr_id'] = curr_id
            item['industry'] = response.xpath('//div[@class="companyProfileHeader"]/div[1]/a/text()').get().strip()
            item['sector'] = response.xpath('//div[@class="companyProfileHeader"]/div[2]/a/text()').get().strip()
            item['employees'] = response.xpath('//div[@class="companyProfileHeader"]/div[3]/p/text()').get().strip()
            item['equity_type'] = response.xpath('//div[@class="companyProfileHeader"]/div[4]/p/text()').get().strip()
            item['isin'] = response.xpath('//div[@id="quotes_summary_current_data"]/div[2]/div[3]/span[2]/text()').get().strip()
            description = response.xpath('//p[contains(@id, "profile-fullStory")]//text()').get()
            item['description'] = description.strip() if description is not None else ""
        except:
            logging.warning("Company doesn't have profile page.")
        finally:
            yield item
            time.sleep(2)