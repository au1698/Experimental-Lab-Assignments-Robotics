# Behavioral Architecture
The scenario describes a behavior simulation of a pet robot that interacts with humans and moves in a discrete 2D environment. 
The human can interact with the robot through speech comands and pointing gestures while the robot can have three beaviors: sleep, play, normal.

## ROS Architecture of the System
The system is made by three ros nodes: "sim_perception.py", "pet_state_machine.py" and "display_position.py". 
The rqt_graph is shown below.

## 

<p align="center"> 
<img src="https://github.com/FraPorta/Itslit/blob/master/ExperimenterDiagram.jpg?raw=true">
</p>


## Installation
The first thing to do, after having cloned the repository in the Ros workspace, is to build the package in your workspace. 
    ```
    catkin_make
    ```

To run the system:
    
    ```
    roslaunch pet_robot pet_robot_launch.launch
    
    ```
To visualize the Smach Viewer:

    ```
 rosrun smach_viewer smach_viewer.py
    
    ```

## Rqt_graph
<p align="center"> 
<img src=https://github.com/au1698/Experimental-Lab-Assignments-Robotics/blob/main/pet_robot/Images/rqt_graph_pet_robot.png raw=true">
</p>

## Working hypoteses
The gesture commands present the same "priority" since they occur in random order.
The home position is fixed (0,0).
## System's limitations
There is not a simulator.

## Possible improvements
Use the ROS parameter service to define a parameter to scale the simulation velocity. 
Using a service-client as kind of comunication between the simulation node and the state machine in order to improve the synchronization. ye


## Author: 

Aurora Bertino 
