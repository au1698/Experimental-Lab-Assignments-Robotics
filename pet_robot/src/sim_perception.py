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
         #target = rospy.get_param('/another_integer')
         #if target == True :
         x = np.random.randint(0, 50, 1)
         y = np.random.randint(0, 50, 1)
         array_point =np.array([x,y])

         #print(array_point)
         #else: 
             #time.sleep(5)  
         #plt.scatter(x, y)
         #plt.show()

         #p2 = Point(x,y)       # create an object point
     
         # 2D coordinates generation (speak interaction)
         user_comand = random.choice(['go_to_home','play', array_point]) 
         print (user_comand)
     
         # Declare Publisher ('name_topic','type msg')   
         vocal_comand_pub = rospy.Publisher('/vocal_comand', String, queue_size=10)
         pointed_comand_pub = rospy.Publisher('/pointed_comand', Int64MultiArray, queue_size=10)

         # Inizialize the node   
         rospy.init_node('sim_perception', anonymous=True)
     
         #rate = rospy.Rate(10) # 10hz ( make loop 10 times for sec)

         pointed_comand = Int64MultiArray()      # inizialize the variable which contains the 2D point
         #pointed_comand = []                    # inizialize the empty array
     
         # Inizialize standard msg 
         # vocal_comand = String()
         # while user_comand is None:  # aspetta, finchè non hai raggiunto il target (ROS PARAMETER SERVICE)
             # time.sleep(15)
         # until the node is active

         if type(user_comand) == str:    #check if "user_comand" is a string o something else
             #vocal_comand.data = user_comand 
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
         

        
        