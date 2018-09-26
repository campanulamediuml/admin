import sys
sys.path.append('../')
import tornado.ioloop
import tornado.web
from common import methods
import pymysql
import json
import server_features
import http_interface
import random
import time

def get_income(invite_id):
    conn,cursor = methods.db_connection()
    sql = 'SELECT income from invitation where invite_id = %s'%invite_id
    cursor.execute(sql)
    income_list = cursor.fetchall()

    if len(income_list) == 0:
        result = 0

    else:
        result = 0
        for i in income_list:
            result += i[0]

    conn.close()
    return result
    # 查找赚了多少钱



def create_i_code():
    seed = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    i_code = ''
    for i in range(0,6):
        i_code += random.choice(seed)
    return i_code
    # 生成邀请码

class business_admin(tornado.web.RequestHandler):
    def get(self):
        try:
            user_token = self.get_secure_cookie("user").decode('utf-8')
            user_token = json.loads(user_token)
            username = user_token['username']
            self.render('business_admin.html')
            return

        except Exception as e:
            methods.log(str(e))
            self.render('login.html')
            return
        #访问公告页面

class create_code(tornado.web.RequestHandler):
    def post(self):
        request_content = json.loads(self.request.body)
        invite_comment = request_content['comment']

        invite_comment = json.dumps(invite_comment).replace('\\','\\\\').replace('"','\\"')
        # 格式化处理方便存入数据库

        conn,cursor = methods.db_connection()
        sql = 'SELECT invite_code from invitation_code'
        cursor.execute(sql)
        invite_code_list = cursor.fetchall()
        if len(invite_code_list) == 0:
            invite_code = create_i_code()
        # 查找邀请码，看看是否存在

        else:
            code_list = []
            for i in invite_code_list:
                code_list.append(i[0])

            while 1:
                invite_code = create_i_code()
                if invite_code in code_list:
                    continue
                else:
                    break
        # 避免重复

        sql = 'INSERT into invitation_code(comment,invite_code) VALUES("%s","%s")'%(invite_comment,invite_code)
        cursor.execute(sql)
        conn.commit()
        conn.close()
        # 插入邀请码
        
        result = {'status_code':0,'comment':request_content['comment'],'invite_code':invite_code}
        self.write(json.dumps(result))
        return

class code_list(tornado.web.RequestHandler):
    def get(self):
        conn,cursor = methods.db_connection()
        sql = 'SELECT comment,invite_code,income_take,id from invitation_code'
        cursor.execute(sql)
        invite_code_list = cursor.fetchall()
        if len(invite_code_list) == 0:
            result =  {'status_code':1}
            # 如果没有邀请码
        else:
            code_list = []
            for i in invite_code_list:
                content = {'code':i[1],'comment':json.loads(i[0])}

                if content['comment'] == '':
                    content['comment'] = 'N/A'

                content['income'] = get_income(i[-1])
                content['take'] = content['income'] - i[2]
                code_list.append(content)

            result = {
                'status_code':0,
                'content':code_list
            }
        conn.close()
        # 返回邀请码相关信息
        self.write(json.dumps(result))

        return


class search_code(tornado.web.RequestHandler):
    def post(self):
        request_content = json.loads(self.request.body)
        code = request_content['code']

        conn,cursor = methods.db_connection()
        sql = 'SELECT comment,invite_code,income_take,id from invitation_code where invite_code = "%s"'%code.upper()
        cursor.execute(sql)
        invite_code_list = cursor.fetchall()
        if len(invite_code_list) == 0:
            result =  {'status_code':1}
        # 乱输邀请码的话去死吧
        else:
            i = invite_code_list[0]
            code_list = []
            content = {'code':i[1],'comment':json.loads(i[0])}
            if content['comment'] == '':
                content['comment'] = 'N/A'
            content['income'] = get_income(i[-1])
            content['take'] = content['income'] - i[2]
            content['status_code'] = 0

            result = content

        conn.close()
        self.write(json.dumps(result))

        return


class take_money(tornado.web.RequestHandler):
    def post(self):
        try:
            user_token = self.get_secure_cookie("user").decode('utf-8')
            user_token = json.loads(user_token)
            username = user_token['username']
        except:
            self.render('login.html')
            return
        # 没登录不能用

        try:
            conn,cursor = methods.db_connection()
            sql = 'SELECT id from user_admin where user = "%s"'%username
            cursor.execute(sql)
            admin_id = cursor.fetchall()[0][0]
            # 查询进行操作的人的id

            request_content = json.loads(self.request.body)
            code = request_content['code']
            money = float(request_content['money'])
            if money < 0:
                result =  {'status_code':-1}
                # 钱不够就别提现了
            else:


                sql = 'SELECT id,income_take from invitation_code where invite_code = "%s"'%code.upper()
                cursor.execute(sql)
                invite_code_list = cursor.fetchall()
                if len(invite_code_list) == 0:
                    result =  {'status_code':1}
                # 乱输邀请码去死好不好


                else:
                    user_id = invite_code_list[0][0]
                    take_money = get_income(user_id) - money - invite_code_list[0][1]
                    if take_money < 0:
                        result =  {'status_code':65536}
                    # 什么？你想输入一个负数来加钱？想多了！
                    else:
                        income_take = money + invite_code_list[0][1]
                        # 更新提现总金额
                        time_now = int(time.time())
                        sql = 'UPDATE invitation_code SET income_take = %s where id = %s'%(income_take,user_id)

                        cursor.execute(sql)
                        sql = 'INSERT INTO money_take_record(user_id,admin_id,time,money) VALUES(%s,%s,%s,%s)'%(user_id,admin_id,time_now,money)
                        cursor.execute(sql)
                        # 插入提现记录
                        conn.commit()
                        result = {'status_code':0}
        except Exception as e:
            print(str(e))
            result = {'status_code':1}

        conn.close()
        self.write(json.dumps(result))


















            




