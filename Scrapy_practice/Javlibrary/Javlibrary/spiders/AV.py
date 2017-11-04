# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup
import re
from Javlibrary.items import JavlibraryItem ##########可以用




#from Pachong.Scrapy_practice.Javlibrary.Javlibrary.pipelines import MyImagesPipeline






class AvSpider(CrawlSpider):
    name = 'AV'
    allowed_domains = ['www.javlibrary.com']
    start_urls = ['http://www.javlibrary.com/cn/']

    rules = (
        #Rule(LinkExtractor(allow='/cn/'),follow=True),
        Rule(LinkExtractor(allow=r'\?v=javli.....'), callback='parse_item',follow=True),
    )




    def parse_item(self, response):
        soup=BeautifulSoup(response.text,'lxml')
        #print(soup.text)

        i = JavlibraryItem()

        i['id']=soup.find('td',class_='text')


        # b = soup.find(id='video_jacket').find('img')['src']

        i['image_urls']=[soup.find(id='video_jacket').find('img')['src']]   #返回列表
        #a = soup.find_all('textarea')
        downloadurls=[]
        for url in soup.find_all('textarea'):
           # c=url.string
            d = re.findall(r"http://.*?\]", url.string)[0].strip(']')
            downloadurls.append(d)
        i['download_urls']=downloadurls
     #   print(i[''])
#  redirect.php\?url.*
        #print(i['id'])
        #i['cover']=
        #i['comments']=soup.find_all('div',class_='text',style='width:807px;')
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
