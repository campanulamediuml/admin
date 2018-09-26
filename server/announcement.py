import sys
sys.path.append('../')
import tornado.ioloop
import tornado.web
from common import methods
import pymysql
import json
import server_features
import http_interface
from ws_connect import WS_connect

class announcement(tornado.web.RequestHandler):
    def get(self):
        try:
            user_token = self.get_secure_cookie("user").decode('utf-8')
            self.render('announcement.html')
            return

        except Exception as e:
            methods.log(str(e))
            self.render('login.html')
            return
        #访问公告页面

class refresh_announcement(tornado.web.RequestHandler):
    def post(self):
        
        try:
            user_token = self.get_secure_cookie("user").decode('utf-8')
            user_token = json.loads(user_token)
            username = user_token['username']
        except Exception as e:
            methods.log(str(e))
            self.render('login.html')
            return

        if server_features.check_announcement_power(user_token['username']) == 0:
            request_content = json.loads(self.request.body)
            if request_content['content'] != '':
                result = server_features.write_announcement(request_content['content'])
                self.write(json.dumps({'status_code':0,'content':'更新成功'}))
                return
            else:
                self.write(json.dumps({'status_code':-1,'content':'兄弟，没公告啊，别乱点啊'}))
                return

        elif  server_features.check_announcement_power(user_token['username']) == 1:
            self.write(json.dumps({'status_code':1,'content':'需要更多高能瓦斯'}))
            return
        #判断是否有修改公告的权限

    # 更新公告

class get_announcement(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,authorization")
        self.set_header('Access-Control-Allow-Methods', 'POST,GET,PUT,DELETE,OPTIONS')

    def get(self):
        # try:
        # user_token = self.get_secure_cookie("user").decode('utf-8')
        announcement = server_features.read_announcement()
        # print(announcement)
        self.write(json.dumps({'status_code':0,'content':announcement}))
        return
        # except Exception as e:
        #     methods.log(str(e))
        #     self.write(open('../webpage/login.html').read())
    # 读取公告


class send_broadcast(tornado.web.RequestHandler):
    def post(self):
        request_content = json.loads(self.request.body)
        # 获取请求身
        user_token = self.get_secure_cookie("user").decode('utf-8')
        user_token = json.loads(user_token)
        
        broad_cast = request_content
        if broad_cast != '':
            test = server_features.write_broadcast(broad_cast)
            if test == 0:
                connection = WS_connect()
                data = '42'+json.dumps(['REQ_SEND_BROADCAST',{}])
                connection.send_from_client(data)
                self.write(json.dumps({'status_code':0,'content':'广播发送成功'}))
                return 
            else:
                self.write(json.dumps({'status_code':1,'content':'广播发送失败，你是不是在里面乱写了什么'}))
                return 
        else:
            self.write(json.dumps({'status_code':-1,'content':'兄弟，没公告啊，别乱点啊'}))
            return


class get_broadcast(tornado.web.RequestHandler):
    def get(self):
        broad_cast_dict = server_features.get_broadcast()
        broad_cast_dict['status_code'] = 0
        self.write(json.dumps(broad_cast_dict))







