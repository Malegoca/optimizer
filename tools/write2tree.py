#!/usr/bin/env python3
import os
import re
import shutil
import subprocess


def write2tree(solutions,solution_idx,generation,path):

    #set directory to store folders for runs
    path2gen=os.path.join(path,str(generation))
    path2ind=os.path.join(path2gen,str(solution_idx))
    path2template=os.path.join(path,'SOLO_GPS')
    # path2template=os.path.join(path,'PIKSI1')

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
                # Trop DryZ
                if re.search(r'\bDryZ\b', line):
                    x=str(solutions[0])
                    change=line.replace(line[11:-1],x)
                    line=change

                # Trop WetZ
                if re.search(r'\bWetZ\b', line):
                    x=str(solutions[1])
                    change=line.replace(line[11:-1],x)
                    line=change

                #Trop Initial Uncertainty and update
                if re.search(r'\bWetZ\b', line): #This copies the line again to compensate for the use of next() below
                    out.write(line)

                if re.search(r'\bWetZ\b', line):
                    TIU=str(solutions[2])
                    TUU=str(solutions[3])
                    next_line=next(Template)
                    x = next_line.find('j')
                    y = next_line.find('$')
                    change = next_line.replace(next_line[x+2:y-1], TIU + ' ' + TUU)
                    line=change
                    # print(line)

                # Position Initial Uncertainty and Update
                if re.search(r'\bPos\b', line):
                    out.write(line)

                if re.search(r'\bPos\b', line):
                    PIU=str(solutions[4])
                    PUU=str(solutions[5])
                    next_line=next(Template)
                    x = next_line.find('j')
                    y = next_line.find('$')
                    change = next_line.replace(next_line[x+2:y-1], PIU + ' ' + PUU)
                    line=change


                # Phase Data Sigma DataLinkSpec_LC_GPS
                if re.search(r'\bDataLinkSpec_LC_GPS\b', line):
                    out.write(line)

                if re.search(r'\bDataLinkSpec_LC_GPS\b', line):
                    Sigma=str(solutions[6])
                    next_line=next(Template)
                    x = next_line.rfind('a')
                    change = next_line.replace(next_line[x+2:-1], Sigma)
                    line=change

                # Range Data Sigma DataLinkSpec_PC_GPS
                # if re.search(r'\bDataLinkSpec_PC_GPS\b', line):
                #     out.write(line)
                #
                # if re.search(r'\bDataLinkSpec_PC_GPS\b', line):
                #     Sigma=str(solutions[7])
                #     next_line=next(Template)
                #     x = next_line.rfind('a')
                #     change = next_line.replace(next_line[x+2:-1], Sigma)
                #     line=change


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
    solutions=[0.195,2.3,0.5,0.005,1000,10,0.01,1]
    generation=1
    idx=1
    # path='/home/src2/Maria/optimizer/data'
    path='/home/WVU-AD/jgross2/optimizer/data'

    flag=write2tree(solutions=solutions,solution_idx=idx,generation=generation,path=path)
    print(type(flag))
