import sys
sys.path.append('../')
import tornado.ioloop
import tornado.web
from common import methods
import pymysql
import json
import server_features
import http_interface



class add_admin(tornado.web.RequestHandler):
    def post(self):
        request_content = json.loads(self.request.body)
        # 获取请求身
        user_token = self.get_secure_cookie("user").decode('utf-8')
        user_token = json.loads(user_token)
        username = user_token['username']
        #获取登录的用户的用户名
        
        add_admin_tuple = (request_content["add_admin_name"],methods.get_md5(request_content['add_admin_password']))
        # 拼接要添加的用户信息
        
        status = server_features.add_admin(username,add_admin_tuple)
        if status == 0:
            return_dict = {'status_code':0,'content':'添加用户成功'}
        elif status == 1:
            return_dict = {'status_code':1,'content':'高能瓦斯不足'}
        elif status == -1:
            return_dict = {'status_code':-1,'content':'用户已经存在'}

        self.write(json.dumps(return_dict))

    # 添加后台账号
class open_admin_center(tornado.web.RequestHandler):
    def get(self):
        try:
            user_token = self.get_secure_cookie("user").decode('utf-8')
            user_token = json.loads(user_token)
            username = user_token['username']
            if server_features.find_user_accessment(username) == 0:
                admin_list = server_features.get_admin_list()
                self.render('admin.html')
                # return_dict = {'status_code':0,'content':admin_list}
            else:
                return_dict = {'status_code':1,'content':'高能瓦斯不足'}
                self.write(json.dumps(return_dict))
        except Exception as e:
            methods.log(str(e))
            self.render('login.html')
        
     # 访问管理中心

class get_admin_list(tornado.web.RequestHandler):
    def get(self):
        user_token = self.get_secure_cookie("user").decode('utf-8')
        user_token = json.loads(user_token)
        username = user_token['username']
        if server_features.find_user_accessment(username) == 0:
            admin_list = server_features.get_admin_list()
            # self.write(open('../webpage/admin.html').read())
            return_dict = {'status_code':0,'content':admin_list}  
        else:
            return_dict = {'status_code':1,'content':'高能瓦斯不足'}
        self.write(json.dumps(return_dict))
     # 获取权限列表


class refresh_admin_center(tornado.web.RequestHandler):
    def post(self):
        request_content = json.loads(self.request.body)
        admin_list = server_features.refresh_power(request_content)
        return_dict = {'status_code':0,'content':admin_list}
        self.write(json.dumps(return_dict))