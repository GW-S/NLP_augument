# author:sheng.Gw
# -*- coding: utf-8 -*-
# @Date :  2019/5/24
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

origion_data = pd.read_csv('stsa_binary.csv')

print(origion_data.head())

with open('origion_with_translate.txt','w+') as fp:
    for index,each in origion_data.iterrows():
        label            = each['label']
        translate_result = each['translate_result']
        the_line = str(label) + ' ' + str(translate_result) +'\n'
        print(the_line)
        fp.writelines(the_line)