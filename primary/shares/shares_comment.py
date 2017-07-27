# coding:utf-8
from __future__ import division
from math import ceil
import re
import MySQLdb
import urllib2
from bs4 import BeautifulSoup as bs
import requests
import time
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

#headers camouflage
useragent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
headers={

        'User-Agent':useragent
}
def shares_comment():
    commenturl=[]
    #爬去顺丰控股80个页面中的所以话题url
    count=0
    for i in range(1,301):
        if count % 10:
            time.sleep(2)
        url="http://guba.eastmoney.com/list,000651_"+str(i)+".html"
        #print url
        req=urllib2.Request(url,"",headers)
        res=urllib2.urlopen(req)
        data=res.read()
        res.close()
        '''
        parse and select what i need
        '''
        #BeautifulSoup(data) will transform [data] in unicode automatically
        soup=bs(data,'html.parser',from_encoding='utf8')


        fnode=soup.find('div',attrs={"id":"articlelistnew"})
        for snode in fnode.find_all('div',class_='articleh'):
            #p为评论数
            p= int(snode.find('span',class_='l2').text)
            #s为话题种类
            s= snode .find('span',class_='l3')
            if s.find('em')==None and p>10:
                a= snode.find('a')['href']
                commenturl.append((a,p))
        count += 1
    #输出评论页面url获取成功
    print('评论页面url获取成功')



    #遍历所有话题url 获取该话题的评论信息
    count=0
    for x in commenturl:
        if count % 10:
            time.sleep(2)
        try:

            #print x
            url="http://guba.eastmoney.com"+x[0]
            pagesum=x[1]
            p=int(ceil(pagesum/30))
            for i in range(1,p+1):
                commenturl =url[0:-5]+"_"+str(i)+".html"
                print commenturl
                #print url
                req=urllib2.Request(commenturl,"",headers)
                res=urllib2.urlopen(req)
                data=res.read()
                res.close()
                #BeautifulSoup(data) will transform [data] in unicode automatically
                soup=bs(data,'html.parser',from_encoding='utf8')

                for fdiv in soup.findAll('div', class_='zwli clearfix'):
                    sdiv = fdiv.find('div', class_='zwlianame')
                    t1 = sdiv.findAll("span", class_ = "zwnick")[0]
                    t2 = t1.findAll("a")[0]
                    userurl=t2['href']
                    #用户名 username
                    username=t2.text
                    #根据用户url获取用户影响力
                    session = requests.Session()
                    session.headers = {
                        'User-Agent' :'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
                    }
                    r =session.get(userurl)
                    #正则提取
                    pattern_name=re.compile(r'data-influence="\d*"')
                    influ=re.findall(pattern_name,r.text)
                    #用户影响力 uinflu
                    uinflu=influ[0][-2:-1]

                    #评论时间 ctime
                    tnode=fdiv.find('div',class_='zwlitime')
                    ctime=tnode.text[4:]

                    #用户评论comment
                    comment =fdiv.find('div',class_='zwlitext stockcodec').text

                    #调用数据库将数据插入数据库
                    insertdb('格力电器',username,uinflu,ctime,comment)

        except :
            print ("出现原谅错误！！！")
        count += 1
    #关闭数据库
    db.close()






def conndb():
    #连接数据库
    conn=MySQLdb.connect(host="localhost",user="root",passwd="123",db="spider",charset="utf8")
    return conn

db = conndb()

def insertdb(sharename,username,uinflu,ctime,comment):
    cursor=db.cursor()
    sql = "insert into sharecomment(sharename,username,uinflu,ctime,comment) values(%s,%s,%s,%s,%s)"
    param=(sharename,username,uinflu,ctime,comment)
    cursor.execute(sql,param)
    cursor.close()
    db.commit()

if __name__ =='__main__':
    shares_comment()