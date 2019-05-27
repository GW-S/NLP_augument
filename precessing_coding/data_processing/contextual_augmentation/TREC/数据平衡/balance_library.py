# author:sheng.Gw
# -*- coding: utf-8 -*-
# @Date :  2019/5/26
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

# 对于每组,先刮下第一个,衡量剩下的，如果有，再刮下来一个;
        # 刮下来一层
def split_layer(my_group):
    choice_index = []
    choice_data = pd.DataFrame()
    for index, each in my_group:
        choice = each.sample(n=1)
        now = choice.index.values.tolist()[0]
        choice_index.append(now) # 这又是一个index,代表唯一的ID
        choice_data = choice_data.append(choice, ignore_index=True)
    return choice_index, choice_data
# 清除刮下来的行，并计算还要刮的数量
def then_analystic(group, number, all_choice_data_now, choice_data, choice_index):
    group = group[~group.index.isin(choice_index)]
    number = number - len(choice_index)
    all_choice_data_now = all_choice_data_now.append(choice_data)
    return number, group, all_choice_data_now

def bucket_balance(dataSet_origion, dataSet_new, label1, label2, index_name):
    """dataSet1指的是原始的数据集，dataSet2指的是新生成的KG的数据集
       采取的思维是，对于同句话，生成的某一种KG扩展的词，视为同个桶，在这个层级上进行抽样。
       由于是这样的原因，所以要在数据扩展的词汇中进行优化，记录每一个扩展词的来源。
       综上，dataSet2需要的是 1.每个句子生成的新句子对应原句子的索引，2.自己的索引，3.标签, 4.文字内容
       # 校验方法
       #    1.对于整体的组，检测其分类的数量
       #    2.对于每一个单独的组，打印出index的数量，检测是否按bucket抽取
    """
    group_label_origion = dataSet_origion.groupby(label1)
    group_label_new     = dataSet_new.groupby(label2)

    data_group_label_new_dict  = {}
    for index, group in group_label_new:
        data_group_label_new_dict[str(index)] = group

    data_group_label_origion_dict = {}
    for index,group in group_label_origion:
        data_group_label_origion_dict[str(index)] = group

    # 最大样本比例 = min(旧数据集/新数据集中的数量)
    # max_proportion = 0
    # for name, item in group_label1:
    #     proportion = len(item)/len(data_group_label2[name])
    #     max_proportion = proportion if proportion > max_proportion else max_proportion

    #步骤1，原始数据的比例


    # 步骤2. 新的/旧的
    min_proportion = 1000000000
    for name, item in group_label_origion:
        # 1是原始的代码
        proportion =  len(data_group_label_new_dict[str(name)])/len(item)
        min_proportion = proportion if proportion < min_proportion else min_proportion
    # 步骤2.

    # 这里的核心思想是尽可能的产生更多的数据集；
    # 此时的制约是，新数据集有的产生的多，有的产生的少；
    # 比如（旧/新） =  1/10 和 2/10,为了维持采样的比例相同；
    # 对于前者可以产生10倍的采样，对于后者，他只能选择五倍的采样。为了同比例，前者也只能扩展五倍的采样。
    # 那么实质上： 新的采样数 =  新数据 /  min( [ 新数据/旧数据 ] ）
    # 那么 最大样本比例 = min(旧数据/新数据)

    # 目的：维持新的采样比例和旧的相同
    # 方法：找出旧的能在新数据中扩展的最大的比例，在新的数据中挑选这样的数量的结果
    # 公式： min（新/旧） * 旧  = 最终的结果
    # 公式： max（旧/新） * 新  = 最终的结果 ===》由于新的的数量不一致，这不能保证最终的结果
    # todo 综上，以前的采样思路错了,以前的实验都要重做。

    all_choice_data = pd.DataFrame()
    for name,group in group_label_new:
        # 对每个grop进行分层采样
        print("分层采样进度",name)
        number = len(data_group_label_origion_dict[name]) * min_proportion
        print("理论上该得的",number)
        temp_group = group
        while number>0:
            print("仍需采样的数量",number)
            group_now = temp_group
            group_now = group_now.groupby(index_name)
            choice_index,choice_data = split_layer(group_now)
            if len(choice_data) >= number:
                choice_data = choice_data.sample(int(number))
            number, temp_group, all_choice_data = then_analystic(temp_group,number,all_choice_data,choice_data,choice_index)
    return all_choice_data


