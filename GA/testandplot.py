#!/usr/bin/env python3

import sys, os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy import stats as st

def moving_average(arr,window_size=int):
    i = 0
    # Initialize an empty list to store moving average
    moving_averages = []
    while i < len(arr) - window_size + 1:
        
        # Calculate the average of current window
        window_average = round(np.sum(arr[
        i:i+window_size]) / window_size, 2)
 
        # Store the average of current
        # window in moving average list
        moving_averages.append(window_average)
        # Shift window to right by one position
        i += 1

    # moving_averages=np.abs(moving_averages)
    # moving_averages=moving_averages
    max_moving_average=np.amax(np.abs(moving_averages))

    return max_moving_average, moving_averages


def count_ma(max,arr,treshold):
    max=(-1)*max
    treshold=max-max*treshold
    # print(treshold)
    count=sum(i > treshold for i in arr)
    return count


os.chdir('/home/src2/Maria/optimizer/data/SIGMATESTING')
path=os.getcwd()
tdp_file_name=[]
#directory where data is stored
# files=os.listdir(path)
for root, dirs, files in os.walk(path):
        dirs.sort()
        for dirname in dirs:
            dir_name=os.path.join(root, dirname)
            # out_file_path=dir_name+'/finalResiduals.out'
            tdp_file_path=dir_name+'/smooth0_0.tdp'
            if os.path.exists(tdp_file_path):
                # out_file_name.append(dir_name+'/finalResiduals.out')
                tdp_file_name.append(dir_name+'/smooth0_0.tdp')



Time=[]
X=[]
Y=[]
Z=[]
x=[]
y=[]
z=[]
TIME=[]

for i, file in enumerate(tdp_file_name):
    X=[]
    Y=[]
    Z=[]
    Time=[]
    print(i)
    with open(file,'r') as tdp:
        for line in tdp:
            if line.rfind('Pos.X')>-1:
                columns=line.strip().split() 
                X.append(float(columns[2]))
                Time.append(float(columns[0]))

            if line.rfind('Pos.Y')>-1:
                columns=line.strip().split()
                Y.append(float(columns[2]))
            if line.rfind('Pos.Z')>-1:
                columns=line.strip().split()
                Z.append(float(columns[2]))
              
        Xr=(np.array(X)-X[0])
        Yr=(np.array(Y)-Y[0])
        Zr=(np.array(Z)-Z[0])
        time=(np.array(Time)-min(Time))/3600.0 #show time in Hours from start
        x.append(Xr)
        y.append(Yr)
        z.append(Zr)
        TIME.append(time)
  

# window_size = 4 
# # i = 0
# # # Initialize an empty list to store moving average
# moving_averages = []
# moving_variance = []

# for j in range(len(tdp_file_name)):
#     arr=[]
#     arr=np.diff(z[j])
#     valuediff, moving_averages_diff=moving_average(arr,window_size)
#     value, moving_averages=moving_average(z[j],window_size)
#     maxvalue=np.amax(np.abs(z[j]))-valuediff

#     plt.plot(moving_averages,'.')
#     plt.plot(moving_averages_diff,'.')
#     plt.show()
#     # count=count_ma(value,moving_averages,0.01)
#     print(j,' diff: ',valuediff,' data: ',value, 'subtract: ', maxvalue)
    
for j in range(len(tdp_file_name)):  
    diff=[]
    yhat = savgol_filter(z[j],1800, 3)
    # print(len(yhat))
    diff=np.abs(yhat-z[j])
    max=np.amax(diff)
    plt.plot(diff)
    plt.show()
    print(j,np.sum(diff),max)
    plt.plot(TIME[0],z[j],'g')
    plt.plot(TIME[0],yhat,'r')
    plt.show()

# while i < len(y[0]) - window_size + 1:
    
#     # Calculate the average of current window
#     window_average = round(np.sum(y[2][
#     i:i+window_size]) / window_size, 2)
#     window_variance=np.var(y[2][
#     i:i+window_size]) 
#     # Store the average of current
#     # window in moving average list
#     moving_averages.append(window_average)
#     moving_variance.append(window_variance)
#     # Shift window to right by one position
#     i += 1
# print(np.amax(moving_averages))
# print(np.amin(moving_averages))
# print('variance')
# print(np.amax(moving_variance))
    

    
    
    




# fig1, axs = plt.subplots(3,sharex=True)
# fig1.suptitle('Motion in ECEF')
# axs[0].plot(TIME[0],x[0],'.', ms = 1)
# axs[0].plot(TIME[1],x[1],'.', ms = 1)
# axs[0].plot(TIME[2],x[2],'.', ms = 1)
# axs[0].plot(TIME[3],x[3],'.', ms = 1)
# axs[0].plot(TIME[4],x[4],'.', ms = 1)



# axs[1].plot(TIME[0],y[0],'.', ms = 1,label='test 1')
# axs[1].plot(TIME[1],y[1],'.', ms = 1,label='test 2')
# axs[1].plot(TIME[2],y[2],'.', ms = 1,label='test 3')
# axs[1].plot(TIME[3],y[3],'.', ms = 1,label='test 4')
# axs[1].plot(TIME[4],y[4],'.', ms = 1,label='test 5')
# axs[1].legend()

# axs[2].plot(TIME[0],z[0],'.', ms = 1)
# axs[2].plot(TIME[1],z[1],'.', ms = 1)
# axs[2].plot(TIME[2],z[2],'.', ms = 1)
# axs[2].plot(TIME[3],z[3],'.', ms = 1)
# axs[2].plot(TIME[4],z[4],'.', ms = 1)
# axs[0].set(ylabel='X (m)')
# axs[1].set(ylabel='Y (m)')
# axs[2].set(ylabel='Z (m)')

# plt.xlabel('Time (hours since start)')
# plt.show()

