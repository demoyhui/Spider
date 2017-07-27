#encoding:utf8
from __future__ import division
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import sys
reload(sys)
sys.setdefaultencoding( "utf8" )
class Scrape:
    def init(self):
        self.url_all=[]
        self.driver = webdriver.Chrome(executable_path='D:\professional  software\python\Scripts\chromedriver.exe')
    def scrapeURL(self):
        url = 'http://demo.adlife.com.cn:889/wlgg/#g=1&p=首页'
        self.driver.get(url)
        data = self.driver.page_source
        soup=bs(data,'html.parser')
        for fnode in soup.findAll('a',attrs={'class':'sitemapPageLink'}):
            fname = fnode.text
            self.url_all.append(fname)
        print self.url_all
    def scrapeHTML(self):
        for fname in self.url_all:
            time.sleep(10)
            url = r'http://demo.adlife.com.cn:889/wlgg/'+fname+'.html'+'#g=1&p=首页'
            self.driver.get(url)
            data = self.driver.page_source
            print data
            print(self.driver.current_url)
            res_ad = 'E:\data'+'\\'+fname+'.txt'
            f = open(res_ad,'w')
            f.write(data)
            f.close()

        self.driver.quit()



scrape = Scrape()
scrape.init()
scrape.scrapeURL()
scrape.scrapeHTML()




