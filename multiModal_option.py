# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 01:03:08 2017

@author: monica
"""

from Env_cleanupWorld import *
import itertools
import numpy as np
import random
from Graph import *

#env = Enviroment(obj=o1,wall_list=wall_list,room_list=room_list,agent=robot,goal_states=[[150,50]])

class Mode(object):
    def __init__(self,name,constraint):
        self.name = name
        self.constraint = constraint
        
        self.mode_set = self._generate_set()
        
    def _generate_set(self):
        minConstraint = self.constraint[0]
        maxConstraint = self.constraint[1]
        step = self.constraint[2]
        
        x = [i for i in range(minConstraint[0],maxConstraint[0]+step,step)]
        y = [i for i in range(minConstraint[1],maxConstraint[1]+step,step)]
        
        if len(minConstraint) == 2:
            mode_set = np.array(list(itertools.product(x,y)))
        elif len(minConstraint) == 4:
            mode_set = np.array(list(itertools.product(x,y,x,y)))
        else:
            print "Constraint not recognised"
        return mode_set
        
    def random_sample(self):
        length, width = self.mode_set.shape
        random_i = random.randint(0,length-1)
        
        return self.mode_set[random_i]
    
    def __str__(self):
        return self.name


#if __name__ == '__main__':
m_room1 = Mode('m_room1',[vr1[0],vr1[2],speed_r])
m_room2 = Mode('m_room2',[vr2[0],vr2[2],speed_r])
m_room3 = Mode('m_room3',[vr3[0],vr3[2],speed_r])
m_room4 = Mode('m_room4',[vr4[0],vr4[2],speed_r])
#p_room1 = Mode('p_room1',[[0,0,0,0],[WIDTH/2,HEIGHT/2,WIDTH/2,HEIGHT/2],speed_r])
#p_room2 = Mode('p_room2',[[WIDTH/2,0,WIDTH/2,0],[WIDTH,HEIGHT/2,WIDTH,HEIGHT/2],speed_r])
#p_room3 = Mode('p_room3',[[WIDTH/2,HEIGHT/2,WIDTH/2,HEIGHT/2],[WIDTH,HEIGHT,WIDTH,HEIGHT],speed_r])
#p_room4 = Mode('p_room4',[[0,HEIGHT/2,0,HEIGHT/2],[WIDTH/2,HEIGHT,WIDTH/2,HEIGHT],speed_r])

transition_graph = Graph([(m_room1,m_room2),(m_room2,m_room3),(m_room3,m_room4),(m_room4,m_room1)])

v_set = transition_graph.vertex_set()

#for i in range(5):
#    random_start = ramdom.sample(v_set)
#    neighbours =  transition_graph.give_connections(random_start)
#    random_goal = random.sample(neighbours)
        
        