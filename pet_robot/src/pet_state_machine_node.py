#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

# INSTALLATION
# - move this file to the 'smach_tutorial/scr' folder and give running permissions to it with
#          $ chmod +x pet_state_machine.py
# - run the 'roscore' and then you can run the state machine with
#          $ rosrun smach_tutorial pet_state_machine.py
# - run the visualiser with
# rosrun smach_viewer smach_viewer.py


# finite state machine defines only interaction (I/O) between the states (noded of a state machine)

array_point = np.array([0,0])
target_pub = rospy.Publisher('/target_point', Int64MultiArray, queue_size=10)
vocal_data = ""


def callback_vocal_comand(data):
     #target_pub = rospy.Publisher('/target_point', Int64MultiArray, queue_size=10)
     # se arriva il messaggio al topic "vocal_comand"
     # traslate "vocal comands" into 2D coordinates
     global vocal_data
     if len (data.data) == 0:
         rospy.logwarn("data empty")
         return 
     else:
         vocal_data = data.data
         
     #if data  == 'go_to_home':  
             #x = np.random.randint(0, 50, 1)
             #y = np.random.randint(0, 50, 1)
             #array_point =np.array([x,y]) 
             # chiama la funzione "get_position" create a publisher 
             #array_point = (0,0)             #home position   
             #target_pub.publish(array_point)
             #print ('active function "go_to_home')
         
     #else: 
         


def callback_pointed_comand(data):
     #target_pub = rospy.Publisher('/target_point', Int64MultiArray, queue_size=10)
     # save inside an array the 2D position
     array_point = data
     target_pub.publish(array_point)
     time.sleep(5)
     print ('active function "go_to_target',array_point)
     if len (data.data) == 0:
         rospy.logwarn("data empty")
         return 
     



# define state  Sleep
class Sleep(smach.State):
    def __init__(self):       # costructor
    # initialisation function, it should not wait   
        smach.State.__init__(self, 
                        outcomes=['wake_up'],
                        input_keys=['sleep_counter_in'],
                        output_keys=['sleep_counter_out'])


    def execute(self,userdata):
    # qui faccio il subscribe/ aspetto dati da sensori, dove faccio il wait
        time.sleep(5)
        rospy.loginfo('Executing state SLEEP')
        userdata.sleep_counter_out = userdata.sleep_counter_in + 1  

    # SE RICEVO DAL ROS PARAMETER SERVER CHE HO HO RAGIUNTO LA "TARGET POSITION"
    # -> SUBSCRIBE NODO (VOCAL COMAND OR POINTED COMAND)
        #reached_target = rospy . get_param ( '/bool_True' )
        
        #target = rospy.get_param('/another_integer')
        #if target == True :
         # define the publisher (target_point)
        #target_pub = rospy.Publisher('/target_point', Int64MultiArray, queue_size=10)
        #rospy.Subscriber("/pointed_comand",Int64MultiArray, callback_pointed_comand)

        # Comand that let the robot go home
        home_comand = Int64MultiArray()     #inizialize the variable 
        home_comand.data = np.array([0,0])  # home position 
        target_pub.publish(home_comand)
        rospy.loginfo('The robot is reaching home position')
        time.sleep(15)
        rospy.Subscriber("/vocal_comand",String, callback_vocal_comand) 
        if vocal_data  == 'go_to_home': # se mi riposo e mi arriva il comando "continua a riposare"
         time.sleep(5)
         rospy.loginfo('THe robot is at home')
        else:
   
             time.sleep(4)  
        
    # CAMBIA STATO -> NORMAL 
        return 'wake_up'


class Normal(smach.State):
    def __init__(self):       # costructor
    # initialisation function, it should not wait   
        smach.State.__init__(self, 
                        outcomes=['go_to_sleep','go_to_play'],
                        input_keys=['normal_counter_in'],
                        output_keys=['normal_counter_out'])

    def execute(self,userdata):
    # qui faccio il subscribe/ aspetto dati da sensori, dove faccio il wait
        time.sleep(5)
        rospy.loginfo('Executing state NORMAL')
        userdata.normal_counter_out = userdata.normal_counter_in + 1  
        for i in range(0, 3):
         # in this state the robot moves randomly 
             x = np.random.randint(0, 50, 1)
             y = np.random.randint(0, 50, 1)
             move_random = Int64MultiArray() 
             move_random.data = np.array([x,y])
             target_pub.publish(move_random) 
             time.sleep(8)  
        # USER ACTIONS 
        rospy.Subscriber("/pointed_comand",Int64MultiArray, callback_pointed_comand)
        rospy.Subscriber("/vocal_comand",String, callback_vocal_comand) 
        #rospy.Subscriber("/pointed_comand",Int64MultiArray, callback_pointed_comand)
        if (vocal_data == 'go_to_sleep'):

             return 'go_to_sleep'
             rospy.loginfo('User decides to go to home')
        if (vocal_data == 'play'):
            rospy.loginfo('User decides to go to play')
            return 'go_to_play' 

        time.sleep(4)       
    # scegli random se attivare SLEEP o PLAY
        return random.choice(['go_to_sleep','go_to_play']) 
                


class Play(smach.State):
    def __init__(self):       # costructor
    # initialisation function, it should not wait   
        smach.State.__init__(self, 
                         outcomes=['go_to_sleep','go_to_normal'],
                         input_keys=['play_counter_in'],
                         output_keys=['play_counter_out'])

    def execute(self,userdata):
    # qui faccio il subscribe/ aspetto dati da sensori, dove faccio il wait
        #time.sleep(5)
        rospy.loginfo('Executing state PLAY')
        userdata.play_counter_out = userdata.play_counter_in + 1 
        person_position = Int64MultiArray()  #inizialize the variable 
        x = np.random.randint(0, 50, 1)
        y = np.random.randint(0, 50, 1)  
        person_position.data = np.array([x,y])
        target_pub.publish(person_position)     # vai dove si trova la persona 
        rospy.loginfo('The robot is reaching person position')
        time.sleep(5)
        rospy.loginfo('The robot is waiting for a pointing gesture')
        time.sleep(7)
        #rospy.Subscriber("/vocal_comand",String, callback_vocal_comand) 
        #rospy.Subscriber("/pointed_comand",Int64MultiArray, callback_pointed_comand)
        while True:
             rospy.Subscriber("/vocal_comand",String, callback_vocal_comand) 
             if (vocal_data == 'go_to_home' or  vocal_data == 'play'):
                 time.sleep(5)  
                 rospy.loginfo('ERROR: I am waiting for a pointing gesture')
             #rospy.Subscriber("/pointed_comand",Int64MultiArray, callback_pointed_comand)
             if (len (vocal_data)) == 0:
                 rospy.Subscriber("/pointed_comand",Int64MultiArray, callback_pointed_comand)
                 #rospy.loginfo('The robot is reaching the pointed location')
                 time.sleep(5)
                 break 
        #rospy.Subscriber("/vocal_comand",String, callback_vocal_comand) 
        #if (vocal_data == 'go_to_sleep'):
            #return 'go_to_sleep'
        #time.sleep(5)
    # scegli random se attivare SLEEP o PLAY
        return  random.choice(['go_to_sleep','go_to_normal'])
            

        
def main():    # configuration of the state machine
    rospy.init_node('pet_state_machine')   #inizializzo nodo ros
    
     # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['container_interface'])   # SINTASSI = libreria.funzione
    sm.userdata.sm_counter = 0


     # Open the container
    with sm:
         # Add states to the container
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
                               transitions={'go_to_sleep':'SLEEP',
                                            'go_to_normal':'NORMAL'}, 
                                            
                                            
                               remapping={'play_counter_in':'sm_counter',
                                          'play_counter_out':'sm_counter'})
                                



    # Create and start the introspection server for visualization
    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()

    # Execute the state machine
    outcome = sm.execute()

    # Wait for ctrl-c to stop the application
    rospy.spin()
    sis.stop()

if __name__ == '__main__':
     main()
                               