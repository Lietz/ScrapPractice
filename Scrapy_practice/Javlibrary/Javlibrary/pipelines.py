# -*- coding: utf-8 -*-
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import os
#from Javlibrary.settings import IMAGES_STORE  #能用，但我手动设置重命名了

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class JavlibraryPipeline(object):
#     def process_item(self, item, spider):
#         return item
# from Pachong.Scrapy_practice.Javlibrary.Javlibrary import settings


class MyImagesPipeline(ImagesPipeline):

    # def process_item(self, item, spider):
    #     dir_path='%s/%s'%(settings.IMAGES_STORE,spider.name)
    #     print('dir_path',dir_path)
    #     if not os.path.exists(dir_path):
    #         os.makedirs(dir_path)
    #     for image_url in item['image_urls']:
    #         list_name=image_url.split('/')
    #         file_name=list_name[len(list_name)-1]
    #         print('filename',file_name)
    #         file_path='%s/%s'%(dir_path,file_name)
    #         print('file_path',file_path)
    #         if os.path.exists(file_name):
    #             continue
    #         with open(file_path,'wb') as file_writer:
    #             conn=urllib.urlopen(image_url)
    #             file_writer.write(conn.read())
    #         file_writer.close()
    #     return item

    # def process_item(self, item, spider):
    #     if len(item['download_urls'])== 0:
    #         raise DropItem("No download_url found")
    #     return item

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):

        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        print(image_paths)
        print(item['image_paths'])
        if item['image_paths']:
            newname=item['image_urls'][0].split('/')[-1]
            os.rename('F:\CJ\Codes\python\Pachong\Scrapy_practice\Javlibrary\pic\\'
                      +image_paths[0],'F:\CJ\Codes\python\Pachong\Scrapy_practice\Javlibrary\pic\\full\\'+newname)  #\f 转义
        return item
