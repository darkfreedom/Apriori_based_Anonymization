"""
run DA and AA with given parameters
"""
#!/usr/bin/env python
# coding=utf-8
from apriori_based_anon import apriori_based_anon
from utils.read_data import read_data, read_tree
from models.gentree import GenTree
import sys
import copy
import random
import cProfile


DATA_SELECT = 'b'
TYPE_ALG = 'AA'
DEFALUT_M = 4
DEFALUT_K = 100
M_MAX = 161


def get_result_one(att_tree, data, type_alg, k=DEFALUT_K):
    """
    run apriori_based_anon for one time, with k=10
    """
    print "K=%d" % k
    print "Size of Data", len(data)
    print "m=%d" % DEFALUT_M
    _, eval_result = apriori_based_anon(att_tree, data, type_alg, k)
    print "NCP %0.2f" % eval_result[0] + "%"
    print "Running time %0.2f" % eval_result[1] + " seconds"


def get_result_k(att_tree, data, type_alg):
    """
    change k, whle fixing size of dataset
    """
    data_back = copy.deepcopy(data)
    # for k in range(5, 105, 5):
    print "m=%d" % DEFALUT_M
    print "Size of Data", len(data)
    for k in [2, 5, 10, 25, 50]:
        print '#' * 30
        print "K=%d" % k
        result, eval_result = apriori_based_anon(att_tree, data, type_alg, k)
        data = copy.deepcopy(data_back)
        print "NCP %0.2f" % eval_result[0] + "%"
        print "Running time %0.2f" % eval_result[1] + " seconds"


def get_result_m(att_tree, data, type_alg, k=DEFALUT_K):
    """
    change k, whle fixing size of dataset
    """
    print "K=%d" % k
    print "Size of Data", len(data)
    data_back = copy.deepcopy(data)
    # for m in range(1, 100, 5):
    for m in [1, 2, 3, 4, 5, M_MAX]:
        print '#' * 30
        print "m=%d" % m
        result, eval_result = apriori_based_anon(att_tree, data, type_alg, k, m)
        data = copy.deepcopy(data_back)
        print "NCP %0.2f" % eval_result[0] + "%"
        print "Running time %0.2f" % eval_result[1] + " seconds"


def get_result_dataset(att_tree, data, type_alg='AA', k=DEFALUT_K, num_test=10):
    """
    fix k, while changing size of dataset
    num_test is the test nubmber.
    """
    print "K=%d" % k
    print "m=%d" % DEFALUT_M
    data_back = copy.deepcopy(data)
    length = len(data_back)
    joint = 5000
    dataset_num = length / joint
    if length % joint == 0:
        dataset_num += 1
    for i in range(1, dataset_num + 1):
        pos = i * joint
        ncp = rtime = 0
        if pos > length:
            continue
        print '#' * 30
        print "size of dataset %d" % pos
        for j in range(num_test):
            temp = random.sample(data, pos)
            _, eval_result = apriori_based_anon(att_tree, temp, type_alg, k)
            ncp += eval_result[0]
            rtime += eval_result[1]
            data = copy.deepcopy(data_back)
        ncp /= num_test
        rtime /= num_test
        print "Average NCP %0.2f" % ncp + "%"
        print "Running time %0.2f" % rtime + " seconds"
        print '#' * 30


if __name__ == '__main__':
    # set K=10 as default
    FLAG = ''
    # gen_even_BMS_tree(5)
    try:
        TYPE_ALG = sys.argv[1]
        DATA_SELECT = sys.argv[2]
        FLAG = sys.argv[3]
    except IndexError:
        pass
    INPUT_K = 10
    if TYPE_ALG == 'DA' or TYPE_ALG == 'da':
        print "Begin DA"
    else:
        print "Begin AA"
    if DATA_SELECT == 'i':
        print "INFORMS data"
        DATA = read_data(1)
        ATT_TREE = read_tree(2)
    else:
        print "BMS-WebView data"
        DATA = read_data(0)
        ATT_TREE = read_tree(0)
    print "*" * 30
    # read generalization hierarchy
    # read record
    # remove duplicate items
    # DATA = DATA[:1000]
    # for i in range(len(DATA)):
    #     if len(DATA[i]) <= 40:
    #         DATA[i] = list(set(DATA[i]))
    #     else:
    #         DATA[i] = list(set(DATA[i][:40]))
    for i in range(len(DATA)):
        DATA[i] = list(set(DATA[i]))
    # print "Begin Apriori based Anon"
    if FLAG == 'k':
        get_result_k(ATT_TREE, DATA, TYPE_ALG)
    elif FLAG == 'm':
        get_result_m(ATT_TREE, DATA, TYPE_ALG)
    elif FLAG == 'data':
        get_result_dataset(ATT_TREE, DATA, TYPE_ALG)
    elif FLAG == '':
        cProfile.run('get_result_one(ATT_TREE, DATA, TYPE_ALG)')
        # get_result_one(ATT_TREE, DATA, TYPE_ALG)
    else:
        try:
            INPUT_K = int(FLAG)
            get_result_one(ATT_TREE, DATA, TYPE_ALG, INPUT_K)
        except ValueError:
            print "Usage: python anonymizer [i | b] [k | data]"
            print "AA: Apriori_based_Anon, DA: Direct Anon"
            print "i: INFORMS ataset, b: BMS-WebView dataset"
            print "k: varying k"
            print "data: varying size of dataset"
            print "example: python anonymizer b 10"
            print "example: python anonymizer b k"
    # anonymized dataset is stored in result
    print "Finish Apriori Based Anon!!"
