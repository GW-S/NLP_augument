# author:sheng.Gw
# -*- coding: utf-8 -*-
# @Date :  2019/3/27

"""处理思想，主要是通过百度翻译，给一个新编号，然后再进行修改翻译"""
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

file_path = '/Users/sheng/PycharmProjects/contextual_augmentation/raw_content/TREC.train'
with open(file_path, 'r') as fp:
    file_list = fp.readlines()

label =[]
sentence = []
for eachline in file_list:
    first  = eachline.strip().split()[0]
    second = " ".join(eachline.strip().split()[1:])
    label.append(first)
    sentence.append(second)
input = pd.DataFrame({'label':label,'sentence':sentence})

# 调用API
from baidu_translate.baidu_trainslate import translate
label    = list(input['label'])
sentence = list(input['sentence'])

trainSet_content = translate(sentence,'en','de')
allline = translate(trainSet_content, 'de', 'en')

input['translate_result'] = allline
print(input['translate_result'][0])

input.to_csv('./TREC_train.csv')