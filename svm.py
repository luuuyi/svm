from numpy import *
import random

def loadDataFromFile(file_name):
    fd = open(file_name)
    datas=[];labels=[]
    for line in fd.readlines():
        line_list = line.strip().split('\t')
        datas.append(float(line_list[0]),float(line_list[1]))
        labels.append(float(line_list[2]))
    return datas, labels

def selectJRand(i,m):
    j = i
    while(j==i):
        j = int(random.uniform(0,m))
    return j

def clipAlpha(aj,H,L):
    if aj>H:    aj = H
    if L>aj:    aj = L
    return aj

