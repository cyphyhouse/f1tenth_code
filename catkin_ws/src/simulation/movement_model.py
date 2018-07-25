import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from pprint import pprint
from scipy import stats, optimize

def get_data(filename):
    skiprows = [0,1,2,4]
    usecols = ['TX', 'TY']
    df = pd.read_csv(filename, skiprows=skiprows, usecols=usecols)

    # shift x,y values so that there min coord is 0
    df['pos_TX'] = df['TX'] - min(df['TX'])
    df['pos_TY'] = df['TY'] - min(df['TY'])
    # get absolute R value
    df['R'] = df.apply(lambda col: np.sqrt(col['pos_TX']**2 + col['pos_TY']**2), axis=1)

    df['vel'] = df['R'].diff()
    # pprint(df['vel'])
    pd.set_option('display.max_rows', len(df['R']))
    # plt.figure()
    # plt.plot(df['vel'])
    # plt.show(block=True)
    return df


def get_linear_regression(r_start, r_end, df, col):
    y = np.array(df.loc[r_start:r_end,col])
    x = range(r_end-r_start+1)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    return slope, r_value, p_value, std_err


def get_poly_fit(deg, r_start, r_end, df, col):
    y = np.array(df.loc[r_start:r_end,col])
    x = range(r_end-r_start+1)

    p, residuals, rank, singular_values, rcond = np.polyfit(x, y, deg, full=True)
    plt.plot(x, y)
    xp = np.linspace(0, r_end, 1000)
    f = np.poly1d(p)
    plt.plot(xp, f(xp))
    plt.show(block=True)
    return p, residuals, rank, singular_values, rcond


def get_curve_fit(func, r_start, r_end, df, col):
    y = np.array(df.loc[r_start:r_end,col])
    x_data = range(r_end-r_start+1)
    popt, pcov = optimize.curve_fit(func, x_data, y)
    y_fit = [func(x_i, *popt) for x_i in x_data]
    plt.plot(x_data, y_fit, 'r-', label='fit')
    plt.plot(x_data, y)
    plt.show(block=True)
    return popt


def acceleration_func(x, a, b, c):
    return a - b * np.exp(-c * x)


def get_max_turn_diameter(df):
    return (max(df['R']) - min(df['R'])) / 2


def get_max_turn_speed(df):
    df = df.dropna()
    return (max(df['vel']) - min(df['vel']))/2


def main():
    filename = 'data/car_f1_acceleration 2.csv'
    df = get_data(filename)
    plt.plot(df['vel'])
    plt.show()
    # print(get_max_turn_diameter(df)/2)




main()