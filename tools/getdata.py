#!/usr/bin/env python3

import os
import numpy as np



def get_position(solution_idx=None,generation=None,path=str):
    # Define paths for data

    # path='/home/src2/Maria/optimizer/data'
    if solution_idx == None and generation == None:
        path2ind=path
    else:
        path2gen=os.path.join(path,str(generation))
        path2ind=os.path.join(path2gen,str(solution_idx))


    #define variables
    Time=[]
    X=[]
    Y=[]
    Z=[]
    ClkBias=[]
    TropWet=[]
    #file names to get data from
    tdp_file_name='smooth0_0.tdp'
    #directory where data is stored
    files=os.listdir(path2ind)

    xyzfile=os.path.join(path2ind,tdp_file_name)
    with open(xyzfile,'r') as tdp:
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

            if line.rfind('Clk.Bias')>-1:
                columns=line.strip().split()
                ClkBias.append(float(columns[2]))
            if line.rfind('Trop.WetZ')>-1:
                columns=line.strip().split()
                TropWet.append(float(columns[2]))
        Xr=(np.array(X)-X[0])
        Yr=(np.array(Y)-Y[0])
        Zr=(np.array(Z)-Z[0])

        Time=(np.array(Time)-min(Time))/3600.0 #show time in Hours from start

    return Xr,Yr,Zr,Time

def get_residuals(solution_idx=None,generation=None,path=str):
    # path='/home/src2/Maria/optimizer/data'
    if solution_idx == None and generation == None:
        path2ind=path
    else:
        path2gen=os.path.join(path,str(generation))
        path2ind=os.path.join(path2gen,str(solution_idx))
    #define variables
    TimeP=[]
    TimeR=[]
    phase=[]
    range=[]

    #file names to get data from
    out_file_name='finalResiduals.out'
    # out_file_name='postfitResiduals.out'
    #directory where data is stored
    residfile=os.path.join(path2ind,out_file_name)
    with open(residfile,'r') as out:
        for line in out:
            if line.find('DELETED')>-1:
                    continue #skip deleted lines by default
            #Extract values
            if line.rfind('IonoFreeL')>-1:
                columns=line.strip().split()
                phase.append(float(columns[3]))
                TimeP.append(int(columns[0]))
            if line.rfind('IonoFreeC')>-1:
                columns=line.strip().split()
                range.append(float(columns[3]))
                TimeR.append(int(columns[0]))


        phase=np.array(phase)*100 #change to cm
        range=np.array(range)*100

        TimeP=(np.array(TimeP)-min(TimeP))/3600.0 #show time in Hours from start
        TimeR=(np.array(TimeR)-min(TimeR))/3600.0 #show time in Hours from start

    return phase, TimeP, range, TimeR


if __name__=="__main__":
    path='/home/src2/Maria/optimizer/data'
    # print(path)
    x,y,z,Time=get_position(solution_idx=1,generation=1,path=path)
    print(Time)
