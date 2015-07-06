import xlrd
import json
import pymongo
from pymongo import *
import time
import os
import redis

class RedisQueue(object):
    """Simple Queue with Redis Backend"""
    def __init__(self, name, namespace='queue', **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.__db= redis.Redis(**redis_kwargs)
        self.key = '%s:%s' %(namespace, name)

    def qsize(self):
        """Return the approximate size of the queue."""
        return self.__db.llen(self.key)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0

    def put(self, item):
        """Put item into the queue."""
        self.__db.rpush(self.key, item)

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue. 

        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)

        if item:
            item = item[1]
        return item

    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)

client = MongoClient('mongodb://localhost:27017/')
db=client.urlsdata
flipkart_queue=RedisQueue('flipkart_coupons_queue')

collection=db.inputurls

wb=xlrd.open_workbook("flip.xlsx")

url=wb.sheet_by_index(0)

row=url.nrows

li=[]

for i in range(row):
    dat=url.row_values(i)
    li.append(dat)

flipkart_url=[]
for j in li:
	dic={'id':j[0],'url':j[1],'netloc':'flipkart.com'}
	flipkart_queue.put(j[0])
	flipkart_url.append(dic)

collection.insert_many(flipkart_url)
