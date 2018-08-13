# -*- coding: utf-8 -*-
import sys
import os

pathroad=os.listdir('/Users/haizhi/PycharmProjects/data/1')

dpath='/Users/haizhi/PycharmProjects/data/1/'

#for filename in pathroad:
errordist={1:'标题',2:'内容',3:'地区',4:'主题',5:'host',6:'脚本',7:'日期',8:'源码'}
errormeg=[]
strall=''
def reader(filename):
    global errordist
    global errormeg
    global strall
    if not str(filename).endswith('.txt'):
        return
    with open(filename,'r')as pre:
        for strtemp in pre.readlines():
            strall=strall+strtemp
    strsplit=strall.split('====================\n')
    count=0
    for x in strsplit:
        content=x.strip()
        count+=1
        #print(str(count)+'.'+content)
        if len(content)==0:
            if count<9:
                print(str(filename+errordist[count]+'为空'))
                errormeg.append(str(filename+errordist[count]+'为空'))
            else:
                continue

for item in pathroad:
    temp=dpath+item
    reader(temp)
    print('完成'+temp)
print(errormeg)