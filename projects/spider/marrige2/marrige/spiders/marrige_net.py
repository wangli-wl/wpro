# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisSpider
from scrapy.spiders import Rule
from marrige.items import MarrigeItem
from scrapy.dupefilters import RFPDupeFilter

class MarrigeNetSpider(RedisSpider):
    name = 'marrige_net'
    #allowed_domains = ['hongniang.com']
    #url = "http://www.hongniang.com/index/search?sort=0&wh=0&sex=2&starage=0&province=0&city=0&marriage=0&edu=0&income=0&height=0&pro=0&house=0&child=0&xz=0&sx=0&mz=0&hometownprovince=0&page="
    #page = 1
    #start_urls = [url+str(page)]
    #print start_urls

    redis_key = "marrige_net:start_urls"
    profile_links = LinkExtractor(allow=r'/user/member/id/\d+')
    rules = (
        Rule(profile_links,callback='parse', follow=True),
    )

    def parse(self, response):
        #i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        #return i
        #print response.url
        text_lists = response.xpath('//div[@class="sub1"]')
        #print text_list.extract()[0].encode("utf-8")
        for text in text_lists:
            id = text.xpath('.//div[@class="name nickname"]/text()').extract()[0].strip()
            #age = text.xpath('./').extract()
            #height = text_list.xpath('')
            #education =
            #occupation =
            thought = text.xpath('.//div[@class="text"]/text()').extract()[0].strip()
            #print id
            #print thought
            item = MarrigeItem()
            item['id'] = id
            item['thought'] = thought
            yield item

