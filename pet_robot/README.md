# Behavioral Architecture
The scenario describes behavior simulation of a pet robot that interacts with humans and moves in a discrete 2D environment. 
The human can interact doing speech comands and pointing gestures. 

## ROS Architecture of the System
The “Gesture Sequence Generator” module is the implementation of the server of a service-client
pattern; the “Experimenter GUI” represents all the graphical part of the architecture (divided into “Configuration UI”, which contains the management of the recording’s configuration, and
“Communication with User UI”, where the user can control the recording and where images and
time elapsed are displayed); the three “Sensor Modules” collect data from the sensors (MOCAP,
Smartwatch and Kinect) and when they receive the signals from the Experimenter_GUI, they
publish datas in a topics (one for each type of message); the three “Record Modules” read data
from the topics published by the Sensor Modules and record them into a Rosbags; the
“Conversion and Segmentation” module is commissioned to convert the data from “rosbag” to
“csv” format, to assign certain labels to it and to segment them.

<p align="center"> 
<img src="https://github.com/FraPorta/Itslit/blob/master/ExperimenterDiagram.jpg?raw=true">
</p>

## Contents of the repository
In this section we will explain the repository's content.


### Launch
This folder contains a launchfile: one executes the whole application and the other one executes the nodes which mimic the hardware's functioning.

### Msg
This folder contains the ".msg" file needed for the gesture sequence structure that is saved in a rosbag.

### Src
This folder contains all the nodes that make up the main program: "GUI_node" initializes the GUI and deals with the logic behind the graphical elements, which makes the user navigate between windows, write personal informations, select which sensors to use, and so on; the "gestures_nodes" implements the server which manages the request for a random gesture sequence; the "fake_node_imu" creates fake simulated data from the Smartwatch; the "Smartwatch_node" manages data from Smartwatch sensor: it saves data when it is required by user; the "Recorder_IMU" saves data Imu into a Rosbag; the "fake_node_pc" create fake simulated data from the Kinect; the "kinect_node" manages data from Kinect sensor: it saves data when it is required by user; the "Recorder_PC" saves data PointCloud2 into a Rosbag; the "mocap_fake" creates fake simulated data from the Mocap; the "Mocap_node" manages data from Mocap sensor: it saves data when it is required by user; the "Recorder_mocap" saves Mocap data into a Rosbag. 
In addition to these 2 files, there's also the following folder.

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


# Rqt_graph
<p align="center"> 
<img src="https://github.com/FraPorta/Itslit/blob/master/rqt.png?raw=true">
</p>

### Modules
* "Experimenter_GUI" Module
* "Gesture Sequence Generator" Module
* "Fake Imu" Module
* "Smartwatch" Module
* "Fake PointCloud2" Module
* "Kinect" Module
* "Recorder Imu" Module
* "Recorder PC" Module
* "Recorder Mocap" Module
* "mocap fake" Module
* "Mocap node" Module
* "Conversion and Segmentation" Module

Author: 

Aurora Bertino 
