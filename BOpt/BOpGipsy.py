import sys
import numpy as np

from bayes_opt import BayesianOptimization
from bayes_opt.util import UtilityFunction, Colours

import write2tree2 as w
from GA.getdata import get_position, get_residuals
from GA.fitness import xyz_fit,residuals_fit


def black_box_function(wetz,dryz,Iu,Uu,PIu,PUu,Psigma):
    path='/home/WVU-AD/jgross2/optimizer/data'
    params=[wetz,dryz,Iu,Uu,PIu,PUu,Psigma]
    #write parameters to tree and check rtgx ran succesfully
    flag,path2run = w.write2tree(*params, path)

    if flag != True:
        sys.exit() #if rtgx fails stop this program

    #Extract data
    x,y,z,Time = get_position(path2run)
    phase, TimeP, range, TimeR = get_residuals(path2run)

    #Get fitness from this data
    xyzfitness=xyz_fit(x,y,z,Time)
    residualfitness=residuals_fit(phase, TimeP, range, TimeR )

    fitness=xyzfitness+residualfitness
    
    return fitness
# wetz,dryz,Iu,Uu,PIu,PUu,Psigma
pbounds = {'wetz': (0.05, 0.25), 'dryz': (1, 3),'Iu':(0.1,1),'Uu': (0.001,1),'PIu':(5,2000),'PUu':(1,1000),'Psigma':(0.01,1)}

optimizer = BayesianOptimization(
    f=black_box_function,
    pbounds=pbounds,
    random_state=1234,
)

optimizer.maximize(n_iter=20)