
import requests


url = 'http://127.0.0.1:8080/ACK_WX_Notify_Unifie_Order'
s = requests.Session()  


# headers = {'Content-Type':'text/xml'}  
# 

r = s.post(url)
print(r.content)



