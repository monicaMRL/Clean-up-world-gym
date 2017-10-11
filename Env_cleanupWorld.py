# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 16:50:47 2017

@author: monica
"""

#-------------------- Imports -----------------------------
import pygame
import matplotlib.path as mplPath
import numpy as np
import math
from scipy.spatial.distance import euclidean as point_dist
import random
import copy
from option_utils import *
#------------------- Global Variables ---------------------------
WIDTH = 200
HEIGHT = 200

colorSpace = {'black':[0,0,0],'white':[255,255,255],'red':[255,0,0],'green':[0,255,0],'blue':[0,0,255],'yellow':[255,255,0],'cyan':[0,255,255],'magenta':[255,0,255]}

speed_r = 10
action2Speed = {'up':[0,-speed_r],'dw':[0,speed_r],'rt':[speed_r,0],'lf':[-speed_r,0]}
actionSpace = {0:'up',1:'dw',2:'rt',3:'lf'}
#-------------------- Classes ------------------------------------
class Object(object):
    def __init__(self,color,center):
        self.color = color
        self.center = copy.deepcopy(center)
        self.oscale = 5
        self.vertices = self._calculateVertices(self.center,self.oscale)
        
    def _calculateVertices(self,c,scale):        
        v = list()
        
        v1 = (c[0]-scale,c[1]-scale)
        v.append(v1)                

        v2 = (c[0]+scale,c[1]-scale)
        v.append(v2)
        
        v3 = (c[0]+scale,c[1]+scale)
        v.append(v3)
        
        v4 = (c[0]-scale,c[1]+scale)
        v.append(v4)
        
        return v
        
    def move(self,speed):
        self.center[0] = self.center[0] + speed[0]
        self.center[1] = self.center[1] + speed[1]
        
        self.vertices = self._calculateVertices(self.center,self.oscale)
        
    def move2(self,position):
        self.center = copy.deepcopy(position)
        self.vertices = self._calculateVertices(self.center,self.oscale)
        
    def __str__(self):
        return ("Center: " + str(self.center) + 'Vertices: ' + str(self.vertices))
    
    
class Agent(Object):
    def __init__(self,color,center):
        super(self.__class__, self).__init__(color,center)
        self.state_size = 2
        self.action_size = 4
        
       
    def inContact(self,obj):
        contact = False
        align = None
        
        distance = point_dist(np.array(self.center),np.array(obj.center))#math.sqrt((self.center[0]-obj.center[0])**2 + (self.center[1]-obj.center[1])**2)
       
        if (self.center[0] == obj.center[0] and self.center[1] > obj.center[1] and distance <= 2*self.oscale):
            align = 'bottom'
            contact = True
        elif (self.center[0] == obj.center[0] and self.center[1] < obj.center[1] and distance <= 2*self.oscale):
            align = 'top'
            contact = True
        elif (self.center[1] == obj.center[1] and self.center[0] > obj.center[0] and distance <= 2*self.oscale):
            align = 'right'
            contact = True
        elif (self.center[1] == obj.center[1] and self.center[0] < obj.center[0] and distance <= 2*self.oscale):
            align = 'left'
            contact = True
        else:
            align = None
            contact = False
            
        return (contact,align)
        
        
    def moveObject(self,obj,speed):
        contact, align = self.inContact(obj)
        if contact:
            #TODO: write pushing code
            obj.move(speed)
            self.move(speed)
        else:
            print "No object in contact"
            
        
        
class Room(object):
    def __init__(self,vertices,name,boundary):
        self.vertices = vertices
        self.name = str(name)
        self.color = colorSpace['black']
        self.boundary = boundary
        
        cx = 0
        cy = 0
        
        for v in self.vertices:
            cx += v[0]
            cy += v[1]
            
        self.center = [cx/4,cy/4]
            
    def inside(self,robot):
        o_path = mplPath.Path(np.array(self.vertices))

        return o_path.contains_point(robot.center,radius=1)
        

class Obstacles(Room):
    def __init__(self,vertices):
        super(self.__class__, self).__init__(vertices,'wall',None)
        self.color = colorSpace['yellow']
        obs_list
    def collision(self,robot):
        return self.inside(robot)
        
#---------------------- Class Instances --------------------------------
wallThikness = 5
gap = 10

#o1 = Object(colorSpace['blue'],[WIDTH/4,HEIGHT/4])
        
o1 = Object(colorSpace['blue'],[20,50])
o2 = Object(colorSpace['red'],[3*WIDTH/4,3*HEIGHT/4])
o3 = Object(colorSpace['cyan'],[WIDTH/4,3*HEIGHT/4])

obs_list = list()

obs_list.append(o1)
#obs_list.append(o2)
#obs_list.append(o3)


vr1 = [[0,0],[WIDTH/2,0],[WIDTH/2,HEIGHT/2],[0,HEIGHT/2]]
vr2 = [[WIDTH/2,0],[WIDTH,0],[WIDTH,HEIGHT/2],[WIDTH/2,HEIGHT/2]]
vr3 = [[WIDTH/2,HEIGHT/2],[WIDTH,HEIGHT/2],[WIDTH,HEIGHT],[WIDTH/2,HEIGHT]]
vr4 = [[0,HEIGHT/2],[WIDTH/2,HEIGHT/2],[WIDTH/2,HEIGHT],[0,HEIGHT]]

br1 = [[0,0],[WIDTH/2-(2*wallThikness),0],[WIDTH/2-(2*wallThikness),HEIGHT/2-(2*wallThikness)],[0,HEIGHT/2-(2*wallThikness)]]
br2 = [[WIDTH/2+(2*wallThikness),0],[WIDTH,0],[WIDTH,HEIGHT/2-(2*wallThikness)],[WIDTH/2+(2*wallThikness),HEIGHT/2-(2*wallThikness)]]
br3 = [[WIDTH/2+(2*wallThikness),HEIGHT/2+(2*wallThikness)],[WIDTH,HEIGHT/2+(2*wallThikness)],[WIDTH,HEIGHT],[WIDTH/2+(2*wallThikness),HEIGHT]]
br4 = [[0,HEIGHT/2+(2*wallThikness)],[WIDTH/2-(2*wallThikness),HEIGHT/2+(2*wallThikness)],[WIDTH/2-(2*wallThikness),HEIGHT],[0,HEIGHT]]

#print br1,br2,br2,br4

r1 = Room(vr1,1,br1)   
r2 = Room(vr2,2,br2)
r3 = Room(vr3,3,br3)
r4 = Room(vr4,4,br4)

room_list = list()

room_list.append(r1)
room_list.append(r2)
room_list.append(r3)
room_list.append(r4)

robot = Agent(colorSpace['white'],[20,30])

wall_list = list()

vw1 = [[WIDTH/2-wallThikness,0],[WIDTH/2+wallThikness,0],[WIDTH/2+wallThikness,HEIGHT/6],[WIDTH/2-wallThikness,HEIGHT/6]]
ob1 = Obstacles(vw1)
vw2 = [[WIDTH/2-wallThikness,HEIGHT/6+gap],[WIDTH/2+wallThikness,HEIGHT/6+gap],[WIDTH/2+wallThikness,HEIGHT/2],[WIDTH/2-wallThikness,HEIGHT/2]]
ob2 = Obstacles(vw2)
vw3 = [[WIDTH/2,HEIGHT/2-wallThikness],[WIDTH/2,HEIGHT/2+wallThikness],[WIDTH-WIDTH/3,HEIGHT/2+wallThikness],[WIDTH-WIDTH/3,HEIGHT/2-wallThikness]]
ob3 = Obstacles(vw3)
vw4 = [[WIDTH-WIDTH/3+gap,HEIGHT/2-wallThikness],[WIDTH-WIDTH/3+gap,HEIGHT/2+wallThikness],[WIDTH+1,HEIGHT/2+wallThikness],[WIDTH+1,HEIGHT/2-wallThikness]]
ob4 = Obstacles(vw4)
vw5 = [[WIDTH/2-wallThikness,HEIGHT/2],[WIDTH/2+wallThikness,HEIGHT/2],[WIDTH/2+wallThikness,HEIGHT-HEIGHT/5],[WIDTH/2-wallThikness,HEIGHT-HEIGHT/5]]
ob5 = Obstacles(vw5)
vw6 = [[WIDTH/2-wallThikness,HEIGHT+1],[WIDTH/2+wallThikness,HEIGHT+1],[WIDTH/2+wallThikness,HEIGHT-HEIGHT/5+gap],[WIDTH/2-wallThikness,HEIGHT-HEIGHT/5+gap]]
ob6 = Obstacles(vw6)
vw7 = [[WIDTH/2,HEIGHT/2-wallThikness],[WIDTH/2,HEIGHT/2+wallThikness],[WIDTH/5,HEIGHT/2+wallThikness],[WIDTH/5,HEIGHT/2-wallThikness]]
ob7 = Obstacles(vw7)
vw8 = [[-1,HEIGHT/2-wallThikness],[-1,HEIGHT/2+wallThikness],[WIDTH/5-gap,HEIGHT/2+wallThikness],[WIDTH/5-gap,HEIGHT/2-wallThikness]]
ob8 = Obstacles(vw8)


wall_list.append(ob1)
wall_list.append(ob2)
wall_list.append(ob3)
wall_list.append(ob4)
wall_list.append(ob5)
wall_list.append(ob6)
wall_list.append(ob7)
wall_list.append(ob8)
#--------------------- Helper Functions ---------------------------

#-------------- Enviroment Class --------------------------------------
class Enviroment(object):
    def __init__(self,obj,room_list,wall_list,agent,goal_states,reward_f=None,terminate_f=None):
        self.displaySurface = pygame.display.set_mode((WIDTH,HEIGHT))
        
        pygame.init()
        pygame.display.set_caption('Clean-up World')
        pygame.display.update()
        
        self.obj = obj
        self.room_list = room_list
        self.wall_list = wall_list
        self.robot = agent
        
        self.rewardFunction = reward_f
        self.terminationFuntion = terminate_f
        
        self.goal_states = goal_states
        
        self.optionRegions = []
        
        self._renderObjects()
        
        
    def _renderObjects(self):
        
        for r in self.room_list:
            pygame.draw.polygon(self.displaySurface,r.color,r.vertices)
            
        for w in self.wall_list:
            pygame.draw.polygon(self.displaySurface,w.color,w.vertices)

        pygame.draw.polygon(self.displaySurface,self.obj.color,self.obj.vertices)
            
        pygame.draw.polygon(self.displaySurface,self.robot.color,self.robot.vertices)
                
        for traj in self.optionRegions:
            for orc in traj:
                pygame.draw.circle(self.displaySurface, [255,0,0], orc, 1, 0)
        
        pygame.display.update()
        
    def _check4Collisions(self,objList):
        for o in objList:
            for w in self.wall_list:
                if w.collision(o):
                    return True
        return False
        
    def outofBound(self,objList):
        boundaryVertices = [[0,0],[WIDTH,0],[WIDTH,HEIGHT],[0,HEIGHT]]
        #boundaryVertices = vr4
        
        o_path = mplPath.Path(np.array(boundaryVertices))
        
        for o in objList:
            if not o_path.contains_point(o.center,radius=1):
                
                return True

        return False
        
    def op_outofBound(self,s,o):
        if not tuple(s) in o.init:
            return True
        return False
        
        
    def _termation(self,s):
        rb_s = [s[0],s[1]]
        if rb_s in self.goal_states:
            return True
        return False
        
    def reset(self,r,o):
        self.robot.move2(r)
        self.obj.move2(o)
        
        self._renderObjects()

        return self.robot.center
        
    def set_goal(self,goalList):
        self.goal_states = goalList
    
    def set_optionRegions(self,regionList):
        self.optionRegions = regionList
        
    def step(self,action):
        
        contact, align = self.robot.inContact(self.obj)
        

        if((action == 0 and align == 'bottom') or (action == 1 and align == 'top') or (action == 3 and align == 'right') or (action == 2 and align == 'left')):
            
            self.robot.moveObject(self.obj,action2Speed[actionSpace[action]])
            collide = self._check4Collisions([self.robot,self.obj])
            out_bound = self.outofBound([self.robot,self.obj])
            
            if (collide or out_bound):
                newAction = [-1*x for x in action2Speed[actionSpace[action]]]
                self.robot.moveObject(self.obj,newAction)
        else:
           
            self.robot.move(action2Speed[actionSpace[action]])
            collide = self._check4Collisions([self.robot])
            out_bound = self.outofBound([self.robot])
            if (collide or out_bound):
                newAction = [-1*x for x in action2Speed[actionSpace[action]]]
                self.robot.move(newAction)
            
    
        self._renderObjects()
        
        s_t = [self.robot.center[0],self.robot.center[1]]
        
        done = self._termation(s_t)
        
        if done:
            reward = 200
        elif collide:
            reward = -5
        else:
            reward = -1
        
        return (s_t,reward,done)
        
        
    def op_step(self,action,o):
        
        contact, align = self.robot.inContact(self.obj)
        

        if((action == 0 and align == 'bottom') or (action == 1 and align == 'top') or (action == 3 and align == 'right') or (action == 2 and align == 'left')):
            
            self.robot.moveObject(self.obj,action2Speed[actionSpace[action]])
            collide = self._check4Collisions([self.robot,self.obj])
            out_bound = self.outofBound([self.robot,self.obj])
            op_outBound = self.op_outofBound(self.robot.center,o)
            if (collide or out_bound or op_outBound):
                newAction = [-1*x for x in action2Speed[actionSpace[action]]]
                self.robot.moveObject(self.obj,newAction)
        else:
           
            self.robot.move(action2Speed[actionSpace[action]])
            collide = self._check4Collisions([self.robot])
            out_bound = self.outofBound([self.robot])
            op_outBound = self.op_outofBound(self.robot.center,o)
            
            if (collide or out_bound or op_outBound):
                newAction = [-1*x for x in action2Speed[actionSpace[action]]]
                self.robot.move(newAction)
            
        #self._renderObjects()
        
        s_t = [self.robot.center[0],self.robot.center[1]]
        
        #print s_t, o.termination, s_t in o.termination
        
        if s_t in o.termination:
            done = True
        else:
            done = False
            
        if (done and self.goal_states == o.termination):
            reward = 20
        elif collide:
            reward = -50
        else:
            reward = -1
        
        return (s_t,reward,done)
        
        
    def vi_step(self,s,action,o):
        
        temp_r = Agent('red',s)
        
        #print "before action: ",temp_r.center
        
        temp_r.move(action2Speed[actionSpace[action]])
        
        #print "after action: ",temp_r.center
        
        collide = self._check4Collisions([temp_r])
        out_bound = self.outofBound([temp_r])
        op_outBound = self.op_outofBound(temp_r.center,o)
        
        if (collide or out_bound or op_outBound):
                newAction = [-1*x for x in action2Speed[actionSpace[action]]]
                temp_r.move(newAction)
      
        s_t = [temp_r.center[0],temp_r.center[1]]
        
        if s_t in self.goal_states:
            done = True
        else:
            done = False
            
        if (done):
            reward = 1
        elif collide:
            reward = -5
        elif (out_bound or op_outBound):
            reward = None
        else:
            reward = -1
        #print "inside step: ", s,action,s_t,reward
        return reward,tuple(s_t),done
        
        
    def usevi_step(self,s,action,o):
        v = o#o.policy
        
        temp_r = Agent('red',s)
        
        temp_r.move(action2Speed[actionSpace[action]])
        
        collide = self._check4Collisions([temp_r])
        out_bound = self.outofBound([temp_r])
        
        op_outBound = False
        if not tuple(temp_r.center) in v.keys():
            op_outBound = True
        
        if (collide or out_bound or op_outBound):
                newAction = [-1*x for x in action2Speed[actionSpace[action]]]
                temp_r.move(newAction)
      
        s_t = [temp_r.center[0],temp_r.center[1]]
        
       
        if collide:
            reward = -5
        elif s_t in self.goal_states:
            reward = v[tuple(s_t)]
        elif (out_bound or op_outBound):
            reward = None
        else:
            reward = v[tuple(s_t)]
        
        return reward,tuple(s_t)
        
        
    