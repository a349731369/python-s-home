import requests
import bs4
import json
import pymysql
import datetime
database=pymysql.connect("localhost","root","fangyang","test")
cursor=database.cursor()
'''
sql="""CREATE TABLE EMPLOYEE (titel char(50) NOT NULL ,
      id char(50),
      time datetime
      )
       """
'''
#cursor.execute(sql)
titlelist=[]
idlist=[]
timelist=[]
url='http://webapi.aixifan.com/query/article/list?pageNo=2&size=100&realmIds=5%2C22%2C1%2C2%2C4&originalOnly=false&orderType=2&periodType=-1&filterTitleImage=true'

header={'User-Agent:':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

content=requests.get(url,header)
conjs=json.loads(content.text)
#print(conjs)
for item in conjs['data']['articleList']:
    titlelist.append(item['title'])
    idlist.append(item['id'])
    #timelist.append((item['tag_list'])['0']['updata_time'])
    timelist.append(datetime.datetime.fromtimestamp((int(item['tag_list'][0]['update_time'])/1000)))

print(timelist)
print(idlist)
print(titlelist)


for i in range(len(titlelist)):
    sql = "INSERT INTO EMPLOYEE(titel, \
           id, time) \
           VALUES ('%s', '%s', '%s')" % \
           (titlelist[i], idlist[i],timelist[i])
    cursor.execute(sql)
    database.commit()

database.close()