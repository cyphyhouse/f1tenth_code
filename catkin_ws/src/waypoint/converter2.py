# Given digital signals in bagged data format, output real-world data (velocity, angle)
import pandas as pd
import numpy as np
from simulator import *
from pprint import pprint

# MOVEMENT PARAMETERS in m/sec
TURN_ANGULAR_FREQ = 1.4873505359695478  # rad/sec
ACCELERATION_FUNCTION_COEFFICIENT = 0.0066454120745643913  # for a in f(x) = ax
BREAKING_COEFFICIENT = 0.056540574036237645  # for a in f(x) = ax
INERTIA_DECELERATION_COEFFICIENT = 0.0058368692660536035  # for a in f(x) = ax


def convert_files(files):
    """Input: list of file names to be converted.
    Output: None
    SideEffects: Converted files are placed in output folder"""
    for file in files:
        df_converted = convert(file)
        filename = file.split(".")
        df_converted.to_csv('output/{}_converted.csv'.format(filename[0]))


def convert(file):
    """Input: single file name to be converted.
    Output: data frame that has the converted values."""
    df = pd.read_csv(file)
    df['duration'] = df['%time'].diff().shift(-1)  # double check the shift
    # normalize drive signals:
    df.ix[df['field.velocity'] < 9780, 'acceleration'] = -1
    df.ix[df['field.velocity'] > 9780, 'acceleration'] = 1
    df.ix[df['field.velocity'] == 9780, 'acceleration'] = 0
    df.ix[df['field.angle'] < 0, 'turn'] = -1
    df.ix[df['field.angle'] > 0, 'turn'] = 1
    df.ix[df['field.angle'] == 0, 'turn'] = 0
    curr_speed = 0.0
    curr_angle = 0.0
    pd.set_option('display.max_rows', len(df))
    # print(df)
    for index, row in df.iterrows():
        # print(row)
         curr_speed, curr_angle = get_movement(row['duration'], row['acceleration'], row['turn'], curr_speed, curr_angle)
         print(curr_speed, curr_angle)


def get_movement(duration, signal_acceleration, signal_turn, curr_speed, curr_direction):
    """Inputs: acceleration, turn in form {-1, 0, 1}. (for turn, -1: left, 1: right)
    duration is amount of time passed until the next message
    Output: updated speed, direction.
    """
    acceleration = ACCELERATION_FUNCTION_COEFFICIENT * duration * 100
    deceleration = INERTIA_DECELERATION_COEFFICIENT * duration * 100
    breaking = BREAKING_COEFFICIENT * duration * 100
    turn = TURN_ANGULAR_FREQ * signal_turn * curr_speed * duration / 10

    if turn == 0:
        new_direction = curr_direction
    else:
        new_direction = curr_direction + turn

    # no acceleration, use deceleration function
    if signal_acceleration == 0:
        if curr_speed > 0:
            new_speed = max(curr_speed - deceleration, 0.0)
        elif curr_speed < 0:
            new_speed = min(curr_speed + deceleration, 0.0)
        else:
            new_speed = curr_speed

    # there is acceleration
    else:
        # positive speed
        if curr_speed > 0.0:
            # positive acceleration
            if acceleration > 0:
                # calculate new speed
                new_speed = curr_speed + acceleration
            # positive speed & breaking
            elif acceleration < 0:
                new_speed = max(curr_speed - breaking, 0.0)

        # negative speed
        elif curr_speed < 0.0:
            # negative acceleration
            if acceleration < 0:
                # calculate new speed in positive terms, and invert sign
                new_speed = curr_speed - acceleration
            # negative speed & breaking
            elif acceleration > 0:
                new_speed = min(curr_speed + breaking, 0.0)

        # 0 speed
        else:
            # print("SPEED = {}".format(speed))
            new_speed = acceleration

    new_speed = max(-2, new_speed)
    new_speed = min(2, new_speed)

    return new_speed, new_direction


def main():
    convert("runs/run1_driveparam.txt")


main()
