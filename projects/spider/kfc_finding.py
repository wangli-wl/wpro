#coding=utf-8

import requests
import json
from redis import *

class Finding_job(object):
    def __init__(self):
        print "欢迎来到肯德基餐厅信息查询系统！\n" +"-------------------------------"*8+"\n"
        self.num = 0

    def get_save_info(self):
        self.cname = raw_input("请输入您想要查询的城市(没有特殊要求请按0)  --- ")
        if self.cname=="0":
            self.cname = ""
        case = raw_input("请输入您想要的服务（没有特殊要求请按0)：1.生日餐会   2.全天营业   3.Wi - Fi   4.店内参观   5.三对三   6.手机点餐  ---  ")
        if int(case)>6:
            case = raw_input("服务内容输入有误，请重新输入  --- ")
        elif case=="0":
            self.pid =""
        elif case=="1":
            self.pid = 20
        elif case=="2":
            self.pid = 13
        elif case=="3":
            self.pid = 31
        elif case=="4":
            self.pid = 21
        elif case=="5":
            self.pid = 19
        elif case=="6":
            self.pid = 35
        self.keyword = raw_input("请输入其他关键词（没有特殊要求请按0)  --- ")
        if self.keyword=="0" :
            self.keyword = ""
        self.get_count()

    def get_response(self,url):
        sess = requests.session()
        formdata = {
            "cname": self.cname,
            "pid": self.pid,
            "keyword": self.keyword,
            "pageIndex": self.page,
            "pageSize": 10
        }
        response = sess.post(url, formdata, headers=self.header)
        d_text = json.loads(response.text)
        return d_text

    def get_count(self):
        if self.keyword!="":
            url = "http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword"
        else:
            if self.pid!="":
                url = "http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=pid"
            else:
                url = "http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname"
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"
        }
        self.page = 1
        formdata = {
            "cname": self.cname,
            "pid":self.pid,
            "keyword":self.keyword,
            "pageIndex":self.page,
            "pageSize":10
        }
        d_text = self.get_response(url)
        count = d_text["Table"][0]["rowcount"]
        if count==0:
            print "\n抱歉，未找到相关搜索结果，请重新搜索.\n"
            self.quit()
        else:
            print "-------\n共查询到" + str(count) + "条结果-------"
            ask_save = raw_input("是否需要保存至数据库？\n1.是    2.否\n")
            if ask_save == "1":
                print "\n正在存储至数据库,请稍等..."
                if count%10!=0:
                    pages = count/10+1
                else:
                    pages = count/10
                for page in range(1,pages+1):
                    self.parse_page(url,page,ask_save)
                print ".........."
                print "存储完成！"
                self.quit()
            else:
                self.quit()

    def parse_page(self,url,page,ask_save):
        self.page = page
        d_text = self.get_response(url)
        for store in  d_text["Table1"]:
            storeName = store["storeName"]
            location = store["provinceName"] + store["cityName"]
            addressDetail = store["addressDetail"]
            service = store["pro"]
            self.num += 1
            self.save_info(storeName,location,addressDetail,service)

    def save_info(self,storeName,location,addressDetail,service):
        redis_cli = StrictRedis(host="192.168.43.218",port=6379,db=0)
        pipe = redis_cli.pipeline()
        s_num = str(self.num)
        pipe.set("Total_num",self.num)
        pipe.set(s_num+":"+"storeName", storeName)
        pipe.set(s_num+":"+"location",location)
        pipe.set(s_num+":"+"addressDetail", addressDetail)
        pipe.set(s_num+":"+"service", service)
        pipe.execute()
        print s_num, "：", storeName, "   ", location, "   ", addressDetail, "   ", service

    def quit(self):
        print "\n" + "-------------------------------" * 8 + "\n谢谢您的使用！再见！"

def main():
    finding_job = Finding_job()
    finding_job.get_save_info()

if __name__=="__main__":
    main()


#https://blog.csdn.net/t7sfokzord1jaymsfk4/article/details/78758345
