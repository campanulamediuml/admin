#coding=utf-8
import sys
sys.path.append('../')
import tornado.ioloop
import tornado.web
from common import methods
import pymysql
import json
import server_features
import random
import os
from login import login
from data_search import data_search
from data_search import online_people
from announcement import announcement
from announcement import refresh_announcement
from announcement import get_announcement
from announcement import send_broadcast
from announcement import get_broadcast
from admin import add_admin
from admin import open_admin_center
from admin import refresh_admin_center
from admin import get_admin_list
from business_admin import business_admin
from business_admin import create_code
from business_admin import code_list
from business_admin import search_code
from business_admin import take_money
from invitation import invitation
from invitation import invitation_detail
from invitation import is_user

class base_handler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class main(base_handler):
    @tornado.web.authenticated
    def get(self):
        self.render('index.html')
    # 主页登录



settings = {
        "cookie_secret": str(random.random()),
        "login_url": "/login",
        "static_path": os.path.join(os.path.dirname('../'), "static"),
        "template_path":os.path.join(os.path.dirname('../'), "webpage")
}



application_1 = tornado.web.Application([

    ("/", main),
    ("/login", login),
    ('/data_search',data_search),
    ('/announcement',announcement),
    ('/business_admin',business_admin),
    
    ('/admin_center',open_admin_center),
    ('/refresh_admin',refresh_admin_center),
    ('/admin_list',get_admin_list),
    ('/refresh_announcement',refresh_announcement),
    ('/get_announcement',get_announcement),
    ('/send_broadcast',send_broadcast),
    ('/get_broadcast',get_broadcast),
    ('/online_people',online_people),
    ('/add_admin',add_admin),
    ('/create_code',create_code),
    ('/code_list',code_list),
    ('/search_code',search_code),
    ('/take_money',take_money),
    
    
    ], **settings) 


application_2 = tornado.web.Application([

    ('/invitation',invitation),
    ('/invitation_detail',invitation_detail),
    ('/is_user',is_user),
    
    ], **settings) 
# 接口规则路由表














        




        


