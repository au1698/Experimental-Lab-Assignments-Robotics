#! /usr/bin/python
# -*- coding: utf-8 -*-

## @file display_position.py 
# @brief This node displays when the target position is reached. 
#
# Details: It subscribe to the topic '/target_position' and publishes when the robot arrives to the target.  
#
import rospy
import numpy as np
from std_msgs.msg import String
from random import random
import threading
import time
from std_msgs.msg import Int64MultiArray

## Define callback function: callback()
def callback(data):
     target = data.data
     ## Wait some time 
     time.sleep(4)         
     ## Display that the target is reached                
     rospy.loginfo('The target is reached ')


def position_subscribe():
     ## Inizialize the ros node 'display_position' 
     rospy.init_node('display_position', anonymous=True) 
     ## Subscribe to the topico '/target_point'
     rospy.Subscriber("/target_point",Int64MultiArray, callback)

     rospy.spin()


if __name__ == '__main__':
     position_subscribe()