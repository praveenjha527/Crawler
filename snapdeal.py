import xlrd
import json
import pymongo
from pymongo import *
import time
import os

client = MongoClient('mongodb://localhost:27017/')
db=client.urlsdata

collection=db.inputurls

wb=xlrd.open_workbook("snap.xlsx")

url=wb.sheet_by_index(0)

row=url.nrows

li=[]

for i in range(row):
    dat=url.row_values(i)
    li.append(dat)

sd_url=[]
for j in li:
	dic={'id':j[0],'url':j[1],'netloc':'snapdeal.com'}
	flipkart_url.append(dic)

collection.insert_many(sd_url)