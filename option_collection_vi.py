# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 06:52:34 2017

@author: monica
"""

from Env_cleanupWorld import *
import random
from option_utils import *
import copy

goal = room2_door2

env = Enviroment(obj=o1,wall_list=wall_list,room_list=room_list,agent=robot,goal_states=goal)

def generate_v(rm_v,doors):
    v = dict()
    init_state = list()
    
    for i in range(rm_v[0][0],rm_v[2][0]+1,speed_r):
        for j in range(rm_v[0][1],rm_v[2][1]+1,speed_r):
            init_state.append((i,j))
            v[(i,j)] = 0
            
    for d in doors:
        init_state.append(tuple(d))
        if d in goal:
            
            v[tuple(d)] = 10
        else:
            v[tuple(d)] = 0
    
    return v,init_state
    
actions = ['rt', 'lf', 'up', 'dw']
actionSpace = {'up':0,'dw':1,'rt':2,'lf':3}

rm_v = r4.boundary
vf,init_s = generate_v(rm_v,[room3_door2[0],room1_door2[0]])  

print vf[tuple(goal[0])]
o = Option(init_s,goal)

name = 'vo42'

def get_reward(s):
    reward_dict = dict()
    
    for a in actions:
        av = actionSpace[a]
        r,sn,done = env.vi_step(list(s),av,o)
        
        if not r == None:
            reward_dict[r,a] = sn
            
    return reward_dict

def useget_reward(s,v):
    reward_dict = dict()
    
    for a in actions:
        av = actionSpace[a]
        r,sn = env.usevi_step(list(s),av,v)
        
        if not r == None:
            reward_dict[r,a] = sn
            
    return reward_dict
    
if __name__ == '__main__':
    gamma = 0.997    
    cnt = 0

    while True:
        delta = 0
        cnt += 1
        for s in vf.keys():
            
            temp = vf[s]
            
            r_dict = get_reward(s)
            list_ar = [ra[0] + gamma * vf[r_dict[ra]] for ra in r_dict.keys()] 
            
            vf[s] = max(list_ar)
            delta = max([delta,abs(temp-vf[s])])
            
        print delta,cnt
        if delta < 0.1:
            break
    print "Done making value function"
    o.setPolicy(vf)
    save_obj(o,name) 

#    o = load_obj(name)
#    print "Termination: ", o.termination
#    
#    ranI = random.randint(0,len(o.init)-1)
#    start = o.init[ranI]
#    print start
#    
#    curr_s = copy.deepcopy(start)
#    step_cnt = 0
#    traj = list()
#    
#    done = False
#    
#    while True:
#        traj.append(curr_s)
#        step_cnt += 1
#        neigh_r = useget_reward(curr_s,o)
#        
#        next_s = neigh_r[max(neigh_r.keys())]
#        
#        if list(next_s) in o.termination:
#            done = True
#        
#        if list(next_s) in goal:
#            act_r = 10
#        else:
#            act_r = -1
#
#
#        print curr_s,next_s,act_r,done
#            
#        curr_s = tuple(next_s)
#                
#        if step_cnt >= 1000 or done:
#            break
#        
#    traj.append(tuple(goal[0]))
#    env.set_optionRegions([traj])
#    env._renderObjects()
#    
#        
