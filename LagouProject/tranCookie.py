# -*- coding: utf-8 -*-

class transCookie:
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict

if __name__ == "__main__":
    cookie = 'user_trace_token=20170721092216-b224b3ce957742f3b97342fc87749e21; LGUID=20170721092217-08f5f7cf-6db3-11e7-b96a-525400f775ce; X_HTTP_TOKEN=70f85cc2cdec3e249d99fbd5fdb73b0d; TG-TRACK-CODE=index_navigation; SEARCH_ID=0b2f7926a1894aa29f572c8d52409b6b; index_location_city=%E6%9D%AD%E5%B7%9E; _gid=GA1.2.286872729.1502773844; JSESSIONID=ABAAABAAAGFABEF26AEF8784B5B7A882A42E6052138C577; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1502512410,1502626911,1502628414,1502773844; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1502949211; _ga=GA1.2.48583056.1500600144; _gat=1; LGSID=20170817135330-65b8f3eb-8310-11e7-896d-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGRID=20170817135330-65b8f67c-8310-11e7-896d-5254005c3644; _putrc=898B7EED4E87F460; login=true; unick=%E5%BC%A0%E4%BA%9A%E8%BE%89; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=19'
    trans = transCookie(cookie)
    print trans.stringToDict()