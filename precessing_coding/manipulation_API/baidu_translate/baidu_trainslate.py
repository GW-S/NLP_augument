# author:sheng.Gw
# -*- coding: utf-8 -*-
# @Date :  2018/11/15
import pandas as pd
import numpy as np
import http.client
import hashlib
import json
import urllib
import random

from tqdm import tqdm

pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)


baidu_translate_app_id      = '20181114000234580'
baidu_translate_secret_code = 'YQdKvZ3JpKImLNtZT5M7'

appid = baidu_translate_app_id
secretKey = baidu_translate_secret_code

def baidu_translate(content,from_langu,to_langu):
    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = content
    fromLang = from_langu  # 源语言
    toLang = to_langu  # 翻译后的语言

    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        jsonResponse = response.read().decode("utf-8")  # 获得返回的结果，结果为json格式
        js = json.loads(jsonResponse)  # 将json格式的结果转换字典结构
        dst = str(js["trans_result"][0]["dst"])  # 取得翻译后的文本结果
        return dst # 打印结果
    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()

def translate(trainSet_content_list,from_langu,to_langu):
    giveback = []
    i = 0
    for eachline in tqdm(trainSet_content_list):
        now = baidu_translate(eachline, from_langu, to_langu)
        # 为了解决会出现断点的问题，当出现断点手工进行调整
        i = i + 1
        if now == None:
            print('这是一个错误的行',i,eachline)
            now = "盛国威真的帅"
        giveback.append(now)
    return giveback

if __name__ == '__main__':
    # 进行数据增强操作
    def reinforce_dataSet(trainSet, save):

        trainSet_content_list = []

        all_data = []
        for index, eachrrows in trainSet.iterrows():
            content_list = eval(eachrrows['content'])
            print(type(content_list))
            all_data.append(" ".join(content_list))



        trainSet_content_list = [each.strip() for each in all_data]
        trainSet_content = translate(trainSet_content_list, 'en', 'de')
        trainSet['translate_content'] = translate(trainSet_content, 'de', 'en')
        trainSet.to_csv(save)



    dataSet = pd.read_csv("/Users/sheng/PycharmProjects/Aspect_sentiment_10/Aspect-level-sentiment-master/code/origion_dataSet.csv")
    print(dataSet.head())
    reinforce_dataSet(dataSet, './原始数据的数据增强.csv')



