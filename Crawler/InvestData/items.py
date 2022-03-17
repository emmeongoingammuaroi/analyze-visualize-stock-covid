# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DailyStockItem(scrapy.Item):
    date = scrapy.Field()
    price = scrapy.Field()
    open_price = scrapy.Field()
    high = scrapy.Field()
    low = scrapy.Field()
    vol = scrapy.Field()
    change = scrapy.Field()
    currId = scrapy.Field()


class CompanyItem(scrapy.Item):
    name = scrapy.Field()
    short_name = scrapy.Field()
    avg_volume = scrapy.Field()
    market_cap = scrapy.Field()
    revenue = scrapy.Field()
    p_e_ratio = scrapy.Field()
    beta = scrapy.Field()
    currId = scrapy.Field()
    smlId = scrapy.Field()


class CompanyDetailItem(scrapy.Item):
    symbol = scrapy.Field()
    curr_id = scrapy.Field()
    industry = scrapy.Field()
    sector = scrapy.Field()
    employees = scrapy.Field()
    equity_type = scrapy.Field()
    isin = scrapy.Field()
    description = scrapy.Field()


class CountryItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    smlId = scrapy.Field()
