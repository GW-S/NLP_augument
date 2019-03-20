# author:sheng.Gw
# -*- coding: utf-8 -*-
# @Date :  2019/3/20
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

from baidu_translate.baidu_trainslate import translate

# 请务必不要运行该代码，因为烧的都是钱

with open('/Users/sheng/Desktop/augument_paper/test_coding/cnn-text-classification-tf/原始数据/rt-polarity-train.pos') as fp:
    allline = fp.readlines()
    trainSet_content = translate(allline, 'en', 'de')
    allline = translate(trainSet_content, 'de', 'en')

with open('/Users/sheng/Desktop/augument_paper/test_coding/cnn-text-classification-tf/原始数据+translate/rt-polarity-train.pos','w+') as fp:
    for each in allline:
        fp.writelines(each+'\n')

with open('/Users/sheng/Desktop/augument_paper/test_coding/cnn-text-classification-tf/原始数据/rt-polarity-train.neg') as fp:
    allline = fp.readlines()
    trainSet_content = translate(allline, 'en', 'de')
    allline = translate(trainSet_content, 'de', 'en')

with open('/Users/sheng/Desktop/augument_paper/test_coding/cnn-text-classification-tf/原始数据+translate/rt-polarity-train.neg','w+') as fp:
    for each in allline:
        fp.writelines(each+'\n')

