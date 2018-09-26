#coding=utf-8
import sys
sys.path.append('../')
import pymysql
from config import db 
import hashlib 
import base64
import time
import datetime


def time_to_str(times):
    date_array = datetime.datetime.utcfromtimestamp(times+(8*3600))
    return date_array.strftime("%Y-%m-%d %H:%M:%S")

def log(content):
    log_content = str(time.asctime( time.localtime(time.time())))+'    '+content+'\n'
    open('../log.log','a').write(log_content)

def get_md5(string):
    md5 = hashlib.md5(string.encode('ascii')).hexdigest()
    return md5
    # 计算md5校验
    # 这里python作为一个弱类型语言的坑就出现了
    # 竟然传入值需要解码成ascii

def db_connection():
    conn = pymysql.connect(host=db.host, port=db.port, user=db.user, passwd=db.passwd, db=db.db, charset=db.charset)
    cursor = conn.cursor()
    return conn,cursor
    # 连接数据库

def search(key_tuple,table,search_dict):
    conn,cursor = db_connection()
    key_words = ','.join(list(key_tuple))
    # 拼接必要的数据搜索条件
    if search_dict != {}:
        params_list = []
        for key in search_dict:
            params_list.append(key+'='+'"'+search_dict[key]+'" ')
        params = 'AND '.join(params_list) 

        select_query = 'SELECT %s FROM %s WHERE %s'%(key_words,table,params)
    else:
        select_query = 'SELECT %s FROM %s'%(key_words,table)
    # print(select_query)
    # 不同条件下不同的搜索语句

    cursor.execute(select_query)
    result = cursor.fetchall()
    # print(result)
    conn.close()
    return result
    #传入元组搜索数据库

def insert(table,params,contents):
    conn,cursor = db_connection()
    params_list = []
    s_list = []
    for i in params:
        params_list.append(i)
        s_list.append('"%s"')
    param_string = ','.join(params_list)
    s_string = ','.join(s_list)
    insert_query = 'INSERT INTO %s(%s) VALUES(%s)'%(table,param_string,s_string)
    insert_query = insert_query%contents
    # 拼接插入语句
    print(insert_query)
    try:
        cursor.execute(insert_query)
        conn.commit()
        result = 0
    except Exception as e:
        log(str(e))
        result = 1
    # 判断是否插入成功 
    conn.close()
    return result

def update(table,params_update,params_need):
    conn,cursor = db_connection()
    for param in params_update:
        refresh = param+'="'+params_update[param]+'"'
    for param in params_need:
        need = param+'="'+params_need[param]+'"'

    # 拼接更新操作语句
    update_params = 'UPDATE %s SET %s WHERE %s'%(table,refresh,need)
    cursor.execute(update_params)
    #更新操作
    conn.commit()
    conn.close()

    return 0





