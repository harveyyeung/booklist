# -*- coding:utf-8 -*-
#!/usr/bin/env python
import pymysql
def connect_db():
    return pymysql.connect(host='10.160.59.222',
                           port=3306,
                           user='root',
                           password='tuscloud',
                           database='tusai',
                           charset='utf8')

def query_user(username,password):

    conn = connect_db()
    cursor = conn.cursor()
    #执行参数化查询
    row_count=cursor.execute("select username,role from USER where username=%s and password=%s",(username,password))
    row_1 = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    if row_1:
        return { 
        "username": row_1[0],
        "role": row_1[1]
        }
    else:
        return None     



def query_report_by_userid(userid,pageNum):

    conn = connect_db()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    #执行参数化查询
    row_count=cursor.execute("""select uuid, check_id as checkId, user_id  as userId, hospital_id as hosptitalId, department, position, report_doctor as reportDoctor, DATE_FORMAT(report_date,'%%Y-%%m-%%d %%T') as reportDate, audit_doctor as auditDoctor, DATE_FORMAT(audit_date,'%%Y-%%m-%%d %%T') as auditDate, image_id as imageId, image_total as imageTotal, DATE_FORMAT(create_date,'%%Y-%%m-%%d %%T') as createDate, DATE_FORMAT(check_date,'%%Y-%%m-%%d %%T') as checkDate, DATE_FORMAT(update_date,'%%Y-%%m-%%d %%T')  as updateDate, type, thumb_img as thumbImg, status ,description  from report where user_id=%s and status=1""",(userid))
    results = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return { 
        "pageSize":15,
        "pageNum":pageNum,
        "total": row_count,
        "list": results
    }   
