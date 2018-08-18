#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from lxml import etree
import json
import re
import requests
import mysqlspi
import time 

# return json.dumps(r.json())

def httprequest(pageindex):
    headers = {'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
    'Cookie':'clicktopay=1533388074284; ua_checkmutilogin=GCEgo9tvxW; pubcookie=VTJUYQ0wVTUCMgxhVjkGblIJXWQAXF1gBDUAMAZnA25Waw8HBWoCPwVlDTcFNVJ9AD1TPVVnAGFYOgZhV28AMVUxVFwNeFVlAnIMNlZmBjVSYV0vACNdbwQtABMGawNuVmEPZwVlAnkFYw02BT9SAABjU2ZVMwBkWDEGZVdkADFVNVRlDQhVYQIwDGtWOQY8UjBdagA0XW4EZABhBj0DN1ZjDz4FbwIxBWQNawVrUjkAMVM2VTQAM1g-BjFXZQAxVWFUNw02; ct_uid=b59dee7d431666d87f63d07e0879a1da',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
    }
    iDisplayStart=(pageindex - 1)*100
    payload={
    'item': 'file_act',
    'action': 'file_list',
    'folder_id': 29335756,
    'task': 'index',
    'sEcho': pageindex,
    'iColumns': 5,
    'sColumns': ',,,,',
    'iDisplayStart': iDisplayStart,
    'iDisplayLength': 100,
    'mDataProp_0': 0,
    'sSearch_0': '',
    'bRegex_0': 'false',
    'bSearchable_0': 'true',
    'bSortable_0': 'false',
    'mDataProp_1': 1,
    'sSearch_1': '',
    'bRegex_1': 'false',
    'bSearchable_1': 'true',
    'bSortable_1': 'true',
    'mDataProp_2': 2,
    'sSearch_2': '',
    'bRegex_2': 'false',
    'bSearchable_2': 'true',
    'bSortable_2': 'true',
    'mDataProp_3': 3,
    'sSearch_3': '',
    'bRegex_3': 'false',
    'bSearchable_3': 'true',
    'bSortable_3': 'true',
    'mDataProp_4': 4,
    'sSearch_4': '',
    'bRegex_4': 'false',
    'bSearchable_4': 'true',
    'bSortable_4': 'true',
    'sSearch': '',
    'bRegex': 'false',
    'iSortingCols': 0,
    '_': 1533714140931
    }
    r = requests.get('https://home.ctfile.com/iajax.php', params=payload,headers=headers)
    r.encoding='utf-8'
    dataobj=r.json()
    # print dataobj
    return dataobj
    # print(r.json().decode('unicode_escape'))

#https://segmentfault.com/q/1010000006053119

def lxmlHtml(html):
    con = etree.HTML(html)
    # print(etree.tostring(con, encoding="gb2312", pretty_print=True, method="html"))
    # print(etree.tostring(con))
    mages =  con.xpath('//div[@class="pull-left"]/a/text()')
    herf =  con.xpath('//div[@class="pull-left"]/a/@href')
    # mages =  con.xpath('//div/i[@fileicon-other]/a/text()')

    return {'title':mages[0],'herf':herf[0]}
    # json.dumps({'title':mages[0],'herf':herf}, encoding='UTF-8', ensure_ascii=False)


def  getHtmlvalue(html):
#https://www.cnblogs.com/hhh5460/p/5079465.html
    con = etree.HTML(html)
    # print(etree.tostring(con))
    value =  con.xpath('//input/@value')
    return value[0]
booklist = []    
def init():
    dataobj=httprequest(1)
    applyData(dataobj)
    totalNum = dataobj['iTotalRecords']
    totalPage = totalNum//100
    if(totalNum%100 > 0):
        totalPage+=1
    for num in range(2,totalPage+1):
        applyData(httprequest(num))


t = time.time()
uuid = int(t)
results=mysqlspi.query_repeat()
def applyData(data):
    for test in data["aaData"]:
        global uuid
        uuid +=1
        html2=re.sub('[\r\n\t]', '', test[1])
        html2.replace("\\","")
        dictobj = lxmlHtml(html2)
        titlestr=dictobj['title']
        ctherf=dictobj['herf']
        formattype="mobi"
        if(titlestr.endswith('.azw')):
            formattype="azw"
            titlestr=titlestr.replace(".azw","")
        elif(titlestr.endswith('.azw3')):
            formattype="azw3"
            titlestr=titlestr.replace(".azw3","")
        elif(titlestr.endswith('.epub')):
            formattype="epub"
            titlestr=titlestr.replace(".epub","")
        elif(titlestr.endswith('.mobi')):
            formattype="mobi"
            titlestr=titlestr.replace(".mobi","")
        for fileinobj in results:
            # print(titlestr)
            if(fileinobj['title']==titlestr):
                print(titlestr)
                fileinfo ={
                'uuid':str(uuid),
                'bookid':fileinobj['uuid'],
                'ctno':ctherf,
                'formatid':formattype
                }
                flag = mysqlspi.insert_ctinfo(fileinfo)  
                break
        # if(not result):
        #     print("nosearchbook:"+titlestr+"|ctno:"+ctherf+"|format:"+formattype)  
        # else:
        #     fileinfo ={
        #         'uuid':str(uuid),
        #         'bookid':result['uuid'],
        #         'ctno':ctherf,
        #         'formatid':formattype
        #         }
        #     flag = mysqlspi.insert_ctinfo(fileinfo)  
              



init()        
def init2():
    with open("./book.json",'r') as load_f:
        load_list = json.load(load_f)
        print(len(load_list))
        for book in load_list:
            print(json.dumps(book, encoding='UTF-8', ensure_ascii=False))

        

