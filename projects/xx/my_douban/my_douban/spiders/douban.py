# -*- coding: utf-8 -*-
import scrapy
from my_douban.items import MyDoubanItem

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    #page = 0

    start_urls = ["https://movie.douban.com/review/best"]

    def parse(self, response):
        page_links = response.xpath('//div[@class="paginator"]/a/@href')
        for link in page_links:
            #print link.extract()
            url = "http://movie.douban.com"+str(link.extract())
            yield scrapy.Request(url,callback=self.parse)

        content_links = response.xpath('//div[@class="review-list chart "]/div/div/a/@href')
        for link in content_links:
            #print link.extract()
            url = link.extract()
            #print url
            yield scrapy.Request(url,callback=self.parse_page)

    def parse_page(self,response):
        text_list = response.xpath('//div[@id="content"]')
        for text in text_list:
            name = text.xpath('./h1[1]/span[1]/text()').extract()
            #print name
            author = text.xpath('.//span[@class="attrs"]/a/text()').extract()
            #print author
            content = text.xpath('.//div[@id="link-report"]/span/text()').extract()
            #print content
            score = text.xpath('.//div[@class="rating_self clearfix"]/strong/text()').extract()
            print score
            item = MyDoubanItem()
            item['name'] = name
            item['author'] = author
            item['content'] = content
            item['score'] = score
            yield item



