#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author:Fangyang
@User:haizhi
@File:JUDGEMENT_WENSHU_for_jilin
@time:2018/8/8下午5:57
@Software:PyCharm

"""
import time
import random
import re

import json
import requests
import pymysql
import pymongo
from bs4 import BeautifulSoup
#config_of_mysql = pymysql.connect("localhost", "root", "fangyang", "test")
config_of_mongodb = pymongo.MongoClient('mongodb://localhost:27017')


header = {'User-Agent:': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 \
                      (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}


class Judgement_wenshu(object):
    def __init__(self, database_name, url):
        self.database_name = database_name
        self.url = url
        self.id_list = []
        self.title_list = []
        self.Pageurl_list = []
        self.source_page_list = []
        self.wenshu_content = []

    def link_database(self):#默认使用mongodb
        # noinspection PyBroadException
        try:
            if self.database_name == "mysql":
                return 0
            elif self.database_name == "mongodb":
                return config_of_mongodb
        except Exception:
            print("缺少数据库名称，默认使用mongodb")
            return config_of_mongodb

    def start_request(self, ip):
        proxy = {
            'http': 'http://{}'.format(ip),
            'https': 'https:{}'.format(ip)
        }
        try:
            context = requests.get(self.url).text
        except Exception as e:
            print(e + "访问失败")
            return -1
        soup = BeautifulSoup(context, "html.parser")
        content_url = "http://www.jlsfy.gov.cn:8080/susong51/cpws/loadPrintContent.htm?id="#详情页的获取页面
        list_context = soup.find_all(onclick=re.compile('javascript:cpwsDetail'))
        for tag in list_context:
            self.id_list.append(tag['onclick'][23:-3])
            temp = str(tag.contents[1]).split('>')
            self.title_list.append(temp[3][:-3])
        for id in self.id_list:
            url1 = content_url + id
            self.Pageurl_list.append(url1)
            if len(self.id_list) == 0:
                return 0
            page_content = requests.get(url1, header).text
            print("获取到"+url1+"的数据")
            temp_js = json.loads(page_content)
            self.source_page_list.append(temp_js['data'])
            print(str(url1) + "    " + "ok")
            # 获取到信息以后剔除HTML标签
            pat = re.compile('>(.*?)<')
            p = ''.join(pat.findall(temp_js['data']))
            self.wenshu_content.append(p)
        return 1

    def write_to_database(self):
        global config_of_mongodb
        if self.databasename == "mysql":
            for i in range(len(self.title_list)):
                sql = "INSERT IGNORE INTO judgement_wenshu(wenshu_content, \
                                  case_name, _site_record_id,topic,source,source_page,PageUrl,_in_time) \
                                  VALUES ('%s', '%s', '%s','%s','%s','%s','%s','%s')" % \
                      (self.wenshu_content[i],
                       self.title_list[i],
                       "www.jlsfy.gov.cn:8080",
                       "0",
                       "judgement_wenshu",
                       "诉讼无忧新版采集脚本v0_吉林高院省",
                       self.source_page_list[i],
                       self.Pageurl_list[i],
                       time.time())
                #cursor = config_of_mysql.cursor()
               # cursor.execute(sql)
               # config_of_mysql.commit()
            return 1
        elif self.database_name == "mongodb":
            for i in range(len(self.title_list)):
                mycol = config_of_mongodb['test']['judgement_wenshu']
                mycol.insert_one({"wenshu_content": self.wenshu_content[i], 'case_name': self.title_list[i],
                                  'site_record_id': 'www.jlsfy.gov.cn:8080',
                                  'topic': 'judgement_wenshu',
                                  'source': '诉讼无忧新版采集脚本v0',
                                  'source_page': self.source_page_list[i],
                                  'PageUrl': self.Pageurl_list[i],
                                  '_in_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                  }
                                 )
            return 1

    def work(self):
        myip=config_of_mongodb['proxy']
        ip = []
        myproxy = myip['raw_proxy'].find()
        for i in myproxy:
            ip.append(i['proxy'])
        self.start_request(random.choice(ip))
        self.writetodatabase()


if __name__ == '__main__':

    cjws = Judgement_wenshu('mongodb', 'http://www.jlsfy.gov.cn:8080/susong51/fymh/750/cpws.htm?page=1')
    cjws.work()
                










