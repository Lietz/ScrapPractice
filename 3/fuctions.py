import datetime
import time

import requests
from bs4 import BeautifulSoup
import re
import itertools
#import urllib
import urllib.robotparser as robotparser
import urllib.parse as urlparse
#from multiprocessing import Queue
import csv
import random
import os
import pickle





# #检查网站所用技术
# pip install builtwith
# import builtwith
# builtweth.parse('...')
#寻找网站所有者
#pip install python-whois
#import whois
#print(whois.shois('appspot.com')

#proxies={"http":"http://10.10.1.10:3128",
 #            "https":"http://10.10.1.10:1080"}

# def download(url,num_retries,proxies=None,headers=None):  #下载函数
#
#     print('Downloading:',url)
#     try:
#         r=requests.get(url,proxies=proxies,headers=headers)
#         if r.status_code!=200:
#             r.raise_for_status()
#     except requests.HTTPError as e:
#         print('Download error code:',r.status_code)
#         if num_retries>0:
#             if 500 <=r.status_code<600:    #5xx,服务器错误
#                  return download(url,num_retries-1)
#         r=None
#     return r

# r=download('http://example.webscraping.com/sitemap.xml')
# print(r.text)

def crawl_sitemap(url):  #1，网站地图爬虫
     sitemap=Downloader.download(url).text
     soup=BeautifulSoup(sitemap,'xml')
    # print(soup)
     links=soup.findAll('loc')


     for link in links:

      html=Downloader.download(link.string)   #得到标签里字符串
     return
# crawl_sitemap('http://example.webscraping.com/sitemap.xml')
def crawl_iditer():   #2，id遍历爬虫
    max_errors=5 #最大错误次数
    num_errors=0 #当前错误次数
    for page in itertools.count(1):   #itertools.count 无限迭代
        url='http://example.webscraping.com/view/-%d' % page  #字符串匹配
        html=Downloader.download(url)
        if html is None:
            num_errors+=1
            if num_errors==max_errors:
                break
    else:
        # success-can scrape the result
        num_errors=0

#crawl_iditer()

def link_crawler(seed_url,link_regex=None,delay=5,max_depth=-1,max_urls=-1,user_agent='wswp',headers=None,
                 proxy=None,num_retries=1,scrape_callback=None): #3，链接爬虫
    """Crawl from the given seed URL following links matched by link_regex"""

    # the queue of URL's that still need to be crawled
   ######## crawl_queue=Queue.deque([seed_url]) #deque:双向队列

    # 记录爬过的url和其深度
    seen={seed_url:0}
    rp=get_robots(seed_url)
   # rp=robotparser.RobotFileParser(seed_url)
    throttle=Throttle(delay)
    headers=headers or {}#传值，则等于headers，不传值则等于{}
    crawl_queue=[seed_url]
    num_urls=0
    #seen=set(crawl_queue)#避免重复下载
   # depth=seen[url]
    D=Downloader(delay=delay,user_agent=user_agent,proxies=proxy,num_retries=num_retries,cache=cache)

    if user_agent:
       headers['User-agent']=user_agent
    while crawl_queue:
        url=crawl_queue.pop() #移除最后一个元素，返回元素值
        depth=seen[url]
        #check url passes robots.txt restrictions
        if rp.can_fetch(user_agent,url):
            html=D(url)
          #  throttle.wait(url)
            #html是response对象
          #  html=D(url,num_retries=num_retries,proxies=proxy,headers=headers) # 下载网页
        #    print('htmlresponse',html)
            links=[]
            if scrape_callback:
                links.extend(scrape_callback(url,html) or [])
            depth=seen[url]
            if depth!=max_depth:
                if link_regex:
                    print('linkregex',link_regex)
                    links.extend(link for link in get_links(html.text) if re.match(link_regex,link))
                    print('linksmatched',links)
            # for link in get_links(html): #提取网页中的链接，加入queue
            #     if re.match(link_regex,link):
            #         link=urllib.urlparse.urljoin(seed_url,link ) #url组合

                for link in links:
                    link=normalize(seed_url,link)
                    if link not in seen:
                        #seen.add(link)
                        seen[link]=depth+1
                        if same_domain(seed_url,link):
                            crawl_queue.append(link)
                            print('queueappend',link)
            num_urls+=1
          #  print('numurls',num_urls)
            if num_urls==max_urls:
                break
        else:
            print('Blocked by robots.txt',url)
def get_links(html):
    strhtml=str(html)
    print('strhtml',strhtml)
    # 从网页提取所有链接的正则
    webpage_regex=re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)
    #网页中所有链接的list
    print('links',webpage_regex.findall(strhtml))
    return webpage_regex.findall(strhtml)

# import urllib.robotparser as robotparser
# rp=robotparser.RobotFileParser()
# rp.set_url('http://example.webscraping.com/robots.txt')
# rp.read()
# url='http://example.webscraping.com'
# user_agent='BadCrawler'
# rp.can_fetch(user_agent,url)
# user_agent='GoodCrawler'
# rp.can_fetch(user_agent,url)

class Throttle:
    #下载之间延时
    def __init__(self,delay):
        self.delay=delay
        #timestamp of when a domain was last accessed
        self.domains={} #字典{域名：时间}
    def wait(self,url):
        domain=urlparse.urlparse(url).netloc  #地址or域名
        last_accessed=self.domains.get(domain)#得到上次访问时间

        if self.delay>0 and last_accessed is not None:
            sleep_secs=self.delay-(datetime.datetime.now()-last_accessed).seconds# 如果间隔过小则sleep
            if sleep_secs>0:
                time.sleep(sleep_secs)  #sleep,推迟执行
        self.domains[domain]=datetime.datetime.now()#记录域名访问的时间
#
# throttle=Throttle(delay)
# throttle.wait(url)
# result=download(...)

def normalize(seed_url,link):
    #urldefrag:# 将url分解成去掉fragment的新url和去掉的fragment的二元组
    link,_=urlparse.urldefrag(link)  #remove hash to avoid duplicates
    return urlparse.urljoin(seed_url,link)

def get_robots(url):
    rp=robotparser.RobotFileParser()
    rp.set_url(urlparse.urljoin(url,'/robots.txt'))
    rp.read()
    return rp

def same_domain(url1,url2):
    return urlparse.urlparse(url1).netloc==urlparse.urlparse(url2).netloc

# __name__ 是当前模块名，当模块被直接运行时模块名为 __main__ 。这句话的意思就是，
# 当模块被直接运行时，以下代码块将被运行，当模块是被导入时，代码块不被运行。
if __name__ == '__main__':
    link_crawler('http://example.webscraping.com', '/(index|view)', delay=0, num_retries=1, user_agent='BadCrawler')
    link_crawler('http://example.webscraping.com', '/(index|view)', delay=0, num_retries=1, max_depth=1, user_agent='GoodCrawler')
  #  delay = 5, max_depth = -1, max_urls = -1, user_agent = 'wswp', headers = None, proxy = None, num_retries = 1)

# class ScrapeCallback:
#     def __init__(self):
#         self.writer=csv.writer(open('countries.csv'),'w')
#         self.fields=('area', 'population', 'iso', 'country',
#                      'capital', 'continent', 'tld', 'currency_code',
#                      'currency_name', 'phone', 'postal_code_format',
#                      'postal_code_regex', 'languages', 'neighbours')
#         self.writer.writerow(self.fields)
#
#         def __call__(self, url, html):
#             if re.search('/view/', url):
#                 tree = lxml.html.fromstring(html)
#                 row = []
#                 for field in self.fields:
#                     row.append(tree.cssselect('table > tr#places_{}__row > td.w2p_fw'.format(field))[0].text_content())
#                 self.writer.writerow(row)
#
#     if __name__ == '__main__':
#         link_crawler('http://example.webscraping.com/', '/(index|view)', scrape_callback=ScrapeCallback())

class Downloader:
    def __init__(self,delay=5,user_agent='wswp',proxies=None,num_retries=1,cache=None):
        self.throttle=Throttle(delay)
        self.user_agent=user_agent
        self.proxies=proxies
        self.num_retries=num_retries
        self.cache=cache

    def __call__(self, url): #下载前检查缓存
        result=None
        if self.cache:
            try:
                result=self.cache[url]
            except KeyError:
                #url is not available in cache
                pass
            else:
                if self.num_retries>0 and 500<=result['code']<600:
                    #server error so ignore result from cache
                    #and redownload
                    result=None
        if result is None:
            #result was not loaded from cache
            #so still need to download
            self.throttle.wait(url)
            ########
            proxy=random.choice(self.proxies) if self.proxies else None
            ########
            headers={'User-agent':self.user_agent}
            result=self.download(url,headers,proxy,self.num_retries)
            if self.cache:
                #save result to cache
                self.cache[url]=result
        return result['html']

    def download(self,url, num_retries, proxies=None, headers=None,data=None):  # 下载函数

        print('Downloading:', url)
        try:
            r = requests.get(url, data,proxies=proxies, headers=headers,)
            if r.status_code != 200:
                r.raise_for_status()
            html=r.url
            code=r.status_code
        except requests.HTTPError as e:
            print('Download error code:', r.status_code)
            html=''
            if num_retries > 0:
                if 500 <= r.status_code < 600:  # 5xx,服务器错误
                    #return download(url, num_retries - 1)
                    return self._get(url, headers, num_retries - 1)
            r = None
        #return r
        return {'html':html,'code':code}



class DiskCache:
    def __init__(self,cache_dir='cache'):
        self.cache_dir=cache_dir
        self.max_length=max_length

    def url_to_path(self,url):
        # Create file system path for this URL
        components=urlparse.urlsplit(url)
        #append index.html to empty paths
        path=components.path
        if not path:
            path='/index.html'
        elif path.endswith('/'):
            path+='index.html'
        filename=components.netloc+path+components.query
        #replace invalid characters
        filename=re.sub('[^/0-9a-zA-Z\-.,;_ ]','_',filename)
        #restrict maximum number of characters
        filename='/'.join(segment[:255] for segment in filename.split("/"))
        return os.path.join(self.cache_dir,filename)

    def __getitem__(self, url):
        # load data form disk for this URL
        path=self.url_to_path(url)
        if os.path.exists(path):
            with open(path,'rb') as fp:
                return pickle.load(fp)
        else:
            # URL has not yet been cached
            raise KeyError(url+'does not exist')

    def __setitem__(self, url,result):
        """Save data to disk for this URL"""
        path=self.url_to_path(url)
        folder=os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(path,'wb') as fp:
            fp.write(pickle.dumps(result))
