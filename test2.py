from importlib.resources import path
import sys
import numpy as np

from tools.getdata import get_position, get_residuals
from tools.fitness import xyz_fit,residuals_fit

path='/home/src2/Maria/testingGA/test1/5'
# generation='test2'
# solution='7'

# path='/home/src2/Maria/optimizer/extraData'
# generation='SIGMATESTING'
# solution='T2'
x,y,z,Time = get_position(solution_idx=None,generation=None,path=path)
# x,y,z,Time = get_position(solution, generation, path)
# phase, TimeP, range, TimeR = get_residuals(solution, generation, path)
# phasefit=residuals_fit(phase, TimeP, range, TimeR)
xyzfitness=xyz_fit(x,y,z,Time)

print(xyzfitness)