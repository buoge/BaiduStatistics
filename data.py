# coding:utf-8
import requests
from lxml import etree
from bs4 import BeautifulSoup
import re
import sys

"""
================================================
 Extract text from the result of BaiDu search

 For Python 3.6+
================================================
"""


def parse_data_in_html(file_name):
    # 加载本地的html文件内容
    htmlfile = open(file_name, 'r', encoding='utf-8')
    htmlhandle = htmlfile.read()

    # 查询结果使用BeautifulSoup处理
    soup = BeautifulSoup(htmlhandle, "lxml")

    # 获取table0
    info_list_table = soup.find("table",class_="table_0")

    # 获取除了tr_th_all外的tr,22一组,第一个是基本信息，第二个tr里面有手机号
    info_list_tr = info_list_table.find_all("tr",recursive=False)

    # 第一行是head不用管
    info_list_tr.pop(0)

    print(len(info_list_tr))

    txt_file_name = file_name + '.txt'
    with open(txt_file_name, 'a',encoding='utf8') as ct: 

        ct.write("记录数:"+str(len(info_list_tr)/2)+"\n\n")

        index_td = 1
        for into_child_tr in info_list_tr:
            
            row_odd = (index_td % 2) == 1
            if row_odd:
                group_index = (index_td + 1) / 2
                print("==============================================",group_index)
                # print(into_child_tr)
                ct.write("\n\n"+"=============================================="+str(group_index)+"\n")

                info_uid = into_child_tr.select("td:nth-of-type(2)")
                print("id:"+info_uid[0].get_text())
                ct.write("id:"+info_uid[0].get_text()+"\n")

                info_keywords = into_child_tr.select("td:nth-of-type(7)")
                print("关键词:"+info_keywords[0].get_text())
                ct.write("关键词:"+info_keywords[0].get_text()+"\n")

                info_link = into_child_tr.select("td:nth-of-type(8)")
                print("咨询页面:"+info_link[0].get_text())
                ct.write("咨询页面:"+info_link[0].get_text()+"\n")

                info_area = into_child_tr.select("td:nth-of-type(9)")
                print("地区:"+info_area[0].get_text()) 
                ct.write("地区:"+info_area[0].get_text()+"\n")

            else:
                
                td_msg_list = into_child_tr.find_all("td",class_="guest_msg")
                for msg_info in td_msg_list:
                    msg_content = msg_info.get_text()
                    number_content = re.sub("\D", "", msg_content) 
                    if (len(number_content) > 0):
                        print("获取手机号部分:",msg_content)   
                        ct.write("获取手机号部分:"+msg_content+"\n")    
                    
            
            index_td+=1
            

            # 解析数据全部存储到mogodb中
    
            # 从mongodb中取出数据并输出到excel   
    ct.close

def parseMobile():
    pass

def parseMainInfo():
    pass  
                 

def main(in_file_name):
    parse_data_in_html(in_file_name)


# 使用方法：python data.py baidudata.html, 后续这个是要处理的html文件名称
# 每个文件在命令行运行一次解析就好，重复运行会让数据在文件末尾叠加
if __name__ == '__main__':
    print('Number of arguments:',sys.argv)
    if len(sys.argv) > 1:
        in_file_name = sys.argv[1]
        main(in_file_name)
    else:
        print('Tips: 请在data.py后面键入空格并输入需要处理的文件名称')
