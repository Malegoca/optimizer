#!/usr/bin/env python3

import numpy as np

from scipy.signal import savgol_filter

from scipy.stats import probplot, kurtosis

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
    # print(xyzfitness)

    return xyzfitness

def residuals_fit(phase, TimeP, range, TimeR):
    #phase fitness: make sure is gausian
    _, _, rp=probplot(phase, dist="norm",fit=True, plot=None)[1]

    if rp**2 < 0.5:
        phasefit=-300
    elif rp**2 < 0.98:
        phasefit=-200
    else:
        phasefit=100

    resultp = kurtosis(phase,fisher=True)
    if resultp <= 0 or resultp > 3:
        phasefit2=-400
    else:
        phasefit2=100

    #Range fitness: make sure is gausian
    _, _, r=probplot(range, dist="norm",fit=True, plot=None)[1]

    if r**2 < 0.5:
        rangefit=-300
    elif r**2 < 0.98:
        rangefit=-200
    else:
        rangefit=100

    result = kurtosis(phase,fisher=True)
    if result <= 0 or result > 3:
        rangefit2=-400
    else:
        rangefit2=100

    residualsfit=phasefit+phasefit2+rangefit+rangefit2

    return residualsfit
