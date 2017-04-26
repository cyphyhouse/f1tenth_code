import pygame, math, sys, waypoint
import numpy as np
from pygame.locals import *
from multiprocessing import Value, Array, Process
import waypoint

# the frequency of the rendering. This also affects speed & direction calculations.
FREQUENCY = waypoint.FREQUENCY

BACKGROUND = (0, 0, 0)

# MOVEMENT PARAMETERS
TURN_ANGULAR_FREQ = 1.4873505359695478  # rad/sec
ACCELERATION_FUNCTION_COEFFICIENT = 0.066454120745643913  # for a in f(x) = ax
BREAKING_COEFFICIENT = 0.56540574036237645  # for a in f(x) = ax
INERTIA_DECELERATION_COEFFICIENT = 0.058368692660536035  # for a in f(x) = ax

# borders
MAX_Y = 1000
MAX_X = 1000


def simulate(drive_signal, car_location):
    # initialize the screen with size (MAX_X, MAX_Y)
    screen = pygame.display.set_mode((MAX_X, MAX_Y))

    car = pygame.image.load('car.png')
    # initialize the sound mixer
    clock = pygame.time.Clock()  # load clock
    k_up = k_down = k_left = k_right = 0  # init key values
    speed = direction = 0.0  # start speed & direction

    position = (100, 100)  # start position

    play = True

    while play:

        clock.tick(FREQUENCY)

        k_up = drive_signal[0]
        k_down = drive_signal[1]
        k_left = drive_signal[2]
        k_right = drive_signal[3]

        keys = (k_up, k_down, k_left, k_right)
        screen.fill(BACKGROUND)
        # SIMULATION
        # get new speed and direction based on the current input and current speed & direction
        new_speed, new_direction = get_movement_sim(keys, speed, direction)

        speed = new_speed
        direction = new_direction
        x, y = position
        rad = direction * math.pi / 180
        # print("SPEED = {}".format(speed))
        x += speed * math.sin(rad) / (float(FREQUENCY)/10.0)
        y += speed * math.cos(rad) / (float(FREQUENCY)/10.0)
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
        # print(position)
        # RENDERING
        # .. rotate the car image for direction
        rotated = pygame.transform.rotate(car, direction)
        # .. position the car on screen
        rect = rotated.get_rect()
        rect.center = position
        # .. render the car to screen
        screen.blit(rotated, rect)
        pygame.display.flip()
        car_location[0] = x
        car_location[1] = y

    sys.exit(0)  # quit


def get_movement_sim(keys, speed, direction):
    k_up, k_down, k_left, k_right = keys

    if k_left == k_right:
        new_direction = direction
    else:
        new_direction = direction + (k_left - k_right) * speed * TURN_ANGULAR_FREQ / (float(FREQUENCY)/10.0)

    # down = positive acceleration.
    acceleration = (k_up - k_down)

    # no acceleration, use deceleration function
    if acceleration == 0:
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
            if acceleration > 0:
                # calculate new speed
                new_speed = speed + ACCELERATION_FUNCTION_COEFFICIENT
            # positive speed & breaking
            elif acceleration < 0:
                new_speed = max(speed - BREAKING_COEFFICIENT, 0.0)

        # negative speed
        elif speed < 0.0:
            # negative acceleration
            if acceleration < 0:
                # calculate new speed in positive terms, and invert sign
                new_speed = speed - ACCELERATION_FUNCTION_COEFFICIENT
            # negative speed & breaking
            elif acceleration > 0:
                new_speed = min(speed + BREAKING_COEFFICIENT, 0.0)

        # 0 speed
        elif speed == 0.0:
            # print("SPEED = {}".format(speed))
            new_speed = acceleration * ACCELERATION_FUNCTION_COEFFICIENT

    # print(new_speed, new_direction)
    new_speed = max(-19.0, new_speed)
    new_speed = min(19.0, new_speed)

    return new_speed, new_direction


def main():
    drive_signal = Array('d', [0.0, 0.0, 0.0, 0.0])
    location = Array('d', [0.0, 0.0])

    waypoints = [(300, 300), (600, 600), (300, 700)]

    simulation_process = Process(target=simulate, args=(drive_signal, location))
    car_process = Process(target=waypoint.track_waypoint, args=(waypoints, drive_signal, location))

    simulation_process.start()
    car_process.start()

    simulation_process.join()
    car_process.join()


main()
