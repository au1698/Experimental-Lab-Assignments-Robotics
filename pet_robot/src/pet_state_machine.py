#!/usr/bin/env python
# -*- coding: utf-8 -*-

## @file pet_state_machine.py 
# @brief This node implements a state machine. 
# 
# Details: It receives commands 'sim_perception' node, implements the state machine and sends the target positions to 'display_position' node.
# 
  

import roslib
import rospy
import smach
import smach_ros
import time
import random
import rospy
import numpy as np
from std_msgs.msg import Int64MultiArray
from std_msgs.msg import String

array_point = np.array([0,0])
target_pub = rospy.Publisher('/target_point', Int64MultiArray, queue_size=10)
vocal_data = ""

## Define callback function: vocal_comand()
def callback_vocal_comand(data):
     global vocal_data
     if len (data.data) == 0:
         rospy.logwarn("data empty")
         return 
     else:
         vocal_data = data.data
         
         
## Define callback function: pointed_comand()
def callback_pointed_comand(data):
    global array_point
    if len (data.data) == 0:
         rospy.logwarn("data empty")
         return 
    ## Save the 2D position
    array_point = data
    ## Publish target position on topic '/target_point'
    target_pub.publish(array_point)
    time.sleep(5)
    rospy.loginfo('The robot is reaching the pointed location')
    print ('active function "go_to_target',array_point)

     
## Define state Sleep
class Sleep(smach.State):
    ## Constructor of the class Sleep
    def __init__(self):       
    ## Initialization function 
        smach.State.__init__(self, 
                        outcomes=['wake_up'],
                        input_keys=['sleep_counter_in'],
                        output_keys=['sleep_counter_out'])


    def execute(self,userdata):
        time.sleep(5)
        rospy.loginfo('Executing state SLEEP')
        userdata.sleep_counter_out = userdata.sleep_counter_in + 1  

        ## Comand that let the robot go home
        home_comand = Int64MultiArray()     
        ## Define home position 
        home_comand.data = np.array([0,0]) 
        ## Publish home position on topic '/target_point'
        target_pub.publish(home_comand)
        rospy.loginfo('The robot is reaching home position')
        time.sleep(15)
        ## Subscribe to the topic '/vocal_comand'
        rospy.Subscriber("/vocal_comand",String, callback_vocal_comand) 
        if vocal_data  == 'go_to_home': 
         time.sleep(5)
         rospy.loginfo('The robot is already at home')
        else:
   
             time.sleep(4)  
        
    ## Change state: from 'SLEEP' to 'NORMAL'  
        return 'wake_up'

## Define state Normal
class Normal(smach.State):
    ## Constructor of the class Normal
    def __init__(self):     
    ## Initialization function 
        smach.State.__init__(self, 
                        outcomes=['go_to_sleep','go_to_play'],
                        input_keys=['normal_counter_in'],
                        output_keys=['normal_counter_out'])

    def execute(self,userdata):
        time.sleep(5)
        rospy.loginfo('Executing state NORMAL')
        userdata.normal_counter_out = userdata.normal_counter_in + 1  
        ## The robot moves randomly 
        for i in range(0, 3):
             x = np.random.randint(0, 50, 1)
             y = np.random.randint(0, 50, 1)
             move_random = Int64MultiArray() 
             move_random.data = np.array([x,y])
             ## Publish random position on topic '/target_point'
             target_pub.publish(move_random) 
             time.sleep(8)  
        ## Subscribe to the topic '/vocal_comand' and '/pointed_comand'
        rospy.Subscriber("/pointed_comand",Int64MultiArray, callback_pointed_comand)
        rospy.Subscriber("/vocal_comand",String, callback_vocal_comand) 

        if (vocal_data == 'go_to_home'):
         ## Check on user's vocal comands
             return 'go_to_sleep'
             rospy.loginfo('User decides to go to home')
        if (vocal_data == 'play'):
            rospy.loginfo('User decides to go to play')
            return 'go_to_play' 

        time.sleep(4)       
    ## Change state randomly: from 'NORMAL' to 'SLEEP' or 'PLAY'   
        return random.choice(['go_to_sleep','go_to_play']) 
                
## Define state Play 
class Play(smach.State):
    ## Constructor of the class Play
    def __init__(self):       
    ## Initialization function   
        smach.State.__init__(self, 
                         outcomes=['go_to_normal'],
                         input_keys=['play_counter_in'],
                         output_keys=['play_counter_out'])

    def execute(self,userdata):
        time.sleep(5)
        rospy.loginfo('Executing state PLAY')
        userdata.play_counter_out = userdata.play_counter_in + 1 
        person_position = Int64MultiArray()  
        ## Define random person position
        x = np.random.randint(0, 50, 1)
        y = np.random.randint(0, 50, 1)  
        person_position.data = np.array([x,y])
        ## Publish person position randomly on topic '/target_point'
        target_pub.publish(person_position)     
        rospy.loginfo('The robot is reaching person position')
        time.sleep(5)
        rospy.loginfo('The robot is waiting for a pointing gesture')
        time.sleep(10)
        while True:
             ## Subscribe to the topic '/vocal_comand' 
             rospy.Subscriber("/vocal_comand",String, callback_vocal_comand) 
             if (vocal_data == 'go_to_home' or  vocal_data == 'play'):
                 rospy.loginfo('ERROR: I am waiting for a pointing gesture')
                 time.sleep(5) 
             else: 
             ## Subscribe to the topic '/pointed_comand'
                 rospy.Subscriber("/pointed_comand",Int64MultiArray, callback_pointed_comand)
                 time.sleep(5) 
             break 
      
        time.sleep(5)
    ## Change state randomly: from 'PLAY' to 'NORMAL' 
        return  'go_to_normal'
            

        
def main():    
    ## Inizialize ros node ''pet_state_machine'
    rospy.init_node('pet_state_machine')   
    
    ## Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['container_interface'])   
    sm.userdata.sm_counter = 0
    
    ## Open state machine container
    with sm:
         ## Add states to the container
         smach.StateMachine.add('SLEEP', Sleep(),
                                  
                               transitions={'wake_up':'NORMAL'},
                                                                
                                            
                               remapping={'sleep_counter_in':'sm_counter', 
                                         'sleep_counter_out':'sm_counter'})
         smach.StateMachine.add('NORMAL', Normal(), 
                               transitions={'go_to_sleep':'SLEEP',
                                            'go_to_play' :'PLAY'},
                                            
                                            
                               remapping={'normal_counter_in':'sm_counter',
                                          'normal_counter_out':'sm_counter'})

         smach.StateMachine.add('PLAY', Play(), 
                               transitions={'go_to_normal':'NORMAL'}, 
                                            
                                            
                               remapping={'play_counter_in':'sm_counter',
                                          'play_counter_out':'sm_counter'})
                                



    ## Create and start the introspection server for visualization
    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()

    ## Execute the state machine
    outcome = sm.execute()

    ## Wait for ctrl-c to stop the application
    rospy.spin()
    sis.stop()

if __name__ == '__main__':
     main()
                               