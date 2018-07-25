import math, sys, waypoint
import pygame as pg
import numpy as np
from pygame.locals import *
from multiprocessing import Value, Array, Process
from copy import deepcopy
import waypoint
import random
import waypoint

# the frequency of the rendering. This also affects speed & direction calculations.
FREQUENCY = waypoint.FREQUENCY

BACKGROUND = (0, 0, 0)

# MOVEMENT PARAMETERS
TURN_ANGULAR_FREQ = 1.4873505359695478  # rad/sec
ACCELERATION_FUNCTION_COEFFICIENT = 0.066454120745643913  # for a in f(x) = ax
BREAKING_COEFFICIENT = 0.56540574036237645  # for a in f(x) = ax
INERTIA_DECELERATION_COEFFICIENT = 0.058368692660536035 / (FREQUENCY / 500)  # for a in f(x) = ax

# borders
MAX_Y = 1000
MAX_X = 1000


def simulate(drive_signal, car_location, waypoints, obstacles, play):
    # initialize the screen with size (MAX_X, MAX_Y)
    screen = pg.display.set_mode((MAX_X, MAX_Y))

    car = pg.image.load('car.png')
    pg.font.init()
    # initialize the sound mixer
    clock = pg.time.Clock()  # load clock
    acceleration_in = steering_in = 0
    speed = direction = 0.0  # start speed & direction

    position = (100, 100)  # start position
    path_taken = []
    iteration = 0
    screen.fill(BACKGROUND)
    # draw waypoints on the screen
    for i, wpt in enumerate(waypoints):
        pg.draw.rect(screen, Color(0, 150, 0, 0), (*wpt, 20, 20))
        myfont = pg.font.SysFont("arial", 20)
        label = myfont.render(" " + str(i + 1), 1, (255, 255, 255))
        screen.blit(label, wpt)

    # draw obstacles on the screen
    for obs in obstacles:
        pg.draw.circle(screen, Color(50, 0, 0, 0), obs, waypoint.OBSTACLE_AVOIDANCE_RADIUS)
        pg.draw.rect(screen, Color(250, 0, 0, 0), (*obs, 3, 3))

    pg.display.flip()

    while play:
        iteration += 1
        events = pg.event.get()
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    play.value = 0

        if play.value == 0:
            break

        clock.tick(FREQUENCY)

        acceleration_in = drive_signal[0]
        steering_in = drive_signal[1]

        drive_inputs = (acceleration_in, steering_in)

        # SIMULATION
        # get new speed and direction based on the current input and current speed & direction
        new_speed, new_direction = get_movement_sim(drive_inputs, speed, direction)

        speed = new_speed
        direction = new_direction
        x, y = position
        rad = direction * math.pi / 180
        # print("SPEED = {}".format(speed))
        x += speed * math.sin(rad) / (float(FREQUENCY) / 10.0)
        y += speed * math.cos(rad) / (float(FREQUENCY) / 10.0)
        # make sure the car doesn't exit the screen

        if y < 0:
            y = 0
        elif y > MAX_Y:
            y = MAX_Y
        if x < 0:
            x = 0
        elif x > MAX_X:
            x = MAX_X

        position = (x, y)

        if iteration % (FREQUENCY / 20) == 0:
            path_taken.append(position)
        # .. rotate the car image for direction
        rotated = pg.transform.rotate(car, direction)
        # .. position the car on screen
        rect = rotated.get_rect()
        rect.center = position
        # .. render the car to screen
        screen.blit(rotated, rect)
        car_location[0] = x
        car_location[1] = y
        # draw path taken on screen
        # if len(path_taken) > 25:
        #     for pt in path_taken[-20:]:
        #         pg.draw.rect(screen, Color(50, 50, 250, 0), (*pt, 3, 3))
        pg.display.flip()



    sys.exit(0)  # quit


def get_movement_sim(drive_inputs, speed, direction):
    acceleration_in, steering_in = drive_inputs
    new_direction = direction + steering_in * speed * TURN_ANGULAR_FREQ / (float(FREQUENCY) / 10.0)

    # no acceleration, use deceleration function
    if acceleration_in == 0:
        if speed > 0:
            new_speed = max(speed - INERTIA_DECELERATION_COEFFICIENT, 0.0)
        elif speed < 0:
            new_speed = min(speed + INERTIA_DECELERATION_COEFFICIENT, 0.0)
        else:
            new_speed = speed

    # there is acceleration
    else:
        # positive speed
        if speed > 0.0:
            # positive acceleration
            if acceleration_in > 0:
                # calculate new speed
                new_speed = speed + ACCELERATION_FUNCTION_COEFFICIENT
            # positive speed & breaking
            elif acceleration_in < 0:
                new_speed = max(speed - BREAKING_COEFFICIENT, 0.0)

        # negative speed
        elif speed < 0.0:
            # negative acceleration
            if acceleration_in < 0:
                # calculate new speed in positive terms, and invert sign
                new_speed = speed - ACCELERATION_FUNCTION_COEFFICIENT
            # negative speed & breaking
            elif acceleration_in > 0:
                new_speed = min(speed + BREAKING_COEFFICIENT, 0.0)

        # 0 speed
        else:
            # print("SPEED = {}".format(speed))
            new_speed = acceleration_in * ACCELERATION_FUNCTION_COEFFICIENT

    # print(new_speed, new_direction)
    new_speed = max(-19.0, new_speed)
    new_speed = min(19.0, new_speed)

    return new_speed, new_direction


def min_distance(curr, pts):
    """Find the distance between this point and the closest point in the set """
    min_dist = math.inf
    for pt in pts:
        dist = waypoint.get_distance(curr, pt)
        if dist < min_dist:
            min_dist = dist

    return min_dist


def generate_waypoints(number, epsilon_radius):
    """Generate given number of waypoints with distance at least epsilon_radius in between"""
    waypts = []
    num_trials = 0
    max_trials = 100000
    while num_trials < max_trials:
        waypt = (random.randint(50, MAX_Y - 50), random.randint(50, MAX_X - 50))
        if min_distance(waypt, waypts) > epsilon_radius:
            waypts.append(waypt)
            if len(waypts) == number:
                return waypts

    raise RuntimeError("Cannot generate waypoints given parameters.")


def generate_obstacles(number, waypoints, epsilon_radius):
    """Generate given number of obstacles with distance at least epsilon_radius in between
    AND at least epsilon_radius away from each waypoint"""
    obstacles = []
    all_items = deepcopy(waypoints)
    num_trials = 0
    max_trials = 100000
    while num_trials < max_trials:
        obstacle = (random.randint(50, MAX_Y - 50), random.randint(50, MAX_X - 50))
        if min_distance(obstacle, all_items) > epsilon_radius:
            obstacles.append(obstacle)
            all_items.append(obstacle)
            if len(obstacles) == number:
                return obstacles

    raise RuntimeError("Cannot generate waypoints given parameters.")


def main():
    drive_signal = Array('d', [0.0, 0.0])
    location = Array('d', [0.0, 0.0])
    play = Value('i', 1)
    waypoints = generate_waypoints(number=8, epsilon_radius=100)
    obstacles = generate_obstacles(number=10, waypoints=waypoints,
                                   epsilon_radius=2.4 * waypoint.OBSTACLE_AVOIDANCE_RADIUS)

    # waypoints = [(100, 800)]
    # obstacles = [(90, 700)]
    simulation_process = Process(target=simulate, args=(drive_signal, location, waypoints, obstacles, play))
    car_process = Process(target=waypoint.track_waypoint, args=(waypoints, obstacles, drive_signal, location, play))
    simulation_process.start()
    car_process.start()
    car_process.join()
    simulation_process.join()


if __name__ == "__main__":
    main()
