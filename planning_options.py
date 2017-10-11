"""
Created on Sun Sep  3 01:39:19 2017

@author: monica
"""
from Env_cleanupWorld import *
from option_utils import *
import random

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

o = o11
ranI = random.randint(0,len(o.init)-1)

start = o.init[ranI]
print start

goal = room2_door2
env = Enviroment(obj=o1,wall_list=wall_list,room_list=room_list,agent=robot,goal_states=goal)


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
    epsilon = 0.05
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

if __name__ == '__main__':
    env.robot.move2(list(start))
    env.obj.move2(goal[0])
    env._renderObjects()
    
    traj_policy = list()
    
    qa = o.policy
    curr_state = copy.deepcopy(start)
    
    pwr = 0
    pwr_sp = 1
    total_r = 0
    statePredic = 0
    gamma = 0.9
    
    c = 0    
    
    while 1:
        c += 1
        
        winA = e_greedy(curr_state,qa)  
    
        traj_policy.append(curr_state)
        next_state, reward, done = env.op_step(winA,o)
    
        curr_state = tuple(next_state)
        
        total_r = total_r + (gamma**pwr * reward)
        pwr += 1
        
        statePredic = statePredic + gamma**pwr_sp
        pwr_sp += 1
            
        print "------------>",winA, next_state, reward
        
        if c >= 100:
            break
        if done:
            
            env.set_optionRegions([traj_policy])
            env._renderObjects()
            print "*************Goal reached********* Stats: ", total_r,statePredic
            break