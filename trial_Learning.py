# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 17:52:32 2017

@author: monica
"""

from Env_cleanupWorld import *
import random

actionSet = {'up':0,'dw':1,'rt':2,'lf':3}

start = [20,30]
goal = [[200,200]]
obj_pos = [100,50]

env = Enviroment(obj=o1,wall_list=wall_list,room_list=room_list,agent=robot,goal_states=goal)

gameExit = False
if __name__ == "__main__":
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print "Quitting........ \n"
                gameExit == True
                break
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    curr_action = actionSet['lf']
                elif event.key == pygame.K_RIGHT:                    
                    curr_action = actionSet['rt']
                elif event.key == pygame.K_UP:                    
                    curr_action = actionSet['up']
                elif event.key == pygame.K_DOWN:
                    curr_action = actionSet['dw']
                else:
                    print "No keys"
                    curr_action = None
                
                next_state, reward, done = env.step(curr_action)
                print "Next state, reward", next_state,reward
                if done:
                    print "Goal reached \n Going to original positions"
                    print start, obj_pos
                    env.reset(start,obj_pos)
      
    print "Out of the game loop \n"
    pygame.quit()
    quit()