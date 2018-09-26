#coding=utf-8
import sys
sys.path.append('../')
import tornado.ioloop
import tornado.web
import http_interface
import random
import os
import http_interface
from config import config
import time
from multiprocessing.dummy import Pool


# settings = {
#         "cookie_secret": str(random.random()),
#         "login_url": "/login",
#         "static_path": os.path.join(os.path.dirname('../'), "static"),
#         "template_path":os.path.join(os.path.dirname('../'), "webpage")
# }



# application = tornado.web.Application([

#     ("/", http_interface.main),
#     ("/login", http_interface.login),
#     ('/add_admin',http_interface.add_admin),
#     ('/admin_center',http_interface.open_admin_center),
#     ('/refresh_admin',http_interface.refresh_admin_center),
#     ('/admin_list',http_interface.get_admin_list),
#     ('/data_search',http_interface.data_search),
#     ('/announcement',http_interface.announcement),
#     ('/refresh_announcement',http_interface.refresh_announcement),
#     ('/get_announcement',http_interface.get_announcement)
    
#     ], **settings) 
# # 接口规则路由表
def run(a):
    if a == 1:
        
        http_interface.application_1.listen(config.port,'0.0.0.0')
        print('running on port',config.port)
        tornado.ioloop.IOLoop.instance().start()
        # except Exception as e:
        #     print(str(e))
        #     print('restarting...',config.port)
        #     time.sleep(1)

    else:
        # while 1:
        #     try:
        http_interface.application_2.listen(8654,'0.0.0.0')
        print('running on port',8654)
        tornado.ioloop.IOLoop.instance().start()
            # except Exception as e:
            #     print(str(e))
            #     print('restarting...',8654)
            #     time.sleep(1)



    
Pool().map(run,[1,2])
    

