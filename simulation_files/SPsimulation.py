import numpy as np
import pandas as pd
import json
from functions import *


def runSim(springArray, particle, constantsFile):
    
    #return E_loss
    pass

def readConstFile(fileName):
    with open(fileName, 'r') as f:
        constantsDict = json.load(f) #actually read the const file
    return constantsDict

def main():
    fileName = "constants.json"
    constantsDict = readConstFile(fileName)

    #initialize spirng
    N_springs = constantsDict["N"]
    dx = constantsDict["dx"]
    k = constantsDict["k"]
    m = constantsDict["m"]
    springArray = init_springs(N_springs, dx, k, m)

    #initialize particle
    M = constantsDict["M"]
    V_X = 0
    V_Y = constantsDict["V_y"]
    X = 1.4
    Y = 1.5
    R = constantsDict["R"]
    particle = Projectile(M,V_X, V_Y, X, Y, R)

    return runSim(springArray, particle, constantsDict)