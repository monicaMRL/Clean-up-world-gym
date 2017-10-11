# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 06:21:33 2017

@author: monica
"""
import pickle


room1_door1 = [[100,40]]
room1_door2 = [[30,100]]
room2_door2 = [[140,100]]
room3_door2 = [[100,170]]

door_list = [room1_door1[0],room1_door2[0],room2_door2[0],room3_door2[0]]
def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        
def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

class Option(object):
    def __init__(self,initiation,termination):
        self.policy = None
        self.termination = termination
        self.init = initiation
        
    def setPolicy(self,qa):
        self.policy = qa
        
        
