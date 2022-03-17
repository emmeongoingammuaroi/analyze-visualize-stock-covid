import scrapy
from InvestData.items import CountryItem

class CountrySpider(scrapy.Spider):
    name = 'country'
    allowed_domains = ['investing.com']
    start_url = 'https://www.investing.com/equities/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
    }
    file_name = 'country'

    def start_requests(self):
        yield scrapy.Request(self.start_url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        for data in response.xpath("//ul[@class='countrySelect']/li/a"):
            name = data.xpath('./text()').get()
            url = 'https://www.investing.com' + data.attrib['href']
            req = scrapy.Request(
                url, callback=self.parse2, headers=self.headers)
            req.cb_kwargs['name'] = name
            req.cb_kwargs['url'] = url
            yield req

    def parse2(self, response, name, url):
        item = CountryItem()
        smlId = response.xpath("//input[@id='smlID']/@value").get()
        item['name'] = name
        item['url'] = url
        item['smlId'] = smlId
        print(item)
        yield item
