#!/usr/bin/env python 
from __future__ import print_function
import rospy
import time
import os.path
from geometry_msgs.msg import Point, PoseStamped
from race.msg import drive_param

from multiprocessing import Process, Array

FPS = 100  # number of collections per second


deca_pos = Array('d', [0.0, 0.0])
vicon_pos = Array('d', [0.0, 0.0])
drive_vals = Array('d', [0.0, 0.0])
    
timestamp = time.time()

def deca_callback(data):
    deca_pos[0] = data.x
    deca_pos[1] = data.y

def vicon_callback(data):
    vicon_pos[0] = data.pose.position.x
    vicon_pos[1] = data.pose.position.y

def drive_callback(data):
    drive_vals[0] = data.velocity
    drive_vals[1] = data.angle

def write_to_file(deca_pos, vicon_pos, drive_vals):
    
    file_no = 0 
    file_name = "/home/ubuntu/catkin_ws/src/week1tutorial/src/data/data_out_{}.csv".format(file_no)
    while os.path.isfile(file_name):
        file_no += 1
        file_name = "/home/ubuntu/catkin_ws/src/week1tutorial/src/data/data_out_{}.csv".format(file_no)

    with open(file_name, "w") as f:
        while True:
            output = "{}, {}, {}, {}, {}, {}, {}\n".format(
                    time.time(),
                    deca_pos[0],
                    deca_pos[1],
                    vicon_pos[0],
                    vicon_pos[1],
                    drive_vals[0],
                    drive_vals[1])

            print(output)
            #print(output, file=f)
            time.sleep(1.0/float(FPS))
data_collect.py
