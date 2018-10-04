#coding=utf-8

import requests
from threading import Thread
from multiprocessing import Queue
import time
from lxml import etree
import json

class Thread_data(object):
    def __init__(self):
        self.Exit = False
        self.thread_list = ["线程1号","线程2号","线程3号"]
        self.page_queue = Queue(10)
        for i in range(1,5):
            self.page_queue.put(i)
        #print self.page_queue

    def get_data(self):
        url = "https://www.qiushibaike.com/8hr/page/"
        headers = {
            "User-Agent" : "User-Agent: Mozilla/5.0-----"
        }
        i = 0
        while not self.Exit:
            thread_name = self.thread_list[i]
            try:
                self.page = self.page_queue.get(False)
                print "\n"
                '''
                调用队列对象的get()方法从队头删除并返回一个项目。可选参数为block，默认为True。
                如果队列为空且block为True，get()就使调用线程暂停，直至有项目可用。
                如果队列为空且block为False，队列将引发Empty异常。
            '''
                thread_getdata = Thread_getdata(url,headers,self.page,thread_name)
                thread_getdata.start()
                time.sleep(3)
                i += 1
                if i==3:
                    i = 0
            except:
                self.Exit = True

class Thread_getdata(Thread):
    def __init__(self,url_name,headers_name,page,thread_name):
        self.part_url = url_name
        self.headers = headers_name
        self.page = page
        self.thread_name = thread_name
        super(Thread_getdata,self).__init__()

    def run(self):
        #print page
        print "正在获取第%d页数据,"%self.page+self.thread_name+"开始，"
        url = self.part_url+str(self.page)+"/"
        print url
        response = requests.get(url,headers = self.headers)
        html = response.text
        #print html
        print "已获得第%d页数据,"%self.page+self.thread_name+"已结束。"
        self.handle_data(html)

    def handle_data(self,html):
        e_html = etree.HTML(html)
        e_html_list = e_html.xpath('//div[contains(@id,"qiushi_tag")]')
        # print e_html_list
        for temp in e_html_list:
            try:
                user_num = temp.xpath('./div/a/@href')[0]
            except:
                user_num = temp.xpath('./div/a/@href')
            # print user_num[0]
            user_content = temp.xpath('./a/div/span')[0].text
            # print user_content

            data = {
                "user_name": user_num,
                "user_content": user_content
            }
            with open("joke.txt"+"-"+str(self.page), "a") as f:
                f.write(json.dumps(data, ensure_ascii=False).encode("utf-8") + "\n")


def main():
    thread_data = Thread_data()
    thread_data.get_data()
    #thread_data.parsedata()

if __name__ == "__main__":
    main()


