# author:sheng.Gw
# -*- coding: utf-8 -*-
# @Date :  2019/5/24
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

from precessing_coding.kg_tools.KG_and_tools import parse_pos_only_NOUN
from precessing_coding.kg_tools.KG_and_tools import ruler # 上义词和同义词

def KG_transform(file_list,label_result):
    change_number = 0
    generate_Set = []

    for index, each_rows in enumerate(file_list):
        plainstring1 = each_rows.strip()
        # 有这个try的原因是，如果第一个没有verb的话，就会报错，似乎对方是默认第一个是主语的
        all_result = parse_pos_only_NOUN(plainstring1, ruler)
        if len(all_result) == 0:
            print("KG_transform have something wrong!")
        else:
            for eachline in all_result:
                label = lable_result[index]
                eachline = str(label) + ' ' +eachline
                print(eachline)
                generate_Set.append(eachline)
                change_number = change_number + 1
    print('最后成功生成的KG句子的数量',change_number)
    return generate_Set

dataSet = pd.read_csv('./stsa_binary.csv')
translate_result = list(dataSet['translate_result'])
lable_result     = list(dataSet['label'])
kg_result = KG_transform(translate_result,lable_result)

with open('./translate_then_kg.txt','w+') as fp:
    for each in kg_result:
        fp.writelines(each + '\n')

# 最后成功生成的KG句子的数量 44528