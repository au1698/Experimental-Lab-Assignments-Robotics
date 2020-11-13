#! /usr/bin/python
# -*- coding: utf-8 -*-

## @file sim_perception.py 
# @brief This node simulates user's comands  


import random 
import numpy as np
import matplotlib.pyplot as plt
import rospy 
from std_msgs.msg import Int64MultiArray
from std_msgs.msg import String
import time

## @file sim_perception.py 
# @brief This node simulates user's comands generation. 
# 
# Details: It generates a vector (pointed gesture)in which there are coordinates x,y and randomly choose between vocal comands
# 'play', 'go_to_home' and the vector.  
# 

def  Simulator (): 
     
     global user_comand 
     
     while not rospy.is_shutdown():
         ## 2D coordinates generation (pointed gestures)
         x = np.random.randint(0, 50, 1)
         y = np.random.randint(0, 50, 1)
         array_point =np.array([x,y]) 
     
        ## User comands (speak interaction and pointed gestures)
         user_comand = random.choice(['go_to_home','play', array_point]) 
         print (user_comand)
     
         ## Declare Publisher   
         vocal_comand_pub = rospy.Publisher('/vocal_comand', String, queue_size=10)
         pointed_comand_pub = rospy.Publisher('/pointed_comand', Int64MultiArray, queue_size=10)

         ## Inizialize the node   
         rospy.init_node('sim_perception', anonymous=True)

         ## Inizialize the variable which contains the 2D point
         pointed_comand = Int64MultiArray()      
         
         ## Check if "user_comand" is a string or an array
         if type(user_comand) == str:   
             rospy.loginfo(user_comand)
             ## Publish 'user_comand' on the topic '/vocal_comand'
             vocal_comand_pub.publish(user_comand)  
             time.sleep(25)

         else: 
             pointed_comand.data = user_comand
             rospy.loginfo(pointed_comand)
             ## Publish 'user_comand' on the topic '/pointed_comand'
             pointed_comand_pub.publish(pointed_comand)
             time.sleep(25)
         

if __name__ == '__main__':
    try:
         Simulator ()
    except rospy.ROSInterruptException: 
         pass
         

        
        