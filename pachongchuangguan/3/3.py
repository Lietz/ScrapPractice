import requests
import re
from bs4 import BeautifulSoup



startUrl="http://www.heibanke.com/lesson/crawler_ex02/"
head={
'Host': 'www.heibanke.com',
'Connection': 'keep-alive',
'Content-Length': '75',
'Pragma':' no-cache',
'Cache-Control': 'no-cache',
'Origin': 'http://www.heibanke.com',
'Upgrade-Insecure-Requests':'' '1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
'Content-Type':' application/x-www-form-urlencoded',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Referer':' http://www.heibanke.com/lesson/crawler_ex01/',
'Accept-Encoding':'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
'Cookie': 'csrftoken=xuuZERZQFb9RvCB6WYH17Ha3BX50eIjt&username=cj&password=1;Hm_lvt_74e694103cf02b31b28db0a346da0b6b=1494650354;Hm_lpvt_74e694103cf02b31b28db0a346da0b6b=1494655610',
'csrfmiddlewaretoken':'xuuZERZQFb9RvCB6WYH17Ha3BX50eIjt&username=cj&password=0'
} #请求头
form={              #提交的表单
'csrfmiddlewaretoken':'haIy9hcxh4d8fx3NMgYjjWB319l15l6d',
'username':'cj',
'password':'0'
}
cookies=dict(sessionid='g9fjnvrz2h5uys62tge5dnj9rhzgs0kt',csrftoken='haIy9hcxh4d8fx3NMgYjjWB319l15l6d',
             Hm_lvt_74e694103cf02b31b28db0a346da0b6b='1494660837',Hm_lpvt_74e694103cf02b31b28db0a346da0b6b='1494661035')

# Cookie:sessionid=g9fjnvrz2h5uys62tge5dnj9rhzgs0kt;
# csrftoken=haIy9hcxh4d8fx3NMgYjjWB319l15l6d;
# Hm_lvt_74e694103cf02b31b28db0a346da0b6b=1494660837;
# Hm_lpvt_74e694103cf02b31b28db0a346da0b6b=1494661035
# csrfmiddlewaretoken:haIy9hcxh4d8fx3NMgYjjWB319l15l6d
# username:aaa
# password:1

#r = requests.post(startUrl, data=form,cookies=cookies)
def trypage(form):
    r = requests.post(startUrl, data=form, cookies=cookies)
   # r = requests.post(startUrl, data=form)# 提交用户名密码表单
    soup = BeautifulSoup(r.text, "lxml")
   # print(soup.text)
    sentence = soup.find("h3").text
  #  print(sentence)
    return sentence
def findpass():
    for i in range(0,30):
        form["password"]=str(i)   # 定义在外面，会被修改
        print(i)
        trypage(form)
        if trypage(form)!='您输入的密码错误, 请重新输入':
            print("密码是:" + str(i))
            break



