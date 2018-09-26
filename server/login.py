import sys
sys.path.append('../')
import tornado.ioloop
import tornado.web
from common import methods
import pymysql
import json
import server_features
import http_interface


class login(tornado.web.RequestHandler):
    def get(self):
        try:
            user_token = self.get_secure_cookie("user").decode('utf-8')
            self.render('index.html')
        except Exception as e:
            methods.log(str(e))
            self.render('login.html')
        #如果已经登录，则跳转，如果没登录，那么就跳转到登录页面

    def post(self):

        print(self.request.body)
        
        request_content = json.loads(self.request.body)
        # 获取请求身
        # print(self.request.body)

        username = request_content["username"]
        password = methods.get_md5(request_content['password'])
        # 取得用户名和密码的md5
        if server_features.find_user(username,password) == 0:
            sercure_json = {'username':username,'password':password}
            self.set_secure_cookie("user", json.dumps(sercure_json))
            # print('a user login')
            return_dict = {'status_code':0,'content':'登陆成功'}
        else:
            return_dict = {'status_code':1,'content':'登录失败,用户名或密码不存在'}

        methods.log('有人登陆了,用户名为'+username)
        # print('somebody log in, username = '+username)
        self.write(json.dumps(return_dict))
    # 登录
