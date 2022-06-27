import statistics
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab
from scipy.signal import savgol_filter
from scipy.stats import chisquare, normaltest,kstest, probplot,anderson, gaussian_kde
# from scipy import qqplot
# from statsmodels.graphics.gofplots import qqplot


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
            tdp_file_path=dir_name+'/postfitResiduals.out'
            if os.path.exists(tdp_file_path):
                # out_file_name.append(dir_name+'/finalResiduals.out')
                tdp_file_name.append(dir_name+'/postfitResiduals.out')


#define variables
TIMEP=[]
TIMER=[]
PHASE=[]
RANGE=[]



for i, file in enumerate(tdp_file_name):
    TimeP=[]
    TimeR=[]
    phase=[]
    range=[]
    with open(file,'r') as out:
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
        TIMEP.append(TimeP)
        TIMER.append(TimeR)
        PHASE.append(phase)
        RANGE.append(range)

# print(PHASE)
for i, data in enumerate(PHASE):
    statistic =anderson(data, dist='norm')
    print(statistic)
    # print(np.mean(data),np.std(data))
    # slope, intercept, r=probplot(data, dist="norm",fit=True, plot=pylab)[1]
    # print(r**2)
    # # probplot(data, dist="norm", plot=pylab)
    # pylab.show()
    plt.hist(data, density=True, bins=200, label='Residuals')
    mn, mx = plt.xlim()
    plt.xlim(mn, mx)
    kde_xs = np.linspace(mn, mx, 300)
    kde = gaussian_kde(data)
    plt.plot(kde_xs, kde.pdf(kde_xs), label="PDF")
    plt.legend(loc="upper left")
    plt.ylabel("Probability")
    plt.xlabel("Data")
    plt.title("Histogram")
    plt.show()
    
# fig1, axs = plt.subplots(2,sharex=True)
# fig1.suptitle('Motion in ECEF')
# axs[0].plot(TIMEP[0],PHASE[0],'.', ms = 1)
# axs[0].plot(TIMEP[1],PHASE[1],'.', ms = 1)
# axs[0].plot(TIMEP[2],PHASE[2],'.', ms = 1)
# axs[0].plot(TIMEP[3],PHASE[3],'.', ms = 1)
# axs[0].plot(TIMEP[4],PHASE[4],'.', ms = 1)



# axs[1].plot(TIMER[0],RANGE[0],'.', ms = 1,label='test 1')
# axs[1].plot(TIMER[1],RANGE[1],'.', ms = 1,label='test 2')
# axs[1].plot(TIMER[2],RANGE[2],'.', ms = 1,label='test 3')
# axs[1].plot(TIMER[3],RANGE[3],'.', ms = 1,label='test 4')
# axs[1].plot(TIMER[4],RANGE[4],'.', ms = 1,label='test 5')
# axs[1].legend()
# axs[0].set(ylabel='Phase (cm)')
# axs[1].set(ylabel='Range (cm)')

# plt.xlabel('Time (hours since start)')
# plt.show()