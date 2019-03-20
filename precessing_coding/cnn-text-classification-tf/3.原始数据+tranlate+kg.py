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
from kg_tools.KG_and_tools import ruler

"""
先进行百度翻译，再进行KG实体替换，最后生成相应的结果
"""

"""百度翻译到KG的转化"""
def KG_transform(file_list):
    # 对该部分进行KG；
    change_number = 0
    generate_Set = []

    for index, each_rows in enumerate(file_list):
        plainstring1 = each_rows.strip()
        # 有这个try的原因是，如果第一个没有verb的话，就会报错，似乎对方是默认第一个是主语的
        all_result = parse_pos_only_NOUN(plainstring1, ruler)
        #logger.debug("this index{}".format(index) + "is worng")
        if len(all_result) == 0:
            print("KG_transform have something wrong!")
        else:
            for eachline in all_result:
                generate_Set.append(eachline)
                change_number = change_number + 1
    print('最后成功生成的KG句子的数量',change_number)
    return generate_Set

with open('/Users/sheng/Desktop/augument_paper/test_coding/cnn-text-classification-tf/原始数据+translate/rt-polarity-train.neg') as fp:
    translate_lines = fp.readlines()
kg_lines_neg = KG_transform(translate_lines)

with open('/Users/sheng/Desktop/augument_paper/test_coding/cnn-text-classification-tf/原始数据+translate/rt-polarity-train.pos') as fp:
    translate_lines = fp.readlines()
kg_lines_pos = KG_transform(translate_lines)
print(len(kg_lines_neg),len(kg_lines_pos))



"""调整两者的比例"""
if len(kg_lines_neg) < len(kg_lines_pos):
    import random
    gen_len = len(kg_lines_neg)
    kg_now = random.sample( kg_lines_pos ,gen_len)
    with open('/Users/sheng/Desktop/augument_paper/test_coding/cnn-text-classification-tf/原始数据+translate+KG/rt-polarity_train.pos', 'w') as fp:
        for each in kg_now:
            fp.writelines(each + '\n')
    with open('/Users/sheng/Desktop/augument_paper/test_coding/cnn-text-classification-tf/原始数据+translate+KG/rt-polarity_train.neg', 'w') as fp:
        for each in kg_lines_neg:
            fp.writelines(each + '\n')
else:
    import random
    gen_len = len(kg_lines_pos)
    kg_now = random.sample( kg_lines_neg ,gen_len)

    with open('/Users/sheng/Desktop/augument_paper/test_coding/cnn-text-classification-tf/原始数据+translate+KG/rt-polarity_train.neg', 'w') as fp:
        for each in kg_now:
            fp.writelines(each + '\n')
    with open('/Users/sheng/Desktop/augument_paper/test_coding/cnn-text-classification-tf/原始数据+translate+KG/rt-polarity_train.pos', 'w') as fp:
        for each in kg_lines_pos:
            fp.writelines(each + '\n')

# 34931 36653