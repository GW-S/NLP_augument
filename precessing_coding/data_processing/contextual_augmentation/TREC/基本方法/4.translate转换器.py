# author:sheng.Gw
# -*- coding: utf-8 -*-
# @Date :  2019/5/10

"""
将原始数据转化，转为translate版本的，适合代码跑的数据

目标格式要求为：label content
"""
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

origion_data = pd.read_csv('TREC_train.csv')

print(origion_data.head())

with open('TREC_train_translate.txt','w+') as fp:
    for index,each in origion_data.iterrows():
        label            = each['label']
        translate_result = each['translate_result']
        the_line = str(label) + ' ' + str(translate_result) +'\n'
        print(the_line)
        fp.writelines(the_line)