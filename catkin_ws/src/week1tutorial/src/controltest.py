#!/usr/bin/env python

import rospy
from race.msg import drive_param
from race.msg import pid_input
from std_msgs.msg import String
import math

pub = rospy.Publisher('drive_parameters', drive_param, queue_size=1)

kp = 14.0 * 2
kd = 0.09 * 2
servo_offset = 18.5
prev_error = 0.0 
vel_input = 10.0
mode = 'wall'

def control(data):
    global kp
    global kd
    global servo_offset
    global prev_error
    global vel_input
    global mode

    msg = drive_param();
    msg.velocity = vel_input

    if mode == 'wall':
        pid_error = data.pid_error
        error = pid_error * kp
        errordot = kd * (pid_error - prev_error)

        angle = error + errordot

        if angle > 100:
            angle = 100
        elif angle < -100:
            angle = -100

        prev_error = pid_error

        print 'pid_error {}\nangle {}'.format(pid_error, angle)

        msg.angle = angle
        
    elif mode == 'corner':
        print 'corner mode, angle 100'
        msg.angle = 100
    
    pub.publish(msg)

def update_mode(_mode):
    global mode
    mode = _mode.data

if __name__ == '__main__':
    print("Listening to error for PID")
    rospy.init_node('pid_controller', anonymous=True)
    rospy.Subscriber('error', pid_input, control)
    rospy.Subscriber('mode', String, update_mode)
    rospy.spin()
