''' datasource: dxy(https://ncov.dxy.cn/ncovh5/view/pneumonia)
    credit: bilibili
    contribution: Mengru Yuan
    contact info: yuanmr@umich.edu
    version: 20220512--v1'''


# 1. 导入相关模块
from cProfile import label
from turtle import home
from xml.dom.minidom import Element
import requests
from bs4 import BeautifulSoup
import re
import json
import csv
import pandas as pd
from datetime import datetime

#2.发送请求，获取首页数据
response = requests.get("https://ncov.dxy.cn/ncovh5/view/pneumonia")
home_page = response.content.decode()

#3.使用BeautifulSoup提取各省市疫情数据
soup = BeautifulSoup(home_page, 'lxml')
script = soup.find(id='fetchRecentStatV2')
text = script.string

#4.使用正则表达式提取json字符串
json_str = re.findall(r'\[.+\]', text)[0]

#5.Json转成python + 数据处理
latest_city_situation = json.loads(json_str)
city_list = []
for each_dict in latest_city_situation:
    for city in each_dict['cities']:
        city_list.append(city)

#6.写进csv
df = pd.DataFrame(city_list)
df1 = df.drop(columns=['notShowCurrentConfirmedCount'])
filename = 'latest_city_situation_' + datetime.today().strftime('%Y%m%d')+'.csv'
df1.to_csv(filename, encoding='utf_8_sig')




