#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 23:08:56 2019

@author: carlosponce
"""
import random

def stdDev(X):
    mean = sum(X)/len(X)
    tot = 0.0
    for x in X:
        tot += (x - mean)**2 
    return (tot/len(X))**2

def throwNeedles(numNeedles): 
    inCircle = 0
    for Needles in range(1, numNeedles + 1): 
        x = random.random()
        y = random.random()
        if (x*x + y*y)**0.5 <= 1:
            inCircle += 1
#Counting needles in one quadrant only, so multiply by 4 
    return 4*(inCircle/numNeedles)

def getEst(numNeedles, numTrials): 
    estimates = []
    for t in range(numTrials):
        piGuess = throwNeedles(numNeedles) 
        estimates.append(piGuess)
    sDev = stdDev(estimates)
    curEst = sum(estimates)/len(estimates) 
    print('Est. =', str(round(curEst, 5)) + ',','Std. dev. =', str(round(sDev, 5)) + ',','Needles =', numNeedles) 
    return (curEst, sDev)

def estPi(precision, numTrials): 
    numNeedles = 1000
    sDev = precision
    while sDev > precision/1.96:
        curEst, sDev = getEst(numNeedles, numTrials)
        numNeedles *= 2
    return curEst

a = estPi(0.0001,100)
print(a)