# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 02:33:23 2017

@author: monica
"""

from Env_cleanupWorld import *
from suffix_tree import SuffixTree
from suffix_tree import GeneralisedSuffixTree
import pickle

actionSet = {'up':0,'dw':1,'rt':2,'lf':3}

traj_file = open('traj_file','rb')
traj_list = list()

def lcs(S,T):
    m = len(S)
    n = len(T)
    counter = [[0]*(n+1) for x in range(m+1)]
    longest = 0
    lcs_set = set()
    for i in range(m):
        for j in range(n):
            if S[i] == T[j]:
                c = counter[i][j] + 1
                counter[i+1][j+1] = c
                if c > longest:
                    lcs_set = set()
                    longest = c
                    lcs_set.add(S[i-c+1:i+1])
                elif c == longest:
                    lcs_set.add(S[i-c+1:i+1])

    return lcs_set

if __name__ == '__main__':
    while 1:
        try:
            traj_list.append(pickle.load(traj_file))
        except EOFError:
            break

    traj_file.close()
    print traj_list[0]
    traj1 =  ''.join(str(e) for e in traj_list[0])
    traj2 = ''.join(str(e) for e in traj_list[2])
    print traj1, traj2

    ret = lcs(traj1,traj2)
    print ret
    
#    gstree = GeneralisedSuffixTree([traj1,traj2])
#    for l in gstree.leaves:
#        print l.pathLabel
#        
#    stree = SuffixTree(traj1)
#    for l in gstree.leaves:
#        print l.pathLabel

