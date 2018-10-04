# -*- coding: utf-8 -*-
import scrapy
import json
from itjuzi import items

class JuziSpider(scrapy.Spider):
    name = 'juzi'
    allowed_domains = ['www.itjuzi.com']
    start_urls = ['https://www.itjuzi.com/ai/index_ajax?type=1&page=1']

    def __init__(self):
        self.offset = 1
        super(JuziSpider,self).__init__()

    def parse(self, response):
        p_response = json.loads(response.body)
        h_response = p_response["recommend_com_info"]
        for temp in h_response:
            url_id = temp["com_id"]
            new_url = "https://www.itjuzi.com/company/"+str(url_id)
            yield scrapy.Request(new_url,callback=self.parse_new)
        self.offset +=1
        s_url = "https://www.itjuzi.com/ai/index_ajax?type=1&page="+str(self.offset)
        yield scrapy.Request(s_url,callback=self.parse)

    def parse_new(self,response):
        c_name = response.xpath('//span[@class="title"]/h1/@data-name').extract()[0].encode("utf-8")
        c_fullname = response.xpath('//span[@class="title"]/h1/@data-fullname').extract()[0].encode("utf-8")
        c_type = response.xpath('//div[@class="info-line"]/h2[@class="seo-slogan"]/text()').extract()[0].encode("utf-8")
        c_status = response.xpath('//div[@class="info-line"]/span/text()').extract()[0].encode("utf-8")
        c_link = response.xpath('//div[@class="link-line"]/a[last()]/text()').extract()[1].encode("utf-8")
        item = items.ItjuziItem()
        item['c_name'] = c_name
        item['c_fullname'] = c_fullname
        item['c_type'] = c_type
        item['c_status'] = c_status
        item['c_link'] = c_link
        return item
