# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 22:55:55 2017

@author: monica
"""

from Env_cleanupWorld import *
from option_utils import *


vo11 = load_obj('vo11')
vo12 = load_obj('vo12')
vo21 = load_obj('vo21')
vo22 = load_obj('vo22')
vo31 = load_obj('vo31')
vo32 = load_obj('vo32')
vo41 = load_obj('vo41')
vo42 = load_obj('vo42')

option_list = [vo11,vo12,vo21,vo22,vo31,vo32,vo41,vo42]

for vo in option_list:
    print "Initiation: ",vo.init
    print "Termination: ",vo.termination
    print "-----------------------------------"