# author:sheng.Gw
# -*- coding: utf-8 -*-
# @Date :  2019/2/17
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

"""
input:list:str
output：content
"""
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

neg_path = '/Users/sheng/Desktop/augument_paper/test_coding/cnn-text-classification-tf/原始数据/rt-polarity-train.neg'
pos_path = '/Users/sheng/Desktop/augument_paper/test_coding/cnn-text-classification-tf/原始数据/rt-polarity-train.pos'

with open(neg_path) as fp:
    neg_lines = fp.readlines()

with open(pos_path) as fp:
    pos_lines = fp.readlines()

neg_lines = KG_transform(neg_lines)
pos_lines = KG_transform(pos_lines)

with open('/Users/sheng/Desktop/augument_paper/test_coding/cnn-text-classification-tf/原始数据+KG/rt-polarity_train.neg','w+') as fp:
    for each in neg_lines:
        fp.writelines(each + '\n')

with open('/Users/sheng/Desktop/augument_paper/test_coding/cnn-text-classification-tf/原始数据+KG/rt-polarity_train.pos','w+') as fp:
    for each in pos_lines:
        fp.writelines(each + '\n')

###
# pos: 生成了38315条
# neg: 生成了36653条

