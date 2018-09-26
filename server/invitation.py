import sys
sys.path.append('../')
import tornado.ioloop
import tornado.web
from common import methods
import pymysql
import json
import server_features
import http_interface


def search_detail(invitation_id):
    conn,cursor = methods.db_connection()
    sql = 'SELECT user_id,invite_time from invitation where invite_id = %s'%invitation_id
    cursor.execute(sql)
    invitation_users = cursor.fetchall()
    result = []
    user_id_list = []
    if len(invitation_users) == 0:
        return result
    # 如果这个邀请码没有用户填过
    else:
        for user in invitation_users:
            # 遍历填过这个邀请码的用户
            sql = 'SELECT order_number from order_info where user_id = %s and create_time > %s and status = 2'%(user[0],user[1])
            cursor.execute(sql)
            order_list = cursor.fetchall()
            # 查找对应的结算过的订单
            if len(order_list) == 0:
                continue
            else:
                for order in order_list:
                    good_id = int(order[0].split('_')[-1])
                    good_type = order[0].split('_')[-2]
                    good_time = int(order[0].split('_')[-0])

                    sql = 'SELECT money from %s where id = %s'%('bag_'+good_type,good_id)
                    cursor.execute(sql)
                    money = cursor.fetchall()[0][0]
                    # 查找对应订单的价格

                    sql = 'SELECT uuid from user where id = %s'%user[0]
                    cursor.execute(sql)
                    uuid = cursor.fetchall()[0][0]
                    # 查找对应订单的uuid

                    uuid = str(uuid)[:2]+'****'+str(uuid)[-2:]

                    line = {
                        'uuid':uuid,
                        'money':money,
                        'time':methods.time_to_str(good_time),
                        'good':good_type
                    }
                    # 结果
                    result.append(line)
    conn.close()
    return result

class invitation(tornado.web.RequestHandler):

    def get(self):
        self.render('invitation.html')
        #访问公告页面

class invitation_detail(tornado.web.RequestHandler):
    def post(self):
        request_content = json.loads(self.request.body)
        invitation_code = request_content['invitation_code']


        conn,cursor = methods.db_connection()
        sql = 'SELECT id from invitation_code where invite_code = "%s"'%invitation_code.upper()
        cursor.execute(sql)
        invitation_id = cursor.fetchall()

        result = {}
        if len(invitation_id) == 0:
            result = {'status_code':1}
        else:
            invitation_id = invitation_id[0][0]
            tmp = search_detail(invitation_id)
            result['status_code'] = 0
            result['content'] = tmp

        conn.close()
        if result['status_code'] == 0:
            result['code'] = invitation_code.upper()
            self.set_secure_cookie('user',json.dumps({'code':invitation_code}))
        # 把查询结果储存为cookie

        self.write(json.dumps(result))
        return

class is_user(tornado.web.RequestHandler):
    def get(self):
        try:
            user_token = self.get_secure_cookie("user").decode('utf-8')
            user_token = json.loads(user_token)
            invite_code = user_token['code']
            if invite_code != '':
                result = {'status_code':0,'code':invite_code}
            else:
                result = {'status_code':1}

        except Exception as e:
            print(str(e))
            result = {'status_code':1}
            
        self.write(json.dumps(result))
        return



