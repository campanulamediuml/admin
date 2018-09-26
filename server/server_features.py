#coding=utf-8
import sys
sys.path.append('../')
from common import methods
import json
import time

def find_user(username,password):
    user_token_pair = (username,password)
    user_params = methods.search(('user','passwd'),'user_admin',{'user':username,'passwd':password})
    #拼接搜索方法进行搜索
    if user_token_pair in user_params:
        return 0
    else:
        return 1
    # 查找用户，认证登录内容

def add_admin(username,add_admin_tuple):
    power = methods.search(('power',),'user_admin',{'user':username})[0][0]
    # 搜索权限
    if power[6] == '1':#这里添加其他权限，0是超级管理员
        if if_user_in(add_admin_tuple[0]) == 0:#先判定表中是否存在用户
            result = methods.insert('user_admin',('user','passwd','power'),(add_admin_tuple[0],add_admin_tuple[1],'0000000'))
            if result == 0:
                return 0
                # 用户不存在，权限合适，写入成功
            else:
                methods.log('没写成功')
        else:
            return -1
            # 用户存在，权限合适，无法写入
    else:
        return 1
        # 权限不足，拒绝写入


def if_user_in(username):
    user_info = methods.search(('*',),'user_admin',{'user':username})
    if len(user_info) == 0:
        return 0
    else:
        return 1
    #查询表中是否存在某个用户

def find_user_accessment(username):
    power = methods.search(('power',),'user_admin',{'user':username})
    # print(power)
    # 调取用户权限，如果用户权限中访问权限为1，则返回成功
    if len(power) == 0:
        methods.log('压根就没找到这个用户啊')
        # 没找到就写入日志
    else:
        if power[0][0][6] == '1':
            # 判断权限
            return 0
        else:
            return 1

def get_admin_list():
    admins = methods.search(('user','power','isroot'),'user_admin',{})
    admin_list = []
    for i in admins:
        if int(i[2]) != 1:
            admin_list.append({'username':i[0],'power':i[1]})
    return admin_list
    # 获取全部管理员账号列表

def refresh_power(request_content):
    result = 0
    for i in request_content:
        result += methods.update('user_admin',{'power':i['power']},{'user':i['username']})
    if result != 0:
        methods.log('部分更新完毕，',result,'条更新失败')
    new_list = get_admin_list()
    return new_list
    #刷新权限列表


def check_announcement_power(username):
    power = methods.search(('power',),'user_admin',{'user':username})
    if power[0][0][5] == '1':
        return 0
    else:
        return 1
    #判断写公告的权限

def read_announcement():
    announcement = json.loads(open('announcement.txt').read())
    # announcement = methods.search(('code','value'),'config',{'array_code':'announcement'})
    # announcement = announcement[0][1]
    return announcement


def write_announcement(content):
    # result = methods.update('config',{'value':content},{'array_code':'announcement'})
    open('announcement.txt','w').write(json.dumps(content))
    result = 0
    return result


def write_broadcast(content):
    conn,cursor = methods.db_connection()
    content_json = json.dumps(content['content']).replace('\\','\\\\').replace('"','\\"')
    sql = 'INSERT INTO broad_cast (content,ctime,repeat_time,broadcast_time) VALUES ("%s",%s,%s,%s)'%(content_json,int(time.time()),int(content['repeat']),int(time.time())+int(content['broadcast_time']))
    print(sql)
    cursor.execute(sql)
    conn.commit()
    conn.close()

    return 0


def get_broadcast():
    conn,cursor = methods.db_connection()
    sql = 'SELECT content,repeat_time,ctime,broadcast_time from broad_cast'
    cursor.execute(sql)
    result = cursor.fetchall()
    result = result[-1]

    content = {
        'content':json.loads(result[0]),
        'repeat_time':result[1],
        'broadcast_time':result[3]-result[2]
    }
    return content

def online_people():
    result = {}

    conn,cursor = methods.db_connection()
    sql = 'SELECT id from user where is_online = 1'
    cursor.execute(sql)
    online_people = cursor.fetchall()
    result['online_people'] = len(online_people)


    sql = 'SELECT last_room_id from user where last_room_id != 0'
    cursor.execute(sql)
    online_room = cursor.fetchall()
    if len(online_room) != 0:
        result['online_room'] = len(set(list(online_room)))
    else:
        result['online_room'] = 0

    return result




















