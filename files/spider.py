# -*- coding: utf-8 -*-
import scrapy
import pymysql
import json
import os

from $PROJECT_NAME$.items import Scrapy$CLASS_NAME$Item

# Load conf
cur_dir = os.path.dirname((os.path.abspath(__file__)))
par_dir = os.path.join(cur_dir,  os.pardir)
conf_path = os.path.join(par_dir, 'conf.json')
f = open(conf_path, 'r')
conf = json.load(f)
f.close()

class Spider$CLASS_NAME$Spider(scrapy.Spider):
    name = '$SPIDER_NAME$'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']
    custom_settings = {
        #'USER_AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0',
        #'CONCURRENT_REQUESTS': 1,
        #'DOWNLOAD_DELAY': 1,
        'LOG_LEVEL': conf['log']['level'],
        'ITEM_PIPELINES': {
			'$PROJECT_NAME$.pipelines.Scrapy$CLASS_NAME$Pipeline': 300
		}
    }

    def parse(self, response):
        # EDIT code here
        pass
