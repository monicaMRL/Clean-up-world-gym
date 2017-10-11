# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 10:56:21 2017

@author: monica16
"""

from Env_cleanupWorld import *
import copy
import random
from option_utils import *

goal = room2_door2
env = Enviroment(obj=o1,wall_list=wall_list,room_list=room_list,agent=robot,goal_states=goal)

filename = 'aveSVI2'
val_f = load_obj(filename)

o11 = load_obj('o11')
o12 = load_obj('o12')
o21 = load_obj('o21')
o22 = load_obj('o22')
o31 = load_obj('o31')
o32 = load_obj('o32')
o41 = load_obj('o41')
o42 = load_obj('o42')

epsilon = 0#0.05#1.0
decay = 0.999
e_min = 0.05

def win_neighbour(s):
    x = s[0]
    y= s[1]
    
    n1 = [x+speed_r,y]
    n2 = [x,y+speed_r]
    n3 = [x-speed_r,y]
    n4 = [x,y-speed_r]
    
    nl = [n1,n2,n3,n4]
    valid_nl = list()
    
    for n in nl:
        if tuple(n) in val_f.keys():
            valid_nl.append(n)
    
    print "state s neighbour: ", s, valid_nl
     
    neigh_val = dict()
    
    
    for n in valid_nl:
#        if tuple(n) in val_f.keys():
        neigh_val[val_f[tuple(n)]] = n
    
    return neigh_val[max(neigh_val.keys())],valid_nl
    

def act(s):
    
    flag = 'N'
    
    best_n, nl = win_neighbour(s)
    
    if random.random() <= epsilon:
        flag = 'random'
    else:
        flag = 'greedy'
        
    if flag == 'greedy':
        neigh = best_n
    elif flag == 'random':
        ranI = random.randint(0,len(nl)-1)
        neigh = nl[ranI]
    else:
        print 'Error \n'
        neigh = None

    return neigh    

if __name__ == '__main__':
    
    ranI = random.randint(0,len(o12.init)-1)
    #s = val_f.keys()[ranI]
    s = o32.init[ranI]
    #s = [130,190]
    env.robot.move2(s)
    
    curr_state = copy.deepcopy(s)
    traj = list()
    
    cnt = 0
    while True:
        print curr_state
        cnt += 1 
        traj.append(curr_state)
        ns = act(curr_state)
        curr_state = ns
        
#        if epsilon > e_min:
#            epsilon = epsilon * decay
        
        if list(curr_state) in goal:
            traj.append(curr_state)
            env.set_optionRegions([traj])
            env._renderObjects()
            print "it works!!!!!! \n"
            break
        
        if cnt >= 8000:
            traj.append(curr_state)
            env.set_optionRegions([traj])
            env._renderObjects()
            print "It didnt work :( \n"
            break