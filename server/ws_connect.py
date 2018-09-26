from ws4py.client.threadedclient import WebSocketClient
from threading import Timer,Thread
import json
import time

SERVER_URL = 'ws://127.0.0.1:9527/socket.io/?EIO=3&transport=websocket'


class DummyClient(WebSocketClient):
    def opened(self):
        self.send('2') #发送请求数据格式
        print('opening')

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

#服务器返回消息
    def received_message(self, m):
        if str(m) != '3':
            print('recv:',m)
        pass
        
class WS_connect(object):
    def __init__(self):
        self.ws = DummyClient(SERVER_URL)
        self.ws.connect()  
        
    # def heart_beat(self):
    #     self.ws.send('2')
    #     self.ws.send('42'+json.dumps(['game_ping']))
    #     # print('send_2')
        # t = Timer(3,self.heart_beat)
        # t.start()

    # def connect_broad_cast(self):
    #     # while 1:
    #         # try:
    #     self.ws = DummyClient(SERVER_URL)
    #     self.ws.connect()
    #     print('done!')
    #     self.heart_beat()
    #     self.ws.run_forever()
    #     # break
        # heart_beat(ws)
    # except Exception as e:
        # self.ws.close() 
        # print(e)
        # time.sleep(5)
                # continue

    def send_from_client(self,content):
        self.ws.send(content)
        self.ws.send('42'+json.dumps(['disconnect']))

    
