import requests
import pymongo
import random
myclient=pymongo.MongoClient("mongodb://localhost:27017")
mydb=myclient['proxy']
myrol=mydb["raw_proxy"]
ip=[]
proxys=myrol.find()
for i in proxys:
    ip.append(i['proxy'])

for ipp in ip:
    proxey = {
            'http' : 'http://'+ipp
        }
    p=requests.get("http://www.baidu.com",proxies=proxys)
    print(p)