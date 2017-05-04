#!/usr/bin/env python
# NOTE: To run, SSH in with -X flag so that pygame console can be run.
import pygame as pg
import sys
import rospy
from race.msg import drive_param  # import the custom message


CLOCK_TICK = 100  # frames per second: number of messages we wish to publish per sec
STOP = 9780
MAX_SPEED_VEC = 10080
MIN_SPEED_VEC = 9480
DELTA_DIRECTION = 10
DELTA_SPEED = 295


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
                if key == pg.K_LEFT:
                    # once the execution reaches here, we know sth happened to left.
                    # set to 1 if it's a keydown, 0 o/w.
                    kLeft = down
                if key == pg.K_RIGHT:
                    kRight = down
                if key == pg.K_UP:
                    kUp = down
                if key == pg.K_DOWN:
                    kDown = down
                if key == pg.K_q:
                    terminate = True

        msg = drive_param()
        # reset speed & direction accordingly.
        if terminate:
            msg.velocity = STOP
            msg.angle = 0
            pub.publish(msg)
            return

        speed += DELTA_SPEED * (kUp - kDown)
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
