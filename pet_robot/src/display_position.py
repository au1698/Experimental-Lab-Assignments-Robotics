#! /usr/bin/python
# -*- coding: utf-8 -*-

import rospy
import numpy as np
from std_msgs.msg import String
from random import random
import threading
import time
from std_msgs.msg import Int64MultiArray

#target = Int64MultiArray()

def callback(data):
     target = data.data
     time.sleep(4)                         # time to arrive to the target
     rospy.loginfo('The target is reached ')


def position_subscribe():
     rospy.init_node('display_position', anonymous=True) #inizialize node
     rospy.Subscriber("/target_point",Int64MultiArray, callback)

     rospy.spin()


if __name__ == '__main__':
     position_subscribe()