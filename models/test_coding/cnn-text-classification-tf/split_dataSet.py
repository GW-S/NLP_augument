# author:sheng.Gw
# -*- coding: utf-8 -*-
# @Date :  2019/2/18
import numpy as np
# 针对于某一种数据进行筛选

with open('/home/guowei/cnn-text-classification-tf/data/原始数据/rt-polarity.neg') as fp:
    all_neg = fp.readlines()
with open('/home/guowei/cnn-text-classification-tf/data/原始数据/rt-polarity.pos') as fp:
    all_pos = fp.readlines()

def split_train_and_test(path,save_path_train,save_path_test):
    with open(path) as fp:
        all_pos = fp.readlines()

    # Randomly shuffle data
    np.random.seed(10)
    shuffle_indices = np.random.permutation(np.arange(len(all_pos)))
    print(list(shuffle_indices))

    x_shuffled = []
    for each in list(shuffle_indices):
        x_shuffled.append(all_pos[each])

    dev_sample_index = -1 * int(0.1 * float(len(x_shuffled)))
    x_train, x_dev = x_shuffled[:dev_sample_index], x_shuffled[dev_sample_index:]

    with open(save_path_train,'w') as fp:
        for eachline in x_train:
            print(eachline)
            fp.writelines(eachline)

    with open(save_path_test,'w') as fp:
        for eachline in x_dev:
            fp.writelines(eachline)

if __name__ == "__main__":

    path_pos = '/home/guowei/cnn-text-classification-tf/data/原始数据/rt-polarity.pos'
    path_train = '/home/guowei/cnn-text-classification-tf/data/原始数据/rt-polarity-train.pos'
    path_test  = '/home/guowei/cnn-text-classification-tf/data/原始数据/rt-polarity-test.pos'
    split_train_and_test(path_pos,path_train,path_test)

    ###
    path_pos = '/home/guowei/cnn-text-classification-tf/data/原始数据/rt-polarity.neg'
    path_train = '/home/guowei/cnn-text-classification-tf/data/原始数据/rt-polarity-train.neg'
    path_test  = '/home/guowei/cnn-text-classification-tf/data/原始数据/rt-polarity-test.neg'
    split_train_and_test(path_pos, path_train, path_test)


"""
切分数据，修改读取文件
"""

