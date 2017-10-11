# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 03:59:01 2017

@author: monica
"""

import pickle
from Env_cleanupWorld import *


traj_file = open('traj_fileMode','rb')
traj_setList = list()
env = Enviroment(obj=o1,wall_list=wall_list,room_list=room_list,agent=robot,goal_states=[[150,50]])

if __name__ == "__main__":
    while 1:
        try:
            l = pickle.load(traj_file)
            s = set(l)
            traj_setList.append(s)
            
        except EOFError:
            break
    optRegions = set.intersection(*traj_setList)
    print optRegions
    env.set_optionRegions(optRegions)
    env._renderObjects()
        