#coding=utf-8

from redis import *
from MySQLdb import *
import json

def main():
    rediscli = StrictRedis("192.168.43.218",6379,0)
    mysqlcli = connect(host="192.168.43.218",port=3306,user="root",passwd="054120",db="marriage",charset="utf8")
    while True:
        souce,data = rediscli.blpop(["juzi:items"])
        item = json.loads(data)
        cursorl= mysqlcli.cursor()
        sql = "insert into company_info (c_name,c_fullname,c_type,c_status,c_link) values ('%s','%s','%s','%s','%s')" %(item['c_name'],item['c_fullname'],item['c_type'],item['c_status'],item['c_link'])
        cursorl.execute(sql)
        mysqlcli.commit()
        cursorl.close()

#if __name__=="__main__":
main()