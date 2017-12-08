from glob import *
import pygame, math, sys, waypoint
from random import randint
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

# waypoints = [(300, 300), (600, 600), (300, 700), (800, 900), (700, 100)]

waypoints = []

# borders
MAX_Y = 1000
MAX_X = 1000


def simulate(drive_signal, car_location):
    pygame.init()
    # initialize the screen with size (MAX_X, MAX_Y)
    screen = pygame.display.set_mode((MAX_X, MAX_Y))

    car = pygame.image.load('car.png')
    # initialize the sound mixer
    clock = pygame.time.Clock()  # load clock
    speed = direction = 0.0  # start speed & direction

    position = (100, 100)  # start position
    play = True

    while play:

        screen.fill(BACKGROUND)
        # SIMULATION
        # get new speed and direction based on the current input and current speed & direction
        new_speed, new_direction = get_movement_sim(drive_signal, speed, direction)

        speed = new_speed
        direction = new_direction
        x, y = position
        rad = direction * math.pi / 180
        # print("SPEED = {}".format(speed))
        x += speed * math.sin(rad) / (float(FREQUENCY)/10.0)
        y += speed * math.cos(rad) / (float(FREQUENCY)/10.0)
        # make sure the car doesn't exit the screen
        myfont = pygame.font.SysFont("calibri" , 35)
        for i, wpt in enumerate(waypoints):
            pygame.draw.circle(screen, (0, 150, 0), wpt, 10)
            label = myfont.render(str(i+1), 1, (255,255,255))
            screen.blit(label, wpt)

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


def get_movement_sim(drive_signals, speed, direction):
    v_pid, a_pid = drive_signals

    # normalize:
    v_signal = (v_pid-STOP) / DELTA_SPEED_ACCELERATE
    a_signal = a_pid / DELTA_DIRECTION

    new_direction = direction + a_signal * speed * TURN_ANGULAR_FREQ / (float(FREQUENCY)/10.0)

    # down = positive acceleration.
    acceleration = v_signal

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

#
# def assert_outside_epsilon():
#     # TODO
#     pass
#
#
# def generate_waypoints(num, e_rad):
#     """Generate num number of waypoints that are at least e_rad from each other"""
#     NUM_TRIES = 100000  # if we can't get num waypoints within e_rad after this many tries, then fail.
#     waypts = []
#     for i in range(NUM_TRIES):
#         (x, y) = randint(e_rad, MAX_X-e_rad), randint(e_rad, MAX_Y-e_rad)
#         if assert_outside_epsilon((x, y), waypts, e_rad):
#             # TODO
#             pass
#             waypts.append()


def main():
    drive_signal = Array('d', [0.0, 0.0])
    location = Array('d', [0.0, 0.0])
    # waypoints = generate_waypoints(6, 100)

    waypoints = [(300, 300), (500, 500), (100, 500)]

    simulation_process = Process(target=simulate, args=(drive_signal, location))
    car_process = Process(target=waypoint.track_waypoint, args=(waypoints, drive_signal, location))

    simulation_process.start()
    car_process.start()

    simulation_process.join()
    car_process.join()


main()
