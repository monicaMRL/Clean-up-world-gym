# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 04:53:35 2017

@author: monica
"""

from Env_cleanupWorld import *
import random
from option_utils import *

def generate_qa(rm_v,doors):
    qa = dict()
    init_state = list()
    
    for i in range(rm_v[0][0],rm_v[2][0]+1,speed_r):
        for j in range(rm_v[0][1],rm_v[2][1]+1,speed_r):
            init_state.append((i,j))
            #print i,j
            for a in actions:
                qa[(i,j),a] = 0
                           
    for d in doors:
        init_state.append(tuple(d))
        for a in actions:
            qa[tuple(d),a] = 0
    
    return qa,init_state

maxEpi = 100
maxStep = 100
epsilon = 0.05
alpha = 0.28
gamma = 0.997

goal = room1_door1

env = Enviroment(obj=o1,wall_list=wall_list,room_list=room_list,agent=robot,goal_states=goal)

actions = ['rt', 'lf', 'up', 'dw']
actionSpace = {'up':0,'dw':1,'rt':2,'lf':3}

rm_v = r4.boundary
qa,init_s = generate_qa(rm_v,[room3_door2[0],room1_door2[0]])  

o = Option(init_s,goal)
name = 'blah'

def winnerNeighbour(s):
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

def act(s):
    flag = 'N'
    a = 'N'
    
    if random.random() <= epsilon:
        flag = 'random'
    else:
        flag = 'greedy'
        
    if flag == 'greedy':
        n, win_a = winnerNeighbour(s)
        a = win_a

    elif flag == 'random':
        index = random.randint(0,len(actions) - 1)
        a = actions[index]
    else:
        print 'Error \n'
        a = None
        
    return a
    
def random_curr():
    ranIndex = random.randint(0,len(o.init)-1)
    
    return o.init[ranIndex]


if __name__ == '__main__':
    #pass
    episode = 0
    #qa = load_obj('room1_door1')
    while(episode < maxEpi):
        rewardSum = 0
        cur_state = random_curr()
        env.robot.move2(list(cur_state))
        for i in range(maxStep):
            a = act(cur_state)
            next_state, reward, done = env.step(actionSpace[a])

            win_n, win_a = winnerNeighbour(cur_state)
            max_qa = qa[tuple(next_state),win_a]
            
            qa[cur_state,a] = qa[cur_state,a] + alpha * (reward + gamma* max_qa - qa[cur_state,a])
            cur_state = tuple(next_state)
            rewardSum += reward
            if done or i == maxStep-1:
                episode += 1
                print "Average Reward: ", rewardSum, "Episode no: ",episode
                break
    
    o.setPolicy(qa)
    save_obj(o,name)
            
    