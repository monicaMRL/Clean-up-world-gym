# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 04:27:01 2017

@author: monica
"""

from Env_cleanupWorld import *
import copy
import random
from option_utils import *

filename = 'aveSVI2'

goal = room2_door2
env = Enviroment(obj=o1,wall_list=wall_list,room_list=room_list,agent=robot,goal_states=goal)
        
epsilon = 0.05
gamma = 0.9

o11 = load_obj('o11')
o12 = load_obj('o12')
o21 = load_obj('o21')
o22 = load_obj('o22')
o31 = load_obj('o31')
o32 = load_obj('o32')
o41 = load_obj('o41')
o42 = load_obj('o42')

actions = ['rt', 'lf', 'up', 'dw']
actionSpace = {'up':0,'dw':1,'rt':2,'lf':3}
option_list = [o11,o12,o21,o22,o31,o32,o41,o42]

rso = 0
psx = 0

def initialiseV():
    val_f = dict()
    total_states = list()
    
    total_states = o11.init + o21.init + o31.init + o41.init 
    
    total_states.remove(tuple(room1_door1[0]))
    total_states.remove(tuple(room1_door2[0]))
    total_states.remove(tuple(room2_door2[0]))
    total_states.remove(tuple(room3_door2[0]))
    
    for s in total_states:
        if s == tuple(goal[0]):
            print "setting s to 1",s
            val_f[s] = 1
        else:
            val_f[s] = 0
            
    return val_f
                

def winnerNeighbour(s,qa):
    '''
    Takes in state: return Max Q valued neighbour with Q value
    @param: state --> tuple position
    @return: s', value --> tuple, float
    '''
    winningN = None
    winningAction = None
    values = list()
    
    for ele in actions:
        values.append(qa[s,ele])

    maxVal = max(values)
    
    winningN, winningAction = qa.keys()[qa.values().index(maxVal)]
    
    return winningN,winningAction


def e_greedy(s,qa):
    flag = 'N'
    a = 'N'
    
    if random.random() <= epsilon:
        flag = 'random'
    else:
        flag = 'greedy'
        
    if flag == 'greedy':
        n, win_a = winnerNeighbour(s,qa)
        a = win_a

    elif flag == 'random':
        index = random.randint(0,len(actions) - 1)
        a = actions[index]
    else:
        print 'Error \n'
        a = None
        
    return actionSpace[a]

def o_model(s,o,itr):
    global rso, psx
    
    alpha = 1.0/itr
    env.robot.move2(list(s))
    
    statePredic = 0
    total_r = 0
    qa = o.policy
    curr_state = tuple(copy.deepcopy(s))
    pwr = 0
    pwr_sp = 1
    while 1:
        
        winA = e_greedy(curr_state,qa)  
    
        next_state, reward, done = env.op_step(winA,o)
        
        if tuple(next_state) in o.init:
            curr_state = tuple(next_state)
        
        total_r = total_r + (gamma**pwr * reward)
                
        statePredic = statePredic + gamma**pwr_sp
                
        pwr += 1
        pwr_sp += 1
        
        rso = rso + alpha * (total_r - rso)
        psx = psx + alpha * (gamma**pwr_sp * statePredic - psx)
        
        if done:
            #env._renderObjects()
            #print "*************Goal reached*********"
            break
        
    return rso,psx

    
if __name__ == "__main__":
    V = initialiseV()
    dup_v = copy.deepcopy(V)
    
    for itr in range(1,16):
        cnt = 0
        print "Iteration No: ",itr
        for s in V.keys():
            cnt += 1
            #print "state number: ",cnt, "State: ", s
            val_list = list()
            for o in option_list:
                
                if s in o.init:
                    rso,ps = o_model(s,o,itr)
                    val = rso + ps * V[tuple(o.termination[0])]
                    val_list.append(val)
            dup_v[s] = max(val_list)
            
            
        V = copy.deepcopy(dup_v)
        
        save_obj(V,filename)