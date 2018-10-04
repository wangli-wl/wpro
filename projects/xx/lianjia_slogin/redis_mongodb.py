#coding=utf-8

from redis import *
from pymongo import *
import json

def main():
    redis_cli = StrictRedis(host="192.168.43.218",port=6379,db=0)
    mongodb_cli = MongoClient("192.168.43.218",27017)
    db = mongodb_cli.info
    lianjia = db.lianjia
    num = 1

    while True:
        souce,data = redis_cli.blpop("lianjia:items")
        data = json.loads(data)
        lianjia.insert({"lianjia_selling":data})
        #lianjia.insert_one({"house_attr": data["house_attr"]})
        #lianjia.insert_one({"house_info":data["house_info"]})
        #lianjia.insert_one({"deal_attr":data["deal_attr"]})
        #lianjia.insert_one({"price":data["price"]})
        num += 1
        print num

if __name__=="__main__":
    main()


