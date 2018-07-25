import numpy as np
import math
import time

X_INIT = 100
Y_INIT = 100
EPSILON_RADIUS = 25
EPSILON_ANGLE = 0.1
FREQUENCY = 200
ANGLE_INTEGRAL_SATURATION = 15
OBSTACLE_AVOIDANCE_RADIUS = 70


# ANGLE_TO_OBSTACLE_EPSILON_RADIANS = 0.1


def get_pid_distance(d_err_curr, d_err_prev, d_err_integral):
    Kp = 1.0
    Ki = 0.0001
    Kd = 5.0
    v_pid = Kp * d_err_curr + Ki * d_err_integral + Kd * (d_err_curr - d_err_prev)
    # print(d_err_curr, d_err_integral, d_err_curr - d_err_prev, v_pid)
    return v_pid


def get_pid_angle(a_err_curr, a_err_prev, a_err_integral):
    Kp = 1
    Ki = 0.0007
    Kd = 10.0
    # Ki = 0.0007
    # Kd = 10.0
    return -(Kp * a_err_curr + Kd * (a_err_curr - a_err_prev) + Ki * a_err_integral)


def get_in_obs_steering(sharpness_coeff, steering_in, dist_to_obs, obs_avoidance_radius):
    """Get steering within avoidance radius of obstacle. The closer we are to the obstacle, the sharper we turn.
     -> Sharpness coeff should ideally be >= 1."""
    return min(sharpness_coeff * steering_in * ((obs_avoidance_radius - dist_to_obs) / obs_avoidance_radius) ** 2,
               1)


def track_waypoint(waypoints, obstacles, drive_signal, location_feed, play):
    # move for 1 second to get idea of your location & orientation

    path = []
    x_prev = -1.0
    y_prev = -1.0

    for i in range(100):
        x = location_feed[0]
        y = location_feed[1]
        if x != x_prev or y != y_prev:
            path.append((x, y))
        drive_signal[0] = 1
        drive_signal[1] = 0
        time.sleep(0.01)

    # stop moving (will have inertia but that's fine)
    drive_signal[0] = 0

    # get first waypoint:
    waypoint = waypoints.pop(0)
    x_prev, y_prev = path[-1]

    # distance and angle prev values
    curr_loc = path[-1]
    next_loc = get_next_loc(path[-1], path[-2])
    a_prev = get_angle_between_3_pts(center=curr_loc, waypoint=waypoint, next_pos=next_loc)

    # distance and angle integrals for PID
    a_integral = 0.0
    in_obstacle = False
    acceleration_in = 1.0
    steering_in = 0.0

    # while our list of points isn't empty
    while play.value == 1:
        time.sleep(0.01)
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
        # get distance and angle between us and the target
        d_error = get_distance(waypoint, curr_loc)
        # get angle between [velocity vector] and [distance vector]
        a_error = get_angle_between_3_pts(center=curr_loc, waypoint=waypoint, next_pos=next_loc)
        if a_error > math.pi:
            a_error = a_error - 2 * math.pi

        # if we are within the obstacle avoidance radius, avoid obstacle.
        if in_obstacle:
            # steer away as hard as you can
            acceleration_in = 1
            dist_to_obs, angle_to_obs = get_distance_and_angle_to_closest_obstacle(curr_loc, obstacles, next_loc)
            print(np.rad2deg(angle_to_obs))
            # steering_in = 1 if 0 < angle_to_obs < np.pi else -1
            if dist_to_obs > OBSTACLE_AVOIDANCE_RADIUS:
                in_obstacle = False
                continue

            in_obs_steering = get_in_obs_steering(sharpness_coeff=2.5,
                                                  steering_in=steering_in,
                                                  dist_to_obs=dist_to_obs,
                                                  obs_avoidance_radius=OBSTACLE_AVOIDANCE_RADIUS)

            # set drive signals and prev positions for next iteration
            drive_signal[0] = acceleration_in
            drive_signal[1] = in_obs_steering
            x_prev = x
            y_prev = y
            # reset the pid controller's integral.
            # a_integral = a_error = a_pid = a_prev = 0

            # print("{}, {}".format(acceleration_in, steering_in))
            continue

        # check if we are within an acceptable margin of the target
        if d_error < EPSILON_RADIUS:
            print("TARGET REACHED")
            # proceed to the new waypt, if there is any more
            if len(waypoints) > 0:
                waypoint = waypoints.pop(0)
                # reset integral errors and prev errors
                a_integral = 0.0
                # a_prev = 0.0
                continue
            # no points left, we're done.
            else:
                print("NO POINTS LEFT. DONE.")
                break

        # ANGLE PID
        a_pid = get_pid_angle(a_err_curr=a_error, a_err_prev=a_prev, a_err_integral=a_integral)

        # set prev value and accumulate onto integral
        a_prev = a_error
        # saturation for integral:
        a_integral = max(min(a_integral + a_error, ANGLE_INTEGRAL_SATURATION), -ANGLE_INTEGRAL_SATURATION)
        steering_in = min(max(a_pid, -1), 1)

        # print("a_pid = {}, v_pid = {}".format(a_pid, v_pid))
        # publish:
        drive_signal[0] = acceleration_in
        drive_signal[1] = steering_in
        x_prev = x
        y_prev = y
        # get distance and angle to closest obstacle:
        dist_to_obs, angle_to_obs = get_distance_and_angle_to_closest_obstacle(curr_loc, obstacles, next_loc)

        if dist_to_obs <= OBSTACLE_AVOIDANCE_RADIUS:
            in_obstacle = True
            steering_in = 1 if 0 < angle_to_obs < np.pi else -1

    # end of execution, stop the car.
    drive_signal[0] = 0.0
    drive_signal[1] = 0.0


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
    if theta < -np.pi:
        theta = 2*np.pi + theta
    elif theta > np.pi:
        theta = 2*np.pi - theta
    return theta

# Given (x_curr, y_curr), (x_prev, y_prev), calculate your next position in (x_next, y_next) format:
def get_next_loc(curr, prev):
    x_step = curr[0] - prev[0]
    y_step = curr[1] - prev[1]
    return curr[0] + x_step, curr[1] + y_step


def get_distance_and_angle_to_closest_obstacle(curr_loc, obstacles, next_loc):
    """
    See function name.
    :param curr_loc: tuple of x,y coords
    :param obstacles: list of x,y coord tuples
    :param next_loc: tuple of x,y coords
    :return: tuple of (distance to closest obs, angle to closest obs)
    """
    closest_obs_dist_pair = min([(obs, get_distance(curr_loc, obs)) for obs in obstacles],
                                key=lambda x: x[1])

    angle_to_closest_obs = get_angle_between_3_pts(curr_loc, closest_obs_dist_pair[0], next_loc)
    return closest_obs_dist_pair[1], angle_to_closest_obs
