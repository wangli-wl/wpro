#coding=utf-8

import requests
from lxml import etree
from MySQLdb import *
import time
import re
import json

class Crawlmovie(object):
    def __init__(self):
        self.url = "http://www.mtime.com/top/movie/top100/"
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"
        }
        self.page = 1
        self.offset = 0

    def get_response(self,url):
        sess = requests.session()
        response = sess.get(url, headers=self.header)
        html = response.text
        e_html = etree.HTML(html)
        return e_html,response

    def crawl_page(self):
        while self.page<=10:
            e_html,response = self.get_response(self.url)
            content_urls = e_html.xpath('//h2[@class="px14 pb6"]/a/@href')
            for url in content_urls:
                self.parse_content(url)
            self.page += 1
            self.url = "http://www.mtime.com/top/movie/top100/index-"+str(self.page)+".html"

    def parse_content(self,url):
        e_html,response = self.get_response(url)
        name = e_html.xpath('//div[@class="clearfix"]/h1/text()|//p[@class="db_enname"]/text()')[0].encode("utf-8")
        author = e_html.xpath('//dl[@class="info_l"]/dd[1]/a/text()')[0].encode("utf-8")
        pub_year = e_html.xpath('//div[@class="clearfix"]/p/a/text()')[0].encode("utf-8")
        content = e_html.xpath('//p[@class="mt6 lh18"]/text()')[0].encode("utf-8")
        score,attitude_count = self.ajax_content(url)
        self.save_mysql(name,author,pub_year,content,score,attitude_count)

    def ajax_content(self, url):
        part_url = re.search(r"\d+",url).group()
        ajax_url = "http://service.library.mtime.com/Movie.api?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Library.Services&Ajax_CallBackMethod=GetMovieOverviewRating&Ajax_CrossDomain=1&Ajax_RequestUrl=http%3A%2F%2Fmovie.mtime.com%2F"+part_url+"%2F&t="+time.strftime("%Y%m%d%H%M%S0368", time.localtime())+"&Ajax_CallBackArgument0="+part_url
        a_html,a_response = self.get_response(ajax_url)
        if a_response.status_code==200:
            a_content = re.search("=(.*?);",a_response.text).group(1)
            json_a = json.loads(a_content)
            json_handle_a = json_a["value"]["movieRating"]
            score = str(json_handle_a["RatingFinal"])
            attitude_count = str(json_handle_a["AttitudeCount"])
        else:
            score = "此电影目前没有此值。"
            attitude_count = "此电影目前没有此值。"
        self.offset += 1
        return score,attitude_count

    def save_mysql(self,name,author,pub_year,content,score,attitude_count):
        mysql_cli = connect(host="192.168.43.218",port=3306,user="root",passwd="054120",db="marriage",charset="utf8")
        cursorl = mysql_cli.cursor()
        print "正在存储第"+str(self.offset)+"条信息；"
        sql = 'insert into movie_info (name,author,score,attitude_count,pub_year,content) values ("%s","%s","%s","%s","%s","%s")'%(name,author,score,attitude_count,pub_year,content)
        cursorl.execute(sql)
        mysql_cli.commit()
        cursorl.close()
        print "第"+str(self.offset)+"条电影信息存储完成。\n\n"

def main():
    crawlmovie = Crawlmovie()
    crawlmovie.crawl_page()
    print "信息已全部传输至数据库。"

if __name__=="__main__":
    main()

#https://blog.csdn.net/weixin_40539892/article/details/78879233