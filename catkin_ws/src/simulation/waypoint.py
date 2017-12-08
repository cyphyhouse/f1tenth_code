from glob import *
import numpy as np
import math
import time

X_INIT = 100
Y_INIT = 100
EPSILON_RADIUS = 50.0
EPSILON_ANGLE = 0.1
FREQUENCY = 1000


def get_pid_distance(d_err_curr, d_err_prev, d_err_integral):
    Kp = 1.2
    Kd = 10
    Ki = 0.001
    return Kp * d_err_curr + Kd * (d_err_curr - d_err_prev) + Ki * d_err_integral


def get_pid_angle(a_err_curr, a_err_prev, a_err_integral):
    Kp = 7
    Kd = 1
    Ki = 0.01
    return Kp * a_err_curr + Kd * (a_err_curr - a_err_prev) + Ki * a_err_integral


def track_waypoint(points, drive_signal, location_feed):
    # move for 1 second to get idea of your location & orientation

    path = []
    x_prev = -1.0
    y_prev = -1.0

    for i in range(100):
        x = location_feed[0]
        y = location_feed[1]
        if x != x_prev or y != y_prev:
            path.append((x, y))
            x = x_prev
            y = y_prev
        drive_signal[0] = MAX_SPEED_VEC
        drive_signal[1] = 0
        time.sleep(0.01)

    # stop moving (will have inertia but that's fine)
    drive_signal[0] = 0

    # get first waypoint_simulation:
    waypoint = points.pop(0)
    x_prev, y_prev = path[-1]

    # distance and angle prev values
    d_prev = 0.0
    a_prev = 0.0

    # distance and angle integrals for PID
    d_integral = 0.0
    a_integral = 0.0

    # while our list of points isn't empty
    while True:
        # get coordinates from environment
        x = location_feed[0]
        y = location_feed[1]
        if x_prev != x or y_prev != y:
            path.append((x, y))
            # print("NEW")

        # current location
        curr_loc = path[-1]
        # prev location
        prev_loc = path[-2]
        # get next position given we move as is:
        next_loc = get_next_loc(curr_loc, prev_loc)
        # print("prev_loc = {}, curr_loc = {}, next_loc = {}".format(prev_loc, curr_loc, next_loc))

        # from our next position and current position, get current polar velocity
        velocity = get_distance(next_loc, curr_loc)

        # get distance and angle between us and the target
        d_target = get_distance(waypoint, curr_loc)

        # get angle between [velocity vector] and [distance vector]
        a_error = get_angle_between_3_pts(center=curr_loc, waypoint=waypoint, next_pos=next_loc)
        if a_error > math.pi:
            a_error = a_error - 2*math.pi
        elif a_error < -math.pi:
            a_error = a_error + 2*math.pi
        print(a_error)
        # print("curr_loc = {}, waypoint_simulation = {}, next_loc = {}, a_error = {}".format(curr_loc, waypoint_simulation, next_loc, a_error))

        # stall here.
        time.sleep(0.01)

        # check if target reached: we are within an acceptable margin of the target
        if d_target < EPSILON_RADIUS:
            # proceed to the new waypt, if there is any more
            if len(points) > 0:
                waypoint = points.pop(0)
                # reset integral errors and prev errors
                a_integral = 0.0
                d_integral = 0.0
                a_prev = 0.0
                d_prev = 0.0
                continue
            # no points left, we're done.
            else:
                print("NO POINTS LEFT. DONE.")
                break

        # VELOCITY PID
        v_pid = get_pid_distance(d_err_curr=d_target, d_err_prev=d_prev, d_err_integral=d_integral)
        # print("v_p = {}, v_i = {}, v_d = {}, v_pid = {}".format(d_target, d_integral, d_target-d_prev, v_pid))

        # set prev value and accumulate onto integral
        d_prev = d_target
        d_integral += d_target

        # @TODO see if checking for epsilon distance works
        max_error = EPSILON_RADIUS
        min_error = -EPSILON_RADIUS

        if d_target > max_error:
            drive_signal[0] = MAX_SPEED_VEC
        elif d_target < min_error:
            drive_signal[0] = MIN_SPEED_VEC
        else:
            drive_signal[0] = STOP

        # ANGLE PID
        a_pid = get_pid_angle(a_err_curr=a_error, a_err_prev=a_prev, a_err_integral=a_integral)
        # print("a_p = {}, a_i = {}, a_d = {}, a_pid = {}".format(a_error, a_integral, a_error-a_prev, a_pid))

        # set prev value and accumulate onto integral
        a_prev = a_error
        a_integral += a_error

        if a_error < -EPSILON_ANGLE:
            drive_signal[1] = 10
        elif a_error > EPSILON_ANGLE:
            drive_signal[1] = -10
        else:
            drive_signal[1] = 0

        # drive_signal[1] = -a_pid

        # print(drive_signal[0], drive_signal[1])

        x_prev = x
        y_prev = y

    # end of execution, stop the car.
    drive_signal[0] = STOP
    drive_signal[1] = 0


# Given (x1, y1), (x2, y2), find separation d
def get_distance(pos_prev, pos_curr):
    # polar coordinates: r
    r = np.sqrt((pos_curr[0] - pos_prev[0]) ** 2 + (pos_curr[1] - pos_prev[1]) ** 2)
    return r


# given a center point and 2 other points, find the angle between them in radians.
# NOTE: IF PT2 IS THE VELOCITY, THEN A POSITIVE THETA MEANS A LEFT (CCW) TURN NEEDS TO BE MADE
def get_angle_between_3_pts(center, waypoint, next_pos):
    # accept "center" as the origin and normalize other points
    n_waypoint = waypoint[0] - center[0], waypoint[1] - center[1]
    n_next_pos = next_pos[0] - center[0], next_pos[1] - center[1]
    # use atan2 between normalized p1 and p2
    theta = np.arctan2(n_waypoint[1], n_waypoint[0]) - np.arctan2(n_next_pos[1], n_next_pos[0])
    return theta


# Given (x_curr, y_curr), (x_prev, y_prev), calculate your next position in (x_next, y_next) format:
def get_next_loc(curr, prev):
    x_step = curr[0] - prev[0]
    y_step = curr[1] - prev[1]
    return curr[0] + x_step, curr[1] + y_step
