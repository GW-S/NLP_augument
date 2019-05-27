# author:sheng.Gw
# -*- coding: utf-8 -*-
# @Date :  2019/5/22
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

"""
该文件将原始文件和引入的文件加入代码中
"""

import pysnooper

# @pysnooper.snoop()
def add_file(path,origion_file,output_file):

    path_file    = path

    with open(origion_file) as fp:
        origion_file_list = fp.readlines()

    with open(path_file) as fp1:
        add_file_list = fp1.readlines()

    origion_file_list.extend(add_file_list)

    import random
    random.shuffle(origion_file_list)

    with open(output_file,'w+') as fp2:
        for eachline in origion_file_list:
            fp2.writelines(eachline)

if __name__ == '__main__':

    origion_file = '/Users/sheng/PycharmProjects/contextual_augmentation/raw_content/TREC.train'

    # step1
    path1 = '/Users/sheng/Desktop/github/augument_paper/precessing_coding/contextual_augmentation/TREC/基本方法/data/1.TREC_train_kg.txt'
    path2 = '/Users/sheng/Desktop/github/augument_paper/precessing_coding/contextual_augmentation/TREC/基本方法/data/2.TREC_train_translate.txt'
    path3 = '/Users/sheng/Desktop/github/augument_paper/precessing_coding/contextual_augmentation/TREC/基本方法/data/3.TREC_train_translate+kg.txt'

    # step2
    path4 = '/Users/sheng/Desktop/github/augument_paper/precessing_coding/contextual_augmentation/TREC/数据平衡/data/4.TREC_train_kg_balance_result.txt'
    path5 = '/Users/sheng/Desktop/github/augument_paper/precessing_coding/contextual_augmentation/TREC/数据平衡/data/5.TREC_translate_kg_balance_result.txt'

    output_dir = '/Users/sheng/Desktop/github/augument_paper/precessing_coding/contextual_augmentation/TREC/增加原始数据/data/'
    path_list = [path1,path2,path3,path4,path5]
    for each_path in path_list:
        output_path = output_dir + each_path.split('/')[-1]
        add_file(each_path, origion_file, output_path)


    # 学习NLP的编程技巧
    # 总结前期工程，关机
    # 写PPT
    # 将准备的实验跑起来