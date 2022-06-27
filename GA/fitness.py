#!/usr/bin/env python3

import numpy as np

from scipy.signal import savgol_filter

from scipy.stats import _

def moving_average(arr,window_size=int):
    i = 0
    #compute the derivate (difference between points)
    arr1=np.diff(arr)
    # Initialize an empty list to store moving average
    moving_averages = []
    while i < len(arr1) - window_size + 1:
        
        # Calculate the average of current window
        window_average = round(np.sum(arr1[
        i:i+window_size]) / window_size, 2)
 
        # Store the average of current
        # window in moving average list
        moving_averages.append(window_average)
        # Shift window to right by one position
        i += 1

    moving_averages=np.abs(moving_averages)
    max_moving_average=(-1)*np.amax(moving_averages)

    return max_moving_average, moving_averages


def count_ma(max,arr,treshold):
    max=(-1)*max
    treshold=max-max*treshold
    count=sum(i > treshold for i in arr)
    return count
    
def smooth(time,arr):
    window=round(len(time)*0.05) #window is 5% the lenght of the data
    arr_hat = savgol_filter(arr,window, 3)
    max_diff=(-1)*np.amax(np.abs(arr-arr_hat))
    return max_diff, arr_hat


def xyz_fit(x,y,z,Time):
    # x,y,z,Time=get_position(solution_idx=1,generation=1,path=path)

    ################ Moving average #######################
    window_size = 4 
    xvalue, xmoving_averages = moving_average(x,window_size)
    yvalue, xmoving_averages = moving_average(y,window_size)
    zvalue, xmoving_averages = moving_average(z,window_size)
    # count=count_ma(value,moving_averages,0.1)

    ##### smoothing spline to detect jumps and spikes #####
    x_max_diff, _ = smooth(Time,x)
    y_max_diff, _ = smooth(Time,y)
    z_max_diff, _ = smooth(Time,z)

    ######### compute fitness #######
    xfit=xvalue+x_max_diff
    yfit=yvalue+y_max_diff
    zfit=zvalue+z_max_diff

    xyzfitness=xfit+yfit+zfit
    print(xyzfitness)

    return xyzfitness

def residuals_fit(phase, TimeP, range, TimeR):
    residual=1000

    return residual
