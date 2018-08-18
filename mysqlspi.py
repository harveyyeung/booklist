# -*- coding:utf-8 -*-
#!/usr/bin/env python
import pymysql
import re
def connect_db():
    return pymysql.connect(host='localhost',
                           port=3306,
                           user='booklist',
                           password='booklist!',
                           database='booklist',
                           charset='utf8')


def insert_bookinfo(bookinfo):
    conn = connect_db()
    cursor = conn.cursor()
    #执行参数化查询
    # print(bookinfo)
    # sql = "INSERT INTO bookinfo(uuid,title,author,isbn10,isbn16,author_info,publisher,summary,dbaltid,grade,cotegoryid,image,createtime,status) VALUES ("+str(bookinfo['uuid'])+", "+str(bookinfo['title'])+","+ str(bookinfo['author'])+","+ str(bookinfo['isbn10'])+","+ str(bookinfo['isbn16'])+","+ str(bookinfo['author_info'])+","+ str(bookinfo['publisher'])+","+ str(bookinfo['summary'])+", "+str(bookinfo['dbaltid'])+","+str(bookinfo['grade'])+","+str(bookinfo['cotegoryid'])+","+ str(bookinfo['image'])+","+str(bookinfo['createtime'])+", 1)"
    # print(sql)
    # cursor.execute(sql)
    # print("INSERT INTO bookinfo(uuid,title,author,isbn10,isbn16,author_info,publisher,summary,dbaltid,grade,cotegoryid,image,createtime,status) VALUES ("+bookinfo['uuid']+", "+bookinfo['title']+","+ str(bookinfo['author'])+","+ bookinfo['isbn10']+","+ bookinfo['isbn16']+","+ bookinfo['author_info']+","+ bookinfo['publisher']+","+ bookinfo['summary']+", "+bookinfo['dbaltid']+","+bookinfo['grade']+","+bookinfo['cotegoryid']+","+ bookinfo['image']+","+bookinfo['createtime']+", 1)")
    try:
        cursor.execute("""INSERT INTO bookinfo(uuid,title,author,isbn10,isbn16,author_info,publisher,summary,dbaltid,grade,cotegoryid,image,createtime,status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s, %s, 1)""",(bookinfo['uuid'], bookinfo['title'], bookinfo['author'], bookinfo['isbn10'], bookinfo['isbn16'], bookinfo['author_info'], bookinfo['publisher'], bookinfo['summary'], bookinfo['dbaltid'], bookinfo['grade'],bookinfo['cotegoryid'], bookinfo['image'],bookinfo['createtime']))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except BaseException:
        conn.commit()
        cursor.close()
        conn.close()
        return False



def query_booklist(pageNum,qstr,cotegory):
    conn = connect_db()
    startNum=(pageNum -1 ) *40
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    if not qstr and not cotegory:
    #执行参数化查询
        cursor.execute("select  bookinfo.*,fileinfo.ctno,fileinfo.formatid,total.totalnum from bookinfo,fileinfo,(SELECT count(uuid)  as totalnum from bookinfo where status=1) total where bookinfo.uuid=fileinfo.bookid and bookinfo.status=1 limit "+str(startNum)+",40")
    
    elif  qstr and not cotegory:
        cursor.execute("select  bookinfo.*,fileinfo.ctno,fileinfo.formatid,total.totalnum from bookinfo,fileinfo,(SELECT count(uuid)  as totalnum from bookinfo where status=1 and title like '%"+qstr+"%') total where bookinfo.uuid=fileinfo.bookid and bookinfo.status=1 and bookinfo.title like '%"+qstr+"%' limit "+str(startNum)+",40")   
    
    elif  not qstr and cotegory:
        cursor.execute("select  bookinfo.*,fileinfo.ctno,fileinfo.formatid,total.totalnum from bookinfo,fileinfo,(SELECT count(uuid)  as totalnum from bookinfo where status=1  and cotegoryid = '"+cotegory+"' ) total where bookinfo.uuid=fileinfo.bookid and bookinfo.status=1 and bookinfo.cotegoryid = '"+cotegory+"'  limit "+str(startNum)+",40")
    
    else:
        cursor.execute("select  bookinfo.*,fileinfo.ctno,fileinfo.formatid,total.totalnum from bookinfo,fileinfo,(SELECT count(uuid)  as totalnum from bookinfo where status=1 and title like '%"+qstr+"%'  and cotegoryid = '"+cotegory+"' ) total where bookinfo.uuid=fileinfo.bookid and bookinfo.status=1 and bookinfo.title like '%"+qstr+"%' and bookinfo.cotegoryid = '"+cotegory+"'   limit "+str(startNum)+",40")   
    

    results = cursor.fetchall()
    totalnum=17925
    if(len(results)>0):
        totalnum=results[0]['totalnum']
    
    pagetotal= totalnum // 40
    print(pagetotal)
    if(totalnum % 40 > 0):
        pagetotal+=1 

    conn.commit()
    cursor.close()
    conn.close()
    return { 
        "pageSize":40,
        "pageNum":pageNum,
        "total": pagetotal,
        "list": results
    }   

def query_random():
    conn = connect_db()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    #执行参数化查询
    row_count=cursor.execute("select bookinfo.*,fileinfo.ctno,fileinfo.formatid from bookinfo,fileinfo where  bookinfo.status=1 and bookinfo.uuid=fileinfo.bookid and bookinfo.uuid ORDER BY  RAND() LIMIT 40")
    print(row_count)
    results = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return results



def query_booklistby_title(qstr):
    conn = connect_db()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    row_count = cursor.execute("""select bookinfo.*,fileinfo.ctno,fileinfo.formatid from bookinfo,fileinfo where  bookinfo.uuid=fileinfo.bookid and bookinfo.title like %s""",(qstr))  
    results = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return results


def insert_ctinfo(fileinfo):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""INSERT INTO fileinfo(uuid,bookid,ctno,formatid,status) VALUES (%s, %s, %s, %s, 1)""",(fileinfo['uuid'], fileinfo['bookid'], fileinfo['ctno'], fileinfo['formatid']))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except BaseException:
        print("notinsertbookid:"+fileinfo['bookid']+"   ctno:"+fileinfo['ctno']+"   formatid:"+fileinfo['formatid'])
        conn.commit()
        cursor.close()
        conn.close()
        return False

def query_repeat():
    conn = connect_db()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    #执行参数化查询
    row_count= cursor.execute("SELECT *  FROM booklist.bookinfo where uuid not in(SELECT bookid FROM booklist.fileinfo)")
    results = cursor.fetchall()
    print(row_count)
    conn.commit()
    cursor.close()
    conn.close()
    return results     