# author:sheng.Gw
# -*- coding: utf-8 -*-
# @Date :  2019/5/24
"""说明信息"""




import pandas as pd
import numpy as np
import os

import sys
from os import path
sys.path.append("/".join(path.abspath(__file__).split('/')[0:-3]))

pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

from precessing_coding.kg_tools.KG_and_tools import parse_pos_only_NOUN
from precessing_coding.kg_tools.KG_and_tools import ruler # 上义词和同义词
from precessing_coding.contextual_augmentation.TREC.数据平衡.balance_library  import bucket_balance

def KG_transform_for_balance(file_list):
    """由于分割需要，维持一个索引"""
    change_number = 0
    generate_Set = []
    for index, each_rows in enumerate(file_list):
        plainstring1 = each_rows.strip()
        all_result = parse_pos_only_NOUN(plainstring1, ruler)
        if len(all_result) == 0:
            print("KG_transform have something wrong!")
        else:
            for eachline in all_result:
                eachline = str(index)  +" " + eachline
                generate_Set.append(eachline)
                change_number = change_number + 1
    print('最后成功生成的KG句子的数量',change_number)
    return generate_Set

if __name__ == "__main__":
    """
    arg
    """

    """ 步骤1：用KG_transform_for_balance重新KG句子"""
    translate_KG_list = []
    if os.path.exists('/Users/sheng/Desktop/github/augument_paper/precessing_coding/contextual_augmentation/TREC/数据平衡/store/translate_Kg_list.txt'):
        with open('/Users/sheng/Desktop/github/augument_paper/precessing_coding/contextual_augmentation/TREC/数据平衡/store/translate_Kg_list.txt') as fp:
            translate_KG_list = fp.readlines()
    else:
        file_path = '/Users/sheng/Desktop/github/augument_paper/precessing_coding/contextual_augmentation/TREC/TREC_train.csv'
        dataSet = pd.read_csv(file_path)
        translate_result = dataSet['translate_result']
        translate_label  = dataSet['label']
        translate_temp_list = []
        for item1,item2 in zip(translate_label,translate_result):
            translate_temp_list.append(str(item1)+" "+str(item2))
        translate_KG_list = KG_transform_for_balance(translate_temp_list)
        with open('/Users/sheng/Desktop/github/augument_paper/precessing_coding/contextual_augmentation/TREC/数据平衡/store/translate_Kg_list.txt','w+') as fp:
            for eachline in translate_KG_list:
                eachline += '\n'
                fp.writelines(eachline)
            fp.close()
    """output：  label    belong                             context
                '  0       2342            how did the possession develop in russia and then leave?'"""

    """步骤2： 分析原始的句子"""
    dataSet_origion = pd.read_csv('/Users/sheng/Desktop/github/augument_paper/precessing_coding/contextual_augmentation/TREC/TREC_train.csv')
    dataFrame_origion = dataSet_origion.groupby('label')

    print("""原始数据集中的数据比例""")
    for name, group in dataFrame_origion:
        print(name)
        print(len(group))

    """步骤3： 分析KG后的句子"""
    label  = []
    belong = []
    for index,eachline in enumerate(translate_KG_list):
        label.append(eachline.split()[1])
        belong.append(eachline.split()[0])
    dataSet = pd.DataFrame()
    dataSet['content'] = translate_KG_list
    dataSet['label']   = label
    dataSet['belong']  = belong
    data = dataSet.groupby('label')
    print("""分析KG后的句子比例""")
    for name, group in data:
        print(name)
        print(len(group))

    """步骤4：保持比例进行采样"""
    all_choice_data = bucket_balance(dataSet_origion,dataSet,"label","label","belong")
    print(all_choice_data.head())

    """步骤5：验证最后的采样比例"""
    data = all_choice_data.groupby('label')
    print("""新数据集中的数据比例""")
    for name, group in data:
        print(name)
        print(len(group))

    """步骤6：验证每一个小group中的index的类别 """
    print("""验证每一个小group中的index的类别""")
    from collections import Counter
    for name,group in data:
        now_counter = Counter(group['belong'])
        print(now_counter.most_common()) # 不会出现很大偏差的装填就是对的

    """步骤7：输出最后平衡KG的结果"""
    with open('./TREC_translate_kg_balance_result.txt', 'w+') as fp:
        for eachline in all_choice_data['content']:
            eachline = " ".join(eachline.split(' ')[1:])
            fp.writelines(eachline)

    """步骤8: """


""" 老的代码比例
0
1162
1
1250
2
86
3
1223
4
835
5
896
"""

""" 新的代码比例
0
1594
1
1715
2
118
3
1678
4
1145
5
1229
"""

# 最后成功生成的KG句子的数量