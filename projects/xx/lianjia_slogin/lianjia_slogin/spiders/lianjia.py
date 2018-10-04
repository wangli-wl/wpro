# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Spider,Rule
from lianjia_slogin.items import LianjiaSloginItem
import re
from bs4 import BeautifulSoup as bs

class LianjiaSpider(Spider):
    name = 'lianjia'
    allowed_domains = ['bj.lianjia.com']
    start_urls = ['https://bj.lianjia.com/chengjiao/']

    def parse(self, response):
        for page in range(1,100):
            url = "https://bj.lianjia.com/chengjiao/pg"+str(page)+"/"
            yield scrapy.Request(url,callback=self.parse_sold_link)

    def parse_sold_link(self, response):
        sold_links = re.findall(r"https://bj.lianjia.com/chengjiao/\d+\.html",response.text)
        for link in sold_links:
            yield scrapy.Request(link,callback=self.parse_content)

    def parse_content(self,response):
        soup = bs(response.text,'lxml')
        house_attr = soup.find_all("div",{"class":"wrapper"})[0].get_text().encode("utf-8").split("米")[0]+"米"
        deal_info = soup.find_all("p",{"class":"record_detail"})[0].get_text().encode("utf-8").split(",")
        deal_unitprice = deal_info[0]
        deal_time_location = deal_info[2]+deal_info[1]
        deal_totalprice = soup.find_all("span",{"class":"dealTotalPrice"})[0].get_text().encode("utf-8")
        deal_num = response.xpath('/html/body/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/ul/li[1]/text()').extract()[0].encode("utf-8").strip()
        house_time = response.xpath('/html/body/section[2]/div[1]/div[1]/div[1]/div[1]/div[2]/ul/li[8]/text()').extract()[0].encode("utf-8")
        house_structure = response.xpath('/html/body/section[2]/div[1]/div[1]/div[1]/div[1]/div[2]/ul/li[10]/text()').extract()[0].encode("utf-8")
        house_floor = response.xpath('/html/body/section[2]/div[1]/div[1]/div[1]/div[1]/div[2]/ul/li[2]/text()').extract()[0].encode("utf-8")
        house_layout = response.xpath("/html/body/section[2]/div[1]/div[1]/div[1]/div[1]/div[2]/ul/li[1]/text()").extract()[0].encode("utf-8")
        house_info = house_time.strip()+"年建成,"+house_layout.strip()+","+","+house_structure.strip()+house_floor.strip()
        deal_guatime = response.xpath("/html/body/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/ul/li[3]/text()").extract()[0].encode("utf-8")
        deal_own = response.xpath("/html/body/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/ul/li[2]/text()").extract()[0].encode("utf-8")
        deal_house = response.xpath("/html/body/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/ul/li[4]/text()").extract()[0].encode("utf-8")
        deal_attr = deal_guatime.strip()+"日挂牌,"+deal_own.strip()+","+deal_house.strip()+","+deal_time_location

        item = LianjiaSloginItem()
        item['deal_num'] = deal_num
        item['house_attr'] = house_attr
        item['price'] = "单价："+deal_unitprice.strip().split("单价")[1]+"  "+"总价："+deal_totalprice.strip()
        item['deal_attr'] =deal_attr
        item['house_info'] = house_info
        return item











