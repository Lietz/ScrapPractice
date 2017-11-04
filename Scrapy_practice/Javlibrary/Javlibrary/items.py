# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JavlibraryItem(scrapy.Item):                    ######   Item对象
    # define the fields for your item here like:
    name = scrapy.Field()
    id=scrapy.Field()
    image_urls=scrapy.Field()
    images=scrapy.Field()
    image_paths=scrapy.Field()
    download_urls=scrapy.Field()
   # cover=scrapy.Field()
    comments=scrapy.Field()



    
