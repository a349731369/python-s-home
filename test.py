#utf-8
import os
import sys

class locoy(object):
    def __init__(self,out):
        if not os.path.exists(out.replace('/','')):
            os.mkdir(out)
        else:
            if os.path.isfile(out.replace('/','')):
                print(out.replace('/',''),'is file and had existed')
                quit()
            else:
                print(out,'had existed')
        self.out=out
        self.quantity_check_file=open(out+'Qquantity_CHECK_FILE.txt','w')
        self.quality_check_file = open(out + 'QUALITY_check_file.txt', 'w')
        self.error_file = open(out + 'error_file.txt', 'w')
        self.section_statistics_file = open(out + 'statistics_file.txt', 'w')
    def __del__(self):#析构的时候关闭文件流
        self.quality_check_file.close()
        self.quantity_check_file.close()
        self.error_file.close()
        self.section_statistics_file.close()

    def read_locoy_file(self, file_name):  # 读文件，参数是obj和文件名
        strall = ''  # 所有内容
        if not file_name.endswith('.txt'):  # 如果不是txt后缀文件，直接返回
            return
        with open(file_name, 'r') as pre:  # 如果是，打开文件读入
            for str1 in pre.readlines():  # 一行
                strall = strall + str1
        strsplit = strall.split('====================\n')  # 分割
        count = 0
        for x in strsplit:  # 对分割出来的每个模块
            content = x.strip()
            count += 1
            print(str(count) + '. ' + content)


def run():
    obj=locoy('/data/湖北/')



if __name__=='__main__':
    run()