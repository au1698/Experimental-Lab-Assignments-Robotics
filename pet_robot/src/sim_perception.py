#! /usr/bin/python
# -*- coding: utf-8 -*-

import random 
import numpy as np
import matplotlib.pyplot as plt
import rospy 
from std_msgs.msg import Int64MultiArray
from std_msgs.msg import String
import time


def  Simulator (): 
     
     global user_comand 
     
     while not rospy.is_shutdown():
         # 2D coordinates generation (pointed gestures)
         x = np.random.randint(0, 50, 1)
         y = np.random.randint(0, 50, 1)
         array_point =np.array([x,y]) 
     
        # User comands (speak interaction and pointed gestures)
         user_comand = random.choice(['go_to_home','play', array_point]) 
         print (user_comand)
     
         # Declare Publisher   
         vocal_comand_pub = rospy.Publisher('/vocal_comand', String, queue_size=10)
         pointed_comand_pub = rospy.Publisher('/pointed_comand', Int64MultiArray, queue_size=10)

         # Inizialize the node   
         rospy.init_node('sim_perception', anonymous=True)

         # inizialize the variable which contains the 2D point
         pointed_comand = Int64MultiArray()      
         
         # Check if "user_comand" is a string or an array
         if type(user_comand) == str:   
             rospy.loginfo(user_comand)
             vocal_comand_pub.publish(user_comand)  
             time.sleep(25)

         else: 
             pointed_comand.data = user_comand
             rospy.loginfo(pointed_comand)
             pointed_comand_pub.publish(pointed_comand)
             time.sleep(25)
         

if __name__ == '__main__':
    try:
         Simulator ()
    except rospy.ROSInterruptException: 
         pass
         

        
        