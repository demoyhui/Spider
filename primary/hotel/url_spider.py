#coding:utf-8
import urllib2
import time
from  bs4 import BeautifulSoup as bs
import re
import MySQLdb



def urls():
    count = 0
    for i in range(1,51):
        if count % 5:
            time.sleep(3)
        url="https://www.dianping.com/hangzhou/hotel/"+"p"+str(i)

        #headers camouflage
        useragent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
        headers={

            'User-Agent':useragent
        }

        req=urllib2.Request(url,"",headers)
        res=urllib2.urlopen(req)
        data=res.read()
        res.close()

        '''
        parse and select what i need
        '''
        #BeautifulSoup(data) will transform [data] in unicode automatically
        soup=bs(data,'html.parser',from_encoding='utf8')
        hotelurls=[]#define a list for hotelurls

        for li in soup.find_all('li',class_=' hotel-block J_hotel-block'):
            for h in li.find_all('h2',class_='hotel-name'):
                for node in h.find_all('a',href=re.compile(r'/shop/\d*'),class_='hotel-name-link'):
                    insertdb(node.text,node['href'])
        count += 1
    db.close()


def conndb():
    #连接数据库
    conn=MySQLdb.connect(host="localhost",user="root",passwd="123",db="spider",charset="utf8")
    return conn

db = conndb()

def insertdb(name,url):
    cursor=db.cursor()
    sql = "insert into hotelurls(hotelname,hotelurl) values(%s,%s)"
    param=(name,url)
    cursor.execute(sql,param)
    cursor.close()
    db.commit()


if __name__ == "__main__":
    urls()