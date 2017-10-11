# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 09:42:29 2017

@author: monica
"""

from Env_cleanupWorld import *
import random
from option_utils import *
import copy

actions = ['rt', 'lf', 'up', 'dw']
actionSpace = {'up':0,'dw':1,'rt':2,'lf':3}

filename = 'val_svi'

goal = room2_door2
env = Enviroment(obj=o1,wall_list=wall_list,room_list=room_list,agent=robot,goal_states=goal)


def useget_reward(s,v):
    reward_dict = dict()
    
    for a in actions:
        av = actionSpace[a]
        r,sn = env.usevi_step(list(s),av,v)
        
        if not r == None:
            reward_dict[r,a] = sn
            
    return reward_dict

vo11 = load_obj('vo11')
vo12 = load_obj('vo12')
vo21 = load_obj('vo21')
vo22 = load_obj('vo22')
vo31 = load_obj('vo31')
vo32 = load_obj('vo32')
vo41 = load_obj('vo41')
vo42 = load_obj('vo42')

option_list = [vo11,vo12,vo21,vo22,vo31,vo32,vo41,vo42]

rso = 0
psx = 0
traj = list()

def initialiseV():
    val_f = dict()
    total_states = list()
    
    total_states = vo11.init + vo21.init + vo31.init + vo41.init 
    
    total_states.remove(tuple(room1_door1[0]))
    total_states.remove(tuple(room1_door2[0]))
    total_states.remove(tuple(room2_door2[0]))
    total_states.remove(tuple(room3_door2[0]))
    
    for s in total_states:
        if s == tuple(goal[0]):
            print "setting s to 1",s
            val_f[s] = 10
        else:
            val_f[s] = 0
            
    return val_f
    

def option_model(s,o,itr):
    
    pwr = 0
    pwr_sp = 1
    gamma = 0.997
    
    alpha = 1.0/itr
    statePredic = 0
    total_r = 0
    
    curr_s = copy.deepcopy(s)
    step_cnt = 0
    
    done = False
    
    while True:
        
        step_cnt += 1
        neigh_r = useget_reward(curr_s,o)
        
        next_s = neigh_r[max(neigh_r.keys())]
        
        if list(next_s) in o.termination:
            done = True
        
        if list(next_s) in goal:
            act_r = 10
        else:
            act_r = -1


        total_r = total_r + (gamma**pwr * act_r)
        
        pwr += 1
        pwr_sp += 1
       
        curr_s = tuple(next_s)
        
    
        if step_cnt >= 1000 or done:
            statePredic = statePredic + gamma**pwr_sp
            break
        
    return total_r,statePredic
    
    

if __name__ == '__main__':
    gamma = 0.997    
    cnt = 0
    V = initialiseV()
    dup_v = copy.deepcopy(V)
    
    while True:
        delta = 0
        cnt += 1
        
        for s in V.keys():
            temp = V[s]
            val_list = list()
            
            for o in option_list:
                if s in o.init:
                    rso,pss = option_model(s,o,cnt)
                    val = rso + pss * V[tuple(o.termination[0])]
                    val_list.append(val)
                    
            dup_v[s] = max(val_list)
            delta = max([delta,abs(temp-dup_v[s])])
            
        V = copy.deepcopy(dup_v)
        print delta,cnt
        if delta < 1 or cnt >= 1000:
            break
    save_obj(V,filename)
    
        

    
    
#    for o in option_list:
#        ranI = random.randint(0,len(o.init)-1)
#        start = o.init[ranI]
#        print start
#        
#        curr_s = copy.deepcopy(start)
#        step_cnt = 0
#        
#        done = False
#    
#        while True:
#            traj.append(curr_s)
#            step_cnt += 1
#            neigh_r = useget_reward(curr_s,o)
#            
#            next_s = neigh_r[max(neigh_r.keys())]
#            
#            if list(next_s) in o.termination:
#                done = True
#            
#            if list(next_s) in goal:
#                act_r = 10
#            else:
#                act_r = -1
#    
#    
#            print curr_s,next_s,act_r,done
#                
#            curr_s = tuple(next_s)
#                    
#            if step_cnt >= 1000 or done:
#                break
#            
#    traj.append(tuple(goal[0]))
#    env.set_optionRegions([traj])
#    env._renderObjects()
#    
#        
