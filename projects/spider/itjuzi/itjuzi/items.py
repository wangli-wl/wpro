# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ItjuziItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    c_name =  scrapy.Field()
    c_fullname =  scrapy.Field()
    c_type = scrapy.Field()
    c_status =  scrapy.Field()
    #c_intro =  scrapy.Field()
    c_link =  scrapy.Field()