# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MovieCrawlerPipeline(object):
    def process_item(self, item, spider):
        with open("meiju.txt",'a',encoding="utf-8") as f:
            f.write(item["name"].encode('utf-8').decode('utf-8') + "\n")
