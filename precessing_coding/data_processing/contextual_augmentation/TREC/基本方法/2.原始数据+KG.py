# author:sheng.Gw
# -*- coding: utf-8 -*-
# @Date :  2019/4/4
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

from kg_tools.KG_and_tools import parse_pos_only_NOUN
from kg_tools.KG_and_tools import ruler # 上义词和同义词
def KG_transform(file_list):
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
                generate_Set.append(eachline)
                change_number = change_number + 1
    print('最后成功生成的KG句子的数量',change_number)
    return generate_Set




file_path = '/Users/sheng/PycharmProjects/contextual_augmentation/raw_content/TREC.train'
with open(file_path, 'r') as fp:
    file_list = fp.readlines()

file_list = KG_transform(file_list)

with open('./TREC_train_kg.txt','w+') as fp:
    for each in file_list:
        fp.writelines(each + '\n')

# 最后成功生成的KG句子的数量 18432