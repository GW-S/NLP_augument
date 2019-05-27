# author:sheng.Gw
# -*- coding: utf-8 -*-
# @Date :  2019/5/15
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

import sys
from os import path
import os
sys.path.append("/".join(path.abspath(__file__).split('/')[0:-3]))

from precessing_coding.kg_tools.KG_and_tools import parse_pos_only_NOUN
from precessing_coding.kg_tools.KG_and_tools import ruler # 上义词和同义词
from precessing_coding.contextual_augmentation.TREC.数据平衡.balance_library  import bucket_balance

def KG_transform_for_balance(file_list):
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

# # 对于每组,先刮下第一个,衡量剩下的，如果有，再刮下来一个;
#         # 刮下来一层
# def split_layer(my_group):
#     choice_index = []
#     choice_data = pd.DataFrame()
#     for index, each in my_group:
#         choice = each.sample(n=1)
#         now = choice.index.values.tolist()[0]
#         choice_index.append(now) # 这又是一个index,代表唯一的ID
#         choice_data = choice_data.append(choice, ignore_index=True)
#     return choice_index, choice_data
# # 清除刮下来的行，并计算还要刮的数量
# def then_analystic(group, number, all_choice_data_now, choice_data, choice_index):
#     group = group[~group.index.isin(choice_index)]
#     number = number - len(choice_index)
#     all_choice_data_now = all_choice_data_now.append(choice_data)
#     return number, group, all_choice_data_now
#
# def bucket_balance(dataSet_origion, dataSet_new, label1, label2, index_name):
#     """dataSet1指的是原始的数据集，dataSet2指的是新生成的KG的数据集
#        采取的思维是，对于同句话，生成的某一种KG扩展的词，视为同个桶，在这个层级上进行抽样。
#        由于是这样的原因，所以要在数据扩展的词汇中进行优化，记录每一个扩展词的来源。
#        综上，dataSet2需要的是 1.每个句子生成的新句子对应原句子的索引，2.自己的索引，3.标签, 4.文字内容
#        # 校验方法
#        #    1.对于整体的组，检测其分类的数量
#        #    2.对于每一个单独的组，打印出index的数量，检测是否按bucket抽取
#     """
#     group_label_origion = dataSet_origion.groupby(label1)
#     group_label_new     = dataSet_new.groupby(label2)
#
#     data_group_label_new_dict  = {}
#     for index, group in group_label_new:
#         print(index)
#         data_group_label_new_dict[str(index)] = group
#
#     data_group_label_orgion_dict = {}
#     for index,group in group_label_origion:
#         data_group_label_orgion_dict[str(index)] = group
#
#     # 最大样本比例 = min(旧数据集/新数据集中的数量)
#     # max_proportion = 0
#     # for name, item in group_label1:
#     #     proportion = len(item)/len(data_group_label2[name])
#     #     max_proportion = proportion if proportion > max_proportion else max_proportion
#
#     min_proportion = 1000000000
#     for name, item in group_label_origion:
#         # 1是原始的代码
#         proportion =  len(data_group_label_new_dict[name])/len(item)
#         min_proportion = proportion if proportion < min_proportion else min_proportion
#
#     # 这里的核心思想是尽可能的产生更多的数据集；
#     # 此时的制约是，新数据集有的产生的多，有的产生的少；
#     # 比如（旧/新） =  1/10 和 2/10,为了维持采样的比例相同；
#     # 对于前者可以产生10倍的采样，对于后者，他只能选择五倍的采样。为了同比例，前者也只能扩展五倍的采样。
#     # 那么实质上： 新的采样数 =  新数据 /  min( [ 新数据/旧数据 ] ）
#     # 那么 最大样本比例 = min(旧数据/新数据)
#
#     # 目的：维持新的采样比例和旧的相同
#     # 方法：找出旧的能在新数据中扩展的最大的比例，在新的数据中挑选这样的数量的结果
#     # 公式： min（新/旧） * 旧  = 最终的结果
#     # 公式： max（旧/新） * 新  = 最终的结果 ===》由于新的的数量不一致，这不能保证最终的结果
#     # todo 综上，以前的采样思路错了,以前的实验都要重做。
#
#     all_choice_data = pd.DataFrame()
#     for name,group in group_label_new:
#         # 对每个grop进行分层采样
#         print("分层采样进度",name)
#         number = len(data_group_label_orgion_dict[name]) * min_proportion
#         temp_group = group
#         while number>0:
#             print("仍需采样的数量",number)
#             group_now = temp_group
#             group_now = group_now.groupby(index_name)
#             choice_index,choice_data = split_layer(group_now)
#             number, temp_group, all_choice_data = then_analystic(temp_group,number,all_choice_data,choice_data,choice_index)
#     return all_choice_data
#
#

if __name__ == "__main__":

    """ 步骤1：用KG_transform_for_balance重新KG句子"""
    origion_KG_list = []
    if os.path.exists(
            '/Users/sheng/Desktop/github/augument_paper/precessing_coding/contextual_augmentation/TREC/数据平衡/store/origion_Kg_list.txt'):
        with open('/Users/sheng/Desktop/github/augument_paper/precessing_coding/contextual_augmentation/TREC/数据平衡/store/origion_Kg_list.txt') as fp:
            origion_KG_list = fp.readlines()
    else:
        file_path = '/Users/sheng/PycharmProjects/contextual_augmentation/raw_content/TREC.train'
        with open(file_path, 'r') as fp:
            file_list = fp.readlines()
        file_list = KG_transform_for_balance(file_list)
        with open('/Users/sheng/Desktop/github/augument_paper/precessing_coding/contextual_augmentation/TREC/数据平衡/store/origion_Kg_list.txt', 'w+') as fp:
            for each in file_list:
                fp.writelines(each + '\n')
            fp.close()
            origion_KG_list = file_list

    """ 步骤2：分析原始的句子"""
    dataSet_origion = pd.read_csv('/Users/sheng/Desktop/github/augument_paper/precessing_coding/contextual_augmentation/TREC/TREC_train.csv')
    dataFrame_origion = dataSet_origion.groupby('label')
    print("""原始数据集中的数据比例""")
    for name, group in dataFrame_origion:
        print(name)
        print(len(group))

    """ 步骤3：分析KG后的句子"""
    label  = []
    belong = []
    for index,eachline in enumerate(origion_KG_list):
        label.append(eachline.split()[1])
        belong.append(eachline.split()[0])
    dataSet = pd.DataFrame()
    dataSet['content'] = origion_KG_list
    dataSet['label']   = label
    dataSet['belong']  = belong
    data = dataSet.groupby('label')
    print("""分析KG后的句子比例""")
    for name, group in data:
        print(name)
        print(len(group))

    """步骤4： 保持比例进行采样"""
    all_choice_data = bucket_balance(dataSet_origion,dataSet,"label","label","belong")
    print(all_choice_data.head())

    """步骤5：验证最后的采样比例"""
    data = all_choice_data.groupby('label')
    print("""新数据集中的数据比例""")
    for name, group in data:
        print(name)
        print(len(group))

    print("""验证每一个小group中的index的类别""")
    from collections import Counter
    for name,group in data:
        now_counter = Counter(group['belong'])
        print(now_counter.most_common()) # 不会出现很大偏差的装填就是对的

    """步骤7：输出最后平衡KG的结果"""
    with open('./TREC_train_kg_balance_result.txt', 'w+') as fp:
        for eachline in all_choice_data['content']:
            eachline = " ".join(eachline.split(' ')[1:])
            fp.writelines(eachline)






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
1851
1
1991
2
137
3
1948
4
1330
5
1427
"""




# 最后成功生成的KG句子的数量 18432










