from numpy import *
import random

def loadDataFromFile(file_name):
    fd = open(file_name)
    datas=[];labels=[]
    for line in fd.readlines():
        line_list = line.strip().split('\t')
        datas.append([float(line_list[0]),float(line_list[1])])
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

def simpleSMO(datas,labels,C,toler,iter_nums):
    datas_mat = mat(datas);labels_mat = mat(labels).transpose()
    b=0;h, w = shape(datas_mat)
    alphas = mat(zeros((h,1)))
    iter_now = 0
    while(iter_now < iter_nums):
        alpha_pairs_changed = 0
        for i in range(h):
            fxi = float(multiply(alphas,labels_mat).T * (datas_mat*datas_mat[i].T)) + b
            ei = fxi - float(labels_mat[i])
            if ((labels_mat[i]*ei < -toler) and (alphas[i] < C)) or ((labels_mat[i]*ei > toler) and (alphas[i] > 0)):
                j = selectJRand(i,h)
                fxj = float(multiply(alphas,labels_mat).T * (datas_mat*datas_mat[j].T)) + b
                ej = fxj - float(labels_mat[j])
                alpha_i_old = alphas[i].copy()
                alpha_j_odl = alphas[j].copy()
                if(labels_mat[i] != labels_mat[j]):
                    L = max(0,alphas[j]-alphas[i])
                    H = min(C,C + alphas[j]-alphas[i])
                else:
                    L = max(0,alphas[j]+alphas[i]-C)
                    H = min(C,alphas[j]+alphas[i])
                if L==H:    print "L==M";continue
                eta = 2.0*datas_mat[i]*datas_mat[j].T - datas_mat[i]*datas_mat[i].T - datas_mat[j]*datas_mat[j].T
                if eta >= 0 :   print "eta>=0";continue
                alphas[j] -= labels_mat[j]*(ei - ej)/eta
                alphas[j] = clipAlpha(alphas[j],H,L)
                if (abs(alphas[j] - alpha_j_odl) < 0.00001):    print "j not moving enough";continue
                alphas[i] = labels_mat[j]*labels_mat[i]*(alpha_j_odl - alphas[j])
                b1 = b - ei - labels_mat[i]*(alphas[i] - alpha_i_old)*datas_mat[i]*datas_mat[i].T - labels_mat[j]*(alphas[j] - alpha_j_odl) * datas_mat[i]*datas_mat[j].T
                b2 = b - ej - labels_mat[i]*(alphas[i] - alpha_i_old)*datas_mat[i]*datas_mat[j].T - labels_mat[j]*(alphas[j] - alpha_j_odl) * datas_mat[j]*datas_mat[j].T
                if (0<alphas[i]) and (C>alphas[i]): b = b1
                elif (0<alphas[j]) and (C>alphas[j]):   b = b2
                else:   b = (b1+b2)/2.0
                alpha_pairs_changed += 1
                print "iter: %d i: %d, pairs changed %d" % (iter_now,i,alpha_pairs_changed)
        if (alpha_pairs_changed == 0): iter_now += 1
        else:   iter_now = 0
        print "iteration number: %d" % iter_now
    return b, alphas

if __name__ == '__main__':
    file_name = 'testSet.txt'
    datas, labels = loadDataFromFile(file_name)
    #print datas, labels
    b, alphas = simpleSMO(datas,labels,0.6,0.001,40)