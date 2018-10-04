#coding=utf-8

from redis import *
from MySQLdb import *
import json

def main():
    rediscli = StrictRedis(host="192.168.43.218",port=6379,db=0)
    mysqlcli = connect(host="192.168.43.218",port=3306,user="root",passwd="054120",db="marriage",charset="utf8")

    while True:
        # FIFO模式为 blpop，LIFO模式为 brpop，获取键值
        source, data = rediscli.blpop(["marrige_net:items"])
        item = json.loads(data)

        print item['thought']
        print "1"

        #try:
        # 使用cursor()方法获取操作游标
        cur = mysqlcli.cursor()
        # 使用execute方法执行SQL INSERT语句
        sql = "insert into marrige_info (thought, nickname) values ('%s', '%s')" % (item['thought'], item['id'])
        cur.execute(sql)
        # 提交sql事务
        mysqlcli.commit()
        # 关闭本次操作
        cur.close()
        #mysqlcli.close()
            #print "inserted %s" % item['source_url']
        #except Exception, e:
            #print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            #print e.message


#if __name__ == '__main__':
main()
