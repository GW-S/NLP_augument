# author:sheng.Gw
# -*- coding: utf-8 -*-
# @Date :  2019/5/24
import pandas as pd
import numpy as np

import sys
sys.path.append("/Users/sheng/Desktop/github/augument_paper/precessing_coding")

pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

file_path   = '/Users/sheng/PycharmProjects/contextual_augmentation/raw_content/stsa.binary.train'
output_path = './stsa_binary.csv'

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
from precessing_coding.baidu_translate.baidu_trainslate import translate
label    = list(input['label'])
sentence = list(input['sentence'])

trainSet_content = translate(sentence,'en','de')
allline = translate(trainSet_content, 'de', 'en')

input['translate_result'] = allline
print(input['translate_result'][0])

input.to_csv(output_path)