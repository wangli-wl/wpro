#coding=utf-8

import requests
import random
from threading import Thread,Lock
from lxml import etree
import re
import json
from MySQLdb import *
import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class C_taobao:
    def __init__(self):
        self.url = "https://www.taobao.com/"
        self.sess = requests.session()
        self.goods_info = []
        self.user_agents = [
            "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "JUC (Linux; U; 2.3.7; zh-cn; MB200; 320*480) UCWEB7.9.3.103/139/999",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0a1) Gecko/20110623 Firefox/7.0a1 Fennec/7.0a1",
            "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
            "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
            "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/1A542a Safari/419.3",
            "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7",
            "Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10",
            "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
            "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
            "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
            "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
            "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER) ",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
            "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
            "Openwave/ UCWEB7.0.2.37/28/999",
            "NOKIA5700/ UCWEB7.0.2.37/28/999",
            "UCWEB7.0.2.37/28/999",
            "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
            "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
            "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
            "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"
        ]

    def get_resonse(self,url):
        user_agent = random.choice(self.user_agents)
        self.headers = {
            "User-Agent": user_agent,
            "Accept": "text / html, application / xhtml + xml, application / xml;q = 0.9, * / *;q = 0.8",
            "Accept - Language": "zh - CN, zh;q = 0.8, zh - TW;q = 0.7, zh - HK;q = 0.5, en - US;q = 0.3, en;q = 0.2",
            "Connection": "keep - alive",
            "If - None - Match": 'W / "2a3f-165fb9a80c0"',
            "Cache - Control": "max - age = 0",
            "Accept - Encoding": "identity"
        }
        while True:
            response_text = self.sess.get(url, headers=self.headers).text
            if response_text!="":
                break
        return response_text

    def search_page(self):
        #content = raw_input("请输入您要查询的商品：")
        content = "连衣裙"
        print "正在为您查询，请稍等："
        total_page = 2
        print "获取到"+str(total_page-1)+"页数据，正在获取详细信息..."
        for page in range(1,total_page):
            s_page = str(page)
            print "    正在获取第 "+s_page+" 页商品信息..."
            url = "https://s.taobao.com/search?q="+content+"&s="+str((page-1)*44)
            response_text = self.get_resonse(url)
            pageinfo = self.process_page(response_text)
            self.goods_info.append(["第"+s_page+"页的商品信息",pageinfo])
            print "    已获取第 "+s_page+" 页商品信息...\n"
        print "\n已获取全部商品信息。"

    def process_page(self, response_text):
        all_pagelist = []
        all_ajaxlist = []
        response = etree.HTML(response_text)
        p = response.xpath("/html/body/div[1]/div[2]/div[3]/div[1]/div[21]/div/div/div[2]/div/div[9]/div[2]/div[1]/div[1]/strong/text()")
        content = re.search("g_page_config = ({.+})", response_text).group(1)
        try:
            j_content = json.loads(content)
        except:
            raw_input("因部分原因限制，查询不到该商品信息，请更换商品或更换该商品关键词。")
            self.search_page()
        all_pageinfo = j_content["mods"]["itemlist"]["data"]["auctions"]
        for info in all_pageinfo:
            all_pagelist.append([{"nid": info["nid"]}, {"title": info["raw_title"]},
                                 {"price": info["view_price"]+"元"},{"sales": info["view_sales"]},
                                 {"post_fee": info["view_fee"]+"元"},{"location": info["item_loc"]},
                                 {"detail_url": info["detail_url"]}, {"store_name": info["nick"]}])
        url_ajax = "https://s.taobao.com/api?_ksTS=1537779777886_209&callback=jsonp210&ajax=true&m=customized&stats_click=search_radio_all:1&_input_charset=utf-8&bcoffset=-1&js=1&suggest=history_2&source=suggest&suggest_query=&q=%E8%BF%9E%E8%A1%A3%E8%A3%99&s=36&initiative_id=staobaoz_20180924&imgfile=&wq=&ie=utf8&rn=f0068d132ee9d67e39c2ad8707483cb3"
        response_ajax_text = self.get_resonse(url_ajax)
        j_content_ajax = json.loads(response_ajax_text[11:-2])
        try:
            all_ajaxinfo = j_content_ajax["API.CustomizedApi"]["itemlist"]["auctions"]
        except:
            raw_input("因部分原因限制，查询不到该商品信息，请更换商品或更换该商品关键词。")
            self.search_page()
        for info in all_ajaxinfo:
            all_ajaxlist.append([{"nid": info["nid"]}, {"title": info["raw_title"]},
                                 {"price": info["view_price"]+"元"},{"sales": info["view_sales"]},
                                 {"post_fee": info["view_fee"]+"元"},{"location": info["item_loc"]},
                                 {"detail_url": info["detail_url"]}, {"store_name": info["nick"]}])
        all_pagelist.extend(all_ajaxlist)
        for temp in all_pagelist:
            p = MyThread(self.parse_page, args=(temp[0]["nid"],))
            p.start()
            p.join()
            total_comment,score,rate_num = p.get_result()
            temp.append({"total_comment": total_comment})
            temp.append({"score":score})
            temp.append({"rate_num": rate_num})
        return all_pagelist

    def parse_page(self,nid):
        mutex.acquire()
        total_comment_url = "https://rate.tmall.com/listTagClouds.htm?itemId="+nid+"&isAll=true&isInner=true&t=1537798991731&groupId=&_ksTS=1537798991735_1009&callback=jsonp1010"
        response_comment_text = self.get_resonse(total_comment_url)
        response_comment_text = response_comment_text[12:-1]
        try:
            j_response_comment = json.loads(response_comment_text)
        except:
            self.parse_page(nid)
        comment_list =  j_response_comment["tags"]["tagClouds"]
        total_comment = ""
        for comment in comment_list:
            total_comment+=comment["tag"]+","
        total_comment = total_comment[:-1]
        if total_comment=="":
            total_comment = "抱歉，该商品目前暂无总评！"
        score_comment_url = "https://dsr-rate.tmall.com/list_dsr_info.htm?itemId="+nid+"&spuId=1035082562&sellerId=898571545&groupId&_ksTS=1537851874186_340&callback=jsonp341"
        response_scorecomment_text = self.get_resonse(score_comment_url)
        response_scorecomment_text = response_scorecomment_text[11:-2]
        try:
            j_response_scorecomment = json.loads(response_scorecomment_text)
        except:
            self.parse_page(nid)
        score = str(j_response_scorecomment["dsr"]["gradeAvg"])+"分"
        if score=="0分":
            score = "null"
        rate_num = str(j_response_scorecomment["dsr"]["rateTotal"])+"条评论"
        mutex.release()
        return total_comment,score,rate_num

    def save_mysql(self):
        print "\n商品信息正在存储中...."
        num = float(0)
        goods_num = 0
        for temp in self.goods_info:
            goods_num += len(temp[1])
        conn = connect(host="192.168.43.218",port=3306,user="root",passwd="054120",db="info",charset="utf8")
        cur = conn.cursor()
        for temp1 in self.goods_info:
            for temp2 in temp1[1]:
                detail_url = temp2[6]['detail_url']
                if detail_url.startswith("//"):
                    detail_url = "https:"+detail_url
                sql = "insert into goods_info(nid,goods_title,price,sales,post_fee,location,detail_url,store_name,total_comment,score,rate_num) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(temp2[0]['nid'],temp2[1]['title'],temp2[2]['price'],temp2[3]['sales'],temp2[4]['post_fee'],temp2[5]['location'],detail_url,temp2[7]['store_name'],temp2[8]['total_comment'],temp2[9]["score"],temp2[10]["rate_num"])
                cur.execute(sql)
                conn.commit()
                num += 1
                save_rate = num/goods_num*100
                print "当前存储进度为%0.2f%%..\r"%save_rate,
        cur.close()
        conn.close()
        print "\n商品信息已存储完成！"

class MyThread(Thread):
    def __init__(self,func,args=()):
        super(MyThread,self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None

mutex = Lock()

def main():
    print "-" * 20 + "欢迎来到淘宝商品信息查询处！" + "-" * 20 + "\n"
    c_taobao = C_taobao()
    c = c_taobao.search_page()
    #c_taobao.save_mysql()
    print "\n\n" + "-" * 20 + "商品信息获取完成，感谢您的使用！" + "-" * 20
    return "hahahahahaha"

if __name__ == '__main__':
    main()






