# Behavioral Architecture
The scenario describes a behavior simulation of a pet robot that interacts with humans and moves in a discrete 2D environment. 
The human can interact with the robot through speech comands and pointing gestures while the robot can have three beaviors: sleep, play, normal.

## ROS Architecture of the System
The system is made by three ros nodes: "sim_perception.py", "pet_state_machine.py" and "display_position.py". 
The rqt_graph is shown below.

# Rqt_graph
<p align="center"> 
<img src=https://github.com/au1698/Experimental-Lab-Assignments-Robotics.git/rqt_graph_pet_robot.png? raw=true">
</p>

## sim_perception
This node until is active simulates user's random choice between a pointing gesture (2D coordinates generation) and the vocal comands: 'go_to_home' and 'play'. 
It prints on the screen user's choice. 
Pointed gesture is of type 'Int64MultiArray' while vocal comands are simply of the type 'string'.
It checks if "user_comand" is a string or an array. In the first case "user_comand" data are published on the topic /pointed_comand in the second data are published onthe topic /vocal_comand.

## pet_state_machine
This node is a finite state machine composed of three states: 

<p align="center"> 
<img src=https://github.com/au1698/Experimental-Lab-Assignments-Robotics/blob/main/pet_robot/Images/pet_state_machine.jpeg raw=true">
</p>


## How to run the code
The first thing to do, after having cloned the repository in the Ros workspace, is to build the package in your workspace. 
    ```
    catkin_make
    ```
Give running permissions to it with
    ```
    $ chmod +x
    ```

To run the system:
    
    ```
    roslaunch pet_robot pet_robot.launch
    
    ```
To visualize the Smach Viewer:

    ```
 rosrun smach_viewer smach_viewer.py
    
    ```

## Working hypoteses
The gesture commands present the same "priority" since they occur in random order.
The home position is fixed (0,0).
## System's limitations
There is not a simulator.

## Possible improvements
Use the ROS parameter service to define a parameter to scale the simulation velocity. 
Using a service-client as kind of comunication between the simulation node and the state machine in order to improve the synchronization. ye


## Author: 

* Aurora Bertino: bertino.aurora16@gmail.com
