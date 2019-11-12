# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import os
import json

# Load conf
cur_dir = os.path.dirname((os.path.abspath(__file__)))
conf_path = os.path.join(cur_dir, 'conf.json')
f = open(conf_path, 'r')
conf = json.load(f)
f.close()

class Scrapy$CLASS_NAME$Pipeline(object):
    def process_item(self, item, spider):
        # EDIT code here
        """
        # Simple example
        params = (item['name'], item['email'], item['age'])
        self.cursor.execute("INSERT INTO example (name, email, age) VALUES (%s, %s, %s, %s)", params) 
        """
        return item


    def open_spider(self, spider):
        self.connection = pymysql.connect(host=conf['mysql']['host'], user=conf['mysql']['user'], passwd=conf['mysql']['passwd'],db=conf['mysql']['db'], charset='utf8', autocommit=True)
        self.cursor = self.connection.cursor()


    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()