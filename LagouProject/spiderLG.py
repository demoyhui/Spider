#encoding=utf8
import urllib2
from bs4 import BeautifulSoup
import socket
import urllib
import requests
import random
from LagouProject.dbhelper import TestDBHelper
import threading
import time
import re
from lxml import etree
from scrapy.conf import settings
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#设置header
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.113 Safari/537.36'
header = {}
header['User-Agent'] = User_Agent

'''
获取西刺首页的所有代理IP地址
'''
def getProxyIp():
     proxy = []
     for i in range(1,2):
          try:
               url = 'http://www.xicidaili.com/nn/'+str(i)
               req = urllib2.Request(url,headers=header)
               res = urllib2.urlopen(req).read()
               soup = BeautifulSoup(res,'html.parser',from_encoding='utf8')
               ips = soup.findAll('tr')
               for x in range(1,len(ips)):
                ip = ips[x]
                tds = ip.findAll("td")
                ip_temp = tds[1].contents[0]+"\t"+tds[2].contents[0]
                proxy.append(ip_temp)
          except:
                continue
     return proxy

'''
验证获得的代理IP地址是否可用
'''

def validateIp(proxy):
      url = "http://ip.chinaz.com/getip.aspx"
      available_ip =[]
      socket.setdefaulttimeout(3)
      for i in range(0,len(proxy)):
          try:
               ip = proxy[i].strip().split("\t")
               proxy_host = "http://"+ip[0]+":"+ip[1]
               proxy_temp = {"http":proxy_host}
               res = urllib.urlopen(url,proxies=proxy_temp).read()
               available_ip.append(proxy_host)
               #print proxy[i]
          except Exception,e:
               continue
      return available_ip

def spider(validateProxy,max_threads=2):
     dbhelper = TestDBHelper()
     #调用TestDBHelper中的testSelect方法读取数据库中的URL
     results = dbhelper.testSelect()
     rLock = threading.RLock()  #RLock对象
     s  = requests.session()
     #需要抓取的URL列表
     url_queue=[]
     #职位列表
     name_list=[]
     #访问失败URL列表
     fail_url=[]
     fail_name=[]
     for row in results:
         name = row[1]
         url = row[2]
         name_list.append(name)
         url_queue.append(url)
     #设置代理
     def process_queue():
          #随机选取一个IP代理
          IP = random.choice(validateProxy)
          while True:
              try:
                  rLock.acquire()
                  url = url_queue.pop()
                  name = name_list.pop()
                  rLock.release()
                  #sleep_time = (random.choice(num_list)%3)*10 #设置随机睡眠时间
                  time.sleep(5)
                  print  'sub thread start!the thread name is:%s\r' % threading.currentThread().getName()
              except:
                  #判断url_queue是否为空
                  rLock.release()
                  break
              try:
                  #设置代理
                  proxies = {
                      'http' :  IP,
                  }
                  print IP
                  cookie = settings['COOKIE']  # 带着Cookie向网页发请求
                  #print cookie
                  #将字典转为CookieJar：
                  cookies = requests.utils.cookiejar_from_dict(cookie, cookiejar=None, overwrite=True)
                  s.cookies= cookies
                  html = s.get(url,headers=header, timeout=10,proxies=proxies,).content.encode('utf-8')
                  #print html
                  page = etree.HTML(html.decode('utf-8'))
                  #print page
                  elements = page.xpath("//div[@class='position-content-l']/dd//span")
                  #print len(elements)
                  #break

                  #一条数据库记录的信息存放在这个列表中
                  content_list=[]
                  for element in elements:
                      content = element.text
                      #print content
                      if content:
                          content = content.replace('/','')
                          if 'k' in content or '年' in content or 'K' in content:
                                 list = re.findall(r'\d+',content)
                                 value = [float(i) for i in list]
                                 content = sum(value)/len(value)
                      else:
                          content = 'null'
                      content_list.append(content)

                  content_list.append(name)
                  #print content_list
                  #将记录插入数据库
                  dbhelper.testInsert(content_list)

              except Exception,e:
                  print '---------------------------------------异常'
                  print url
                  print e
                  IP = random.choice(validateProxy) #如果在timeout内没有访问网页成功，从新选择一个代理
                  rLock.acquire()
                  fail_name.append(name)
                  fail_url.append(url)  #把访问失败的网页添加到fail_url以备递归访问
                  rLock.release()
                  continue
     #设置多线程
     threads=[]
     while threads or url_queue:
          for thread in threads:
              if not thread.is_alive():
                 #移除the stopped threads
                 threads.remove(thread)
          while len(threads) < max_threads and url_queue:
              time.sleep(5)
              #can start some more threads
              thread = threading.Thread(target=process_queue)
              # set daemon so main thread can exit when receives ctrl-c
              thread.setDaemon(True)
              print '---------------------------------------------------------------------------------多线程'+thread.name

              thread.start()
              threads.append(thread)
          time.sleep(1)


     if fail_url:   #把访问失败的URL递归调用spider方法
         failspider(fail_url,fail_name,validateProxy,max_threads=1)



def failspider(url_list,name_list,proxy,max_threads=2):
      print url_list
      print name_list
      dbhelper = TestDBHelper()
      s  = requests.session()
      rLock = threading.RLock()  #RLock对象
      #访问失败URL列表
      fail_url=[]
      fail_name=[]
      def process_queue():
          #随机选取一个IP代理
          IP = [random.choice(proxy)]
          while True:
              try:
                  rLock.acquire()
                  url = url_list.pop()
                  name = name_list.pop()
                  rLock.release()
                  #sleep_time = (random.choice(num_list)%3)*10
                  time.sleep(5)
                  print  'sub thread start!the thread name is:%s\r' % threading.currentThread().getName()
              except:
                  #判断url_queue是否为空
                  rLock.release()
                  break
              try:
                  #设置代理
                  proxies = {
                      'http' :  IP,
                  }
                  print IP
                  cookie = settings['COOKIE']  # 带着Cookie向网页发请求
                  #print cookie
                  #将字典转为CookieJar：
                  cookies = requests.utils.cookiejar_from_dict(cookie, cookiejar=None, overwrite=True)
                  s.cookies= cookies
                  html = s.get(url,headers=header, timeout=10,proxies=proxies).content.encode('utf-8')
                  #print html
                  page = etree.HTML(html.decode('utf-8'))
                  #print page
                  elements = page.xpath("//div[@class='position-content-l']/dd//span")
                  #break
                  #一条数据库记录的信息存放在这个列表中
                  content_list=[]
                  for element in elements:
                      content = element.text
                      if content:
                          content = content.replace('/','')
                          if 'k' in content or '年' in content or 'K' in content:
                                 list = re.findall(r'\d+',content)
                                 value = [float(i) for i in list]
                                 content = sum(value)/len(value)
                      else:
                          content = 'null'
                      content_list.append(content)

                  content_list.append(name)
                  #print content_list
                  #将记录插入数据库
                  dbhelper.testInsert(content_list)

              except Exception,e:
                  print '---------------------------------------异常'
                  print e
                  IP = random.choice(validateProxy) #如果在timeout内没有访问网页成功，从新选择一个代理
                  rLock.acquire()
                  fail_url.append(name)
                  fail_name.append(url)  #把访问失败的网页添加到fail_url以备递归访问
                  rLock.release()
                  continue
      #设置多线程
      threads=[]
      while threads or url_list:
          for thread in threads:
              if not thread.is_alive():
                 #移除the stopped threads
                 threads.remove(thread)
          while len(threads) < max_threads and url_list:
              time.sleep(5)
              #can start some more threads
              thread = threading.Thread(target=process_queue)
              # set daemon so main thread can exit when receives ctrl-c
              thread.setDaemon(True)
              print '---------------------------------------------------------------------------------多线程'+thread.name
              thread.start()
              threads.append(thread)
          time.sleep(1)


      if fail_url:   #把访问失败的URL递归调用spider方法
          failspider(fail_url,fail_name,proxy,max_threads=1)




if __name__ == '__main__':
 # proxy = getProxyIp()
 # validateProxy = validateIp(proxy)
 # print validateProxy
 validateProxy=[u'http://60.209.166.172:8118', u'http://121.43.227.212:808', u'http://113.87.90.218:53281', u'http://112.123.42.94:9745', u'http://175.42.102.252:8118', u'http://116.248.172.233:80', u'http://175.16.221.31:8118', u'http://171.36.182.180:8118', u'http://115.215.50.218:8118', u'http://171.126.12.9:80', u'http://113.205.0.23:8118', u'http://106.58.152.171:80', u'http://59.63.178.203:53281', u'http://111.155.116.239:8123', u'http://117.90.34.87:8118', u'http://111.155.116.200:8123', u'http://61.183.176.122:53281', u'http://112.114.96.94:8118', u'http://58.49.122.30:53281', u'http://112.114.94.8:8118', u'http://27.22.63.12:808', u'http://112.114.78.28:8118']

 spider(validateProxy,max_threads=2)