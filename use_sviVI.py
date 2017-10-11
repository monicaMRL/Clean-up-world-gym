# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 04:16:51 2017

@author: monica
"""

from Env_cleanupWorld import *
import random
from option_utils import *
import copy

goal = room2_door2

env = Enviroment(obj=o1,wall_list=wall_list,room_list=room_list,agent=robot,goal_states=goal)

filename = 'val_svi'

actions = ['rt', 'lf', 'up', 'dw']
actionSpace = {'up':0,'dw':1,'rt':2,'lf':3}

def useget_reward(s,v):
    reward_dict = dict()
    
    for a in actions:
        av = actionSpace[a]
        r,sn = env.usevi_step(list(s),av,v)
        
        if not r == None:
            reward_dict[r,a] = sn
            
    return reward_dict
    
if __name__ == '__main__':
    v_env = load_obj(filename)
    opt_name = 'vo11'
    o = load_obj(opt_name)    
    print "Termination: ", o.termination
    
    ranI = random.randint(0,len(o.init)-1)
    start = o.init[ranI]
    print start
    
    curr_s = copy.deepcopy(start)
    step_cnt = 0
    traj = list()
    
    done = False
    
    while True:
        traj.append(curr_s)
        step_cnt += 1
        neigh_r = useget_reward(curr_s,v_env)
        
        next_s = neigh_r[max(neigh_r.keys())]
        
        if list(next_s) in goal:
            done = True
        
        if list(next_s) in goal:
            act_r = 10
        else:
            act_r = -1

        print step_cnt,done,v_env[tuple(goal[0])]
        print curr_s,v_env[tuple(curr_s)]
        print next_s,v_env[tuple(next_s)]
        curr_s = tuple(next_s)
                
        if step_cnt >= 100 or done:
            break
        
    traj.append(tuple(goal[0]))
    env.set_optionRegions([traj])
    env._renderObjects()
    
        
