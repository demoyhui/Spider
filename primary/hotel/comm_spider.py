#coding:utf-8
import re
import urllib2
from bs4 import  BeautifulSoup as bs
import time
import MySQLdb

useragent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
headers={

'User-Agent':useragent
}

def comment():
   for row in relist:
       hotelname=row[0]
       hotelurl=row[1]
       print hotelname,hotelurl
       #酒店评论首页url
       index_url="https://www.dianping.com"+hotelurl+"/review_more"

       req=urllib2.Request(index_url,"",headers)
       res=urllib2.urlopen(req)
       data=res.read()
       res.close()

       soup=bs(data,'html.parser',from_encoding='utf8')

       result=soup.find_all('a',href=re.compile(r'\?pageno=\d'),class_='PageLink')

       try:
           for i in range(1,int(result[-1].text)+1):
               comment_url=index_url+"?pageno="+str(i)
               req=urllib2.Request(comment_url,"",headers)
               res=urllib2.urlopen(req)
               data=res.read()
               res.close()
               soup=bs(data,'html.parser',from_encoding='utf8')
               li=soup.findAll('li',attrs={'id':re.compile(r'rev_\d*')})
               for aa in li:
                   try:
                       #用户名

                       node=aa.find_all('a',href=re.compile(r'/member/\d*'))
                       username=node[1].text.strip()

                       #评论
                       node=aa.find('div',class_='J_brief-cont')
                       comment=node.text.strip()

                       #去掉评论中的表情
                       temp = ""
                       for i in comment:
                            try:
                                i.encode("gbk")
                                temp = temp + i
                            except:
                                continue
                       comment=temp
                       #时间

                       node=aa.find('span',class_='time')
                       ctime=node.text[0:5]

                       #星数

                       node=aa.find('span',class_=re.compile(r'item-rank-rst irr-star\d0'))
                       cstar=node['class'][1][-2:-1]

                       insertdb(hotelname,username,ctime,cstar,comment)
                   except :
                       print "出现可容错异常！"
               time.sleep(1)
       except :
           print "出现可容错异常！"
       time.sleep(5)
   db.close()












def conndb():
    #连接数据库
    conn=MySQLdb.connect(host="localhost",user="root",passwd="123",db="spider",charset="utf8")
    return conn

db = conndb()

def selectdb():
    cursor=db.cursor()
    sql="select hotelname,hotelurl from hotelurls WHERE id >156"
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    db.commit()
    return result
#relist存放数据库查询结果集
relist=selectdb()

def insertdb(hotelname,username,ctime,cstar,comment):
    cursor=db.cursor()
    sql = "insert into hotelcomment(hotelname,username,ctime,cstar,comment) values(%s,%s,%s,%s,%s)"
    param=(hotelname,username,ctime,cstar,comment)
    cursor.execute(sql,param)
    cursor.close()
    db.commit()



if __name__ == "__main__":
    comment()