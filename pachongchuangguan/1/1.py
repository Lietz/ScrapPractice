import requests
import re
from bs4 import BeautifulSoup



startUrl="http://www.heibanke.com/lesson/crawler_ex00/"

def getNumber(url):
    number=""
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        sentence = soup.find("h3").text
        print(sentence)
       # number = sentence[11:16]
        #你需要在网址后输入数字22213.
      #  re.findall(r"\d+", sentence) >>>>>>>>>['22213']
       # number=re.match('\d+', sentence)  match()方法判断是否匹配，如果匹配成功，返回一个Match对象，否则返回None
        # print(sentence)
        number=re.findall(r"\d+", sentence)[0]
        return number
    except IOError:
        return number

# r=requests.get(startUrl)
# while (getNumber()!=None):

def download(url):
    number=""
    try:
        while True:
            number = getNumber(url+number)
        #    url=url+number
            # page=getNumber(url+getNumber(url))
            # url=url+getNumber(url)
            print("url"+url)
       #     print("number"+number)
    except Exception:
        return number










