#!/usr/bin/env python
#NOTE: To run, SSH in with -X flag so that pygame console can be run.
import pygame as pg
import sys
import rospy
import subprocess
import os
from race.msg import drive_param  # import the custom message


CLOCK_TICK = 100  # frames per second: number of messages we wish to publish per sec
STOP = 9780
MAX_SPEED_VEC = 10080
MIN_SPEED_VEC = 9480
DELTA_DIRECTION = 10
DELTA_SPEED_DRIVE = 295
DELTA_SPEED_ACCELERATE = 800
ACCELERATION_PERIOD = 30
# bash command for bagging data using this topic.
#BASH_CMD = "rosbag record drive_parameters"
#BAG_DIR = "/media/ubuntu/9C33-6BBD1/bagfiles"
#CURR_DIR = "/home/ubuntu/catkin_ws/src/week1tutorial/src"
#os.chdir(BAG_DIR)
#process = subprocess.Popen(BASH_CMD, shell=True) #stdout=subprocess.PIPE)
#output, error = process.communicate()
#os.chdir(CURR_DIR)


def drive():
    pg.display.set_mode((400, 300))
    rospy.init_node('keyboard_talker', anonymous=True)
    pub = rospy.Publisher('drive_parameters', drive_param, queue_size=10)
    pg.init()
    clock = pg.time.Clock()
    speed = STOP
    direction = 0
    # states of keys: 0 indicates up, 1 is down.
    kUp = kDown = kLeft = kRight = 0
    run = True
    down = False
    cycles_since_stop = 0
    accelerate = False
    while run:
        # reset values
        speed = STOP
        direction = 0
        terminate = False
        # stall here
        clock.tick(CLOCK_TICK)
        for event in pg.event.get():
            # no elifs
            # just care about the keydown&keyup events
            if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                key = event.key
                down = int(event.type == pg.KEYDOWN)
                up = int(event.type == pg.KEYUP)
                if key == pg.K_LEFT:
                    kLeft = down
                if key == pg.K_RIGHT:
                    kRight = down
                if key == pg.K_UP:
                    kUp = down
                    cycles_since_stop = 0
                if key == pg.K_DOWN:
                    kDown = down
                    cycles_since_stop = 0
                if key == pg.K_q:
                    terminate = True

        msg = drive_param()
        # reset speed & direction accordingly.
        if terminate:
            msg.velocity = STOP
            msg.angle = 0
            pub.publish(msg)
            #process.kill()
            return

        cycles_since_stop += 1

        if cycles_since_stop < ACCELERATION_PERIOD:
            speed += DELTA_SPEED_ACCELERATE * (kUp - kDown)
        else:
            speed += DELTA_SPEED_DRIVE * (kUp - kDown)
        direction += DELTA_DIRECTION * (kRight - kLeft)
        msg.velocity = speed
        msg.angle = direction
        # print(kUp, kDown, kLeft, kRight)
        # print(speed, direction)
        # sys.stdout.flush()
        pub.publish(msg)


def main():
    drive()


main()

