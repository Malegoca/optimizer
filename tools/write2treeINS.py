#!/usr/bin/env python3
import os
import re
import shutil
import subprocess


def write2tree(solutions,solution_idx,generation,path):

    #set directory to store folders for runs
    path2gen=os.path.join(path,str(generation))
    path2ind=os.path.join(path2gen,str(solution_idx))
    # path2template=os.path.join(path,'SOLO_GPS')
    path2template=os.path.join(path,'PIKSI3')

    isexistG=os.path.exists(path2gen)
    isexistI=os.path.exists(path2ind)

    #create directories if they don't exist
    if not isexistG:
        os.mkdir(path2gen)

    if not isexistI:
        os.mkdir(path2ind)

    #define file handles
    template=os.path.join(path2template,'Trees/ppp_0.tree')
    #make tree dir for out file
    outdir=os.path.join(path2ind,'Trees')
    os.mkdir(outdir)
    outfile=os.path.join(outdir,'ppp_0.tree')

    #write to tree in respective directory
    with open(template,'r') as Template:
        with open(outfile,'w+') as out:

            for line in Template:

                # Position Initial Uncertainty and Update
                if re.search(r'\bPos\b', line):
                    out.write(line)

                if re.search(r'\bPos\b', line):
                    PIU=str(solutions[0])
                    PUU=str(solutions[1])
                    next_line=next(Template)
                    x = next_line.find('j')
                    y = next_line.find('$')
                    change = next_line.replace(next_line[x+2:y-1], PIU + ' ' + PUU)
                    line=change
                # Velocity Initial Uncertainty and Update
                if re.search(r'\bVel\b', line):
                    out.write(line)

                if re.search(r'\bVel\b', line):
                    VIU=str(solutions[2])
                    VUU=str(solutions[3])
                    next_line=next(Template)
                    x = next_line.find('j')
                    y = next_line.find('$')
                    change = next_line.replace(next_line[x+2:y-1], VIU + ' ' + VUU)
                    line=change
                # Attitute Initial Uncertainty and Update
                if re.search(r'\bAttitute\b', line):
                    out.write(line)

                if re.search(r'\bAttitute\b', line):
                    AIU=str(solutions[4])
                    AUU=str(solutions[5])
                    next_line=next(Template)
                    x = next_line.find('j')
                    y = next_line.find('$')
                    change = next_line.replace(next_line[x+2:y-1], AIU + ' ' + AUU)
                    line=change
                 # AccelerometerBias Initial Uncertainty and Update
                if re.search(r'\bAccelerometerBias\b', line):
                    out.write(line)

                if re.search(r'\bAccelerometerBias\b', line):
                    BIU=str(solutions[6])
                    BUU=str(solutions[7])
                    next_line=next(Template)
                    x = next_line.find('j')
                    y = next_line.find('$')
                    change = next_line.replace(next_line[x+2:y-1], BIU + ' ' + BUU)
                    line=change
                 # GyroBias Initial Uncertainty and Update
                if re.search(r'\bGyroBias\b', line):
                    out.write(line)

                if re.search(r'\bGyroBias\b', line):
                    GIU=str(solutions[8])
                    GUU=str(solutions[9])
                    next_line=next(Template)
                    x = next_line.find('j')
                    y = next_line.find('$')
                    change = next_line.replace(next_line[x+2:y-1], GIU + ' ' + GUU)
                    line=change


                out.writelines(line)

    #copy all files in template directory to new tree file directory for rtgx run
    files=os.listdir(path2template)
    # print(files)
    for fname in files:
        file=os.path.join(path2template,fname)
        if os.path.isfile(file):
            shutil.copy(file, path2ind)
    #copy GNSSinitvalues folders
    folder_path_src=os.path.join(path2template,'GNSSinitValues')
    folder_path_dst=os.path.join(path2ind,'GNSSinitValues')
    shutil.copytree(folder_path_src,folder_path_dst)

    # call rtgx and wait till its done
    rtgx=subprocess.call(['rtgx', 'Trees/ppp_0.tree'], cwd=path2ind,stdout=subprocess.DEVNULL)
    # rtgx = subprocess.call('./test.py', cwd=path2ind)
    # print(rtgx)
    #delete iterRTGx folder to save space
    iterfolder='iterRtgx'
    path2folder=os.path.join(path2ind,iterfolder)
    shutil.rmtree(path2folder)
    # check rtgx ran
    if rtgx != 0:
        print('rtgx failed')
    else:
        print('rtgx ran succesfully')
        return True

if __name__=="__main__":
    solutions=[1000,100,50,10,0.1,0.001,0.02,0.0002,0.003,0.00003]
    generation=1
    idx=1
    path='/home/src2/Maria/testingGA'
    # path='/home/WVU-AD/jgross2/optimizer/data'

    flag=write2tree(solutions=solutions,solution_idx=idx,generation=generation,path=path)
    print(type(flag))
