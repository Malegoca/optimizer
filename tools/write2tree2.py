#!/usr/bin/env python3
import os
import re
import shutil
import subprocess


def write2tree(params,path):

    #set directory to store folders for runs
    # path2gen=os.path.join(path,str(generation))
    # path2ind=os.path.join(path2gen,str(solution_idx))
    path2run=os.path.join(path,'BopRunningFolder')
    path2template=os.path.join(path,'SOLO_GPS')
    # path2template=os.path.join(path,'template')

    isexist=os.path.exists(path2run)


    #create directories if they don't exist
    if not isexist:
        os.mkdir(path2run)

    #define file handles
    template=os.path.join(path2template,'Trees/ppp_0.tree')
    #make tree dir for out file
    outdir=os.path.join(path2run,'Trees')
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    #file path for tree to write parameters and run rtgx
    outfile=os.path.join(outdir,'ppp_0.tree')

    #write to tree in respective directory
    with open(template,'r') as Template:
        with open(outfile,'w+') as out:

            for line in Template:
                # Trop DryZ
                if re.search(r'\bDryZ\b', line):
                    x=str(params[0])
                    change=line.replace(line[11:-1],x)
                    line=change

                # Trop WetZ
                if re.search(r'\bWetZ\b', line):
                    x=str(params[1])
                    change=line.replace(line[11:-1],x)
                    line=change

                #Trop Initial Uncertainty and update
                if re.search(r'\bWetZ\b', line): #This copies the line again to compensate for the use of next() below
                    out.write(line)

                if re.search(r'\bWetZ\b', line):
                    TIU=str(params[2])
                    TUU=str(params[3])
                    next_line=next(Template)
                    x = next_line.find('j')
                    y = next_line.find('3')
                    change = next_line.replace(next_line[x+2:y-1], TIU + ' ' + TUU)
                    line=change
                    # print(line)

                # Position Initial Uncertainty and Update
                if re.search(r'\bPos\b', line):
                    out.write(line)

                if re.search(r'\bPos\b', line):
                    PIU=str(params[4])
                    PUU=str(params[5])
                    next_line=next(Template)
                    x = next_line.find('j')
                    y = next_line.find('$')
                    change = next_line.replace(next_line[x+2:y-1], PIU + ' ' + PUU)
                    line=change


                # Phase Data Sigma DataLinkSpec_LC_GPS
                if re.search(r'\bDataLinkSpec_LC_GPS\b', line):
                    out.write(line)

                if re.search(r'\bDataLinkSpec_LC_GPS\b', line):
                    Sigma=str(params[6])
                    next_line=next(Template)
                    x = next_line.rfind('a')
                    change = next_line.replace(next_line[x+2:-1], Sigma)
                    line=change

                # Range Data Sigma DataLinkSpec_PC_GPS
                # if re.search(r'\bDataLinkSpec_PC_GPS\b', line):
                #     out.write(line)
                #
                # if re.search(r'\bDataLinkSpec_PC_GPS\b', line):
                #     Sigma=str(params[7])
                #     next_line=next(Template)
                #     x = next_line.rfind('a')
                #     change = next_line.replace(next_line[x+2:-1], Sigma)
                #     line=change


                out.writelines(line)

    # call rtgx and wait till its done
    rtgx=subprocess.call(['rtgx', 'Trees/ppp_0.tree'], cwd=path2run,stdout=subprocess.DEVNULL)
    # rtgx = subprocess.call('./test.py', cwd=path2ind)

    # check rtgx ran
    if rtgx != 0:
        print('rtgx failed')
    else:
        print('rtgx ran succesfully')
        return True,path2run

if __name__=="__main__":
    params=[0.195,2.3,0.5,0.005,1000,10,0.01,1]
    generation=1
    idx=1
    # path='/home/src2/Maria/optimizer/data'
    path='/home/WVU-AD/jgross2/optimizer/data'

    flag=write2tree(params=params,solution_idx=idx,generation=generation,path=path)
    print(type(flag))
