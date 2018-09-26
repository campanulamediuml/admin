import sys
sys.path.append('../')
import tornado.ioloop
import tornado.web
from common import methods
import pymysql
import json
import server_features
import http_interface


class data_search(tornado.web.RequestHandler):
    def get(self):
        try:
            user_token = self.get_secure_cookie("user").decode('utf-8')
            user_token = json.loads(user_token)
            username = user_token['username']
            self.render('data_search.html')
            return
        except Exception as e:
            methods.log(str(e))
            self.render('login.html')
            return
        
    # 访问数据查询页面
class online_people(tornado.web.RequestHandler):
    def get(self):
        data = server_features.online_people()
        data['status_code'] = 0
        self.write(json.dumps(data))
        return
        



