#!/usr/bin/env python
#NOTE: To run, SSH in with -X flag so that pygame console can be run.
import pygame as pg
import sys
import rospy
import subprocess
import os
import math
import numpy as np
import time
from race.msg import drive_param  # import the custom message
from geometry_msgs.msg import Point, PoseStamped
from std_msgs.msg import String
from multiprocessing import Process, Value, Array

FPS = 100  # frames per second: number of messages we wish to publish per sec
COMMUNICATOR_SLEEP_MILLIS = 10    # period for sending/receiving waypoint/acks.
STOP = 9780
MAX_SPEED_VEC = 10080
MIN_SPEED_VEC = 9480
DELTA_DIRECTION = 12
DELTA_SPEED_DRIVE = 300
DELTA_SPEED_ACCELERATE = 800
ACCELERATION_PERIOD = 30
EPSILON_RADIUS = .4
EPSILON_ANGLE = .1
INITIAL_RUN_LOOPS = 5
# bash command for bagging data using this topic.
#BASH_CMD = "rosbag record drive_parameters"
#BAG_DIR = "/media/ubuntu/9C33-6BBD1/bagfiles"
#CURR_DIR = "/home/ubuntu/catkin_ws/src/week1tutorial/src"
#os.chdir(BAG_DIR) 
#process = subprocess.Popen(BASH_CMD, shell=True) #stdout=subprocess.PIPE)
#output, error = process.communicate()
#os.chdir(CURR_DIR)

pub = rospy.Publisher('drive_parameters', drive_param, queue_size=10)  

points = [(-1.57, -.63), (2.43, 1.80), (-1.66, 2.2), (3.31, -0.2), \
        (-1.57, -.63), (2.43, 1.80), (-1.66, 2.2), (3.31, -0.2), \
        (-1.57, -.63), (2.43, 1.80), (-1.66, 2.2), (3.31, -0.2)]
pos = [0, 0]


def deca_callback(data):
    pos[0] = data.x
    pos[1] = data.y

def vicon_callback(data):
    pos[0] = data.pose.position.x
    pos[1] = data.pose.position.y

def get_distance(pos_prev, pos_curr):
waypoint.py
