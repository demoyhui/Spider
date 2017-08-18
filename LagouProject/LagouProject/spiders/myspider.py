# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import re
from scrapy.http import Request
from LagouProject.items import LagouprojectItem
from scrapy.conf import settings

class MyspiderSpider(scrapy.spiders.Spider):
    name = 'myspider'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']
    cookie = settings['COOKIE']  # 带着Cookie向网页发请求
    def parse(self, response):
        se=Selector(response) #创建查询对象

        if(re.match("https://www.lagou.com/", response.url)):#如果url能够匹配到需要爬取的url就爬取  [starts-with(@href, 'https://www.lagou.com/zhaopin/')]
            src = se.xpath("//div[@class='mainNavs']/div[1]//div[@class='category-list']/a")
            for i in range(1,len(src)+1):
                name = se.xpath("//div[@class='mainNavs']/div[1]//div[@class='category-list']/a[%d]/text()"%i).extract()#获取a标签中的内容
                url = se.xpath("//div[@class='mainNavs']/div[1]//div[@class='category-list']/a[%d]/@href"%i).extract()#获取a标签中的href属性地址
                if name and url:
                     yield Request(url=url[0], meta={'name': name[0]}, callback=self.parse_url ,cookies=self.cookie)



    def parse_url(self,response):          #该函数是用来获取每一个招聘公司的url和招聘的职位
        name = response.meta['name']
        cookie = response.request.headers.getlist('Cookie')
        print '-----------------------------------------------cookie'
        print cookie
        # print response.body
        se = Selector(response)
        if(re.match("https://www.lagou.com/", response.url)):
            src = se.xpath("//div[@id='s_position_list' ]/ul/li")
            for i in range(1,len(src)+1):
                url = se.xpath("//div[@id='s_position_list' ]/ul/li[%d]//a[@class='position_link']/@href"%i).extract()#获取个招聘信息的详细页面的url
                item = LagouprojectItem()
                item['name'] = name
                item['url'] = url[0]
                yield  item
            nextpage = se.xpath("//div[@class='pager_container']/a[last()]/@href").extract()#获取下一页的地址
            print nextpage
            if (re.match(r"https://www.lagou.com/zhaopin/\w+/\d+/",nextpage[0])):  #判断是否为最后一页
                yield Request(url=nextpage[0], meta={'name': name}, callback=self.parse_url)
                response.request.headers.getlist('Cookie')



