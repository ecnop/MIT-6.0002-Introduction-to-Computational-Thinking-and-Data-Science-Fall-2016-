#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 14:20:42 2019

@author: carlosponce
"""

"""
Implement a function that calculates the probability of rolling exactly two 3’s 
in k rolls of a fair die. Use this function to plot the probability as k varies 
from 2 to 100.
"""

import math
import pylab
import scipy.integrate

def binom(n,k,p):
    """
    Aumes n, k are integers
    Asumes p a probability. 0 <= p <= 1
    Returns the probability of a getting k successful events out of n total, no
    matter the order, given that the probability of a k event is p and the 
    events are independent from each other.
    """
    # Get the combination of n choose k
    denominator = math.factorial(k)*math.factorial(n-k)
    n_choose_k = math.factorial(n) / denominator
    
    # Return the probability in question
    return n_choose_k*p**(k)*(1-p)**(n-k)

def binom_dist_over_n(k, minN, maxN, p):
    """
    Asumes minN and maxN integers. Min and max number of events, respectively.
    Asumes k an integer.
    Asumes p a probability of a successful k event. 0 <= p <= 1
    Returns a plot of the binominal probability distribution of k successful events 
    (no matter the order) over n, at a probability of successful event p against, 
    from n = minN to maxN.
    """
    # Get the arrays of probabilities and number of events
    probs, n = [], []
    for i in range(minN, maxN):
        probs.append(binom(i,k,p))
        n.append(i)
        
    # Create the plot
    pylab.figure()
    pylab.title('Probability of getting exactly '+str(k)+' events vs total number of events at probability '+str(round(p,3))+'.')
    pylab.xlabel('Number of total events')
    pylab.ylabel('Probability')
    pylab.plot(n, probs, 'ko')
    pylab.xlim(0, maxN + 1)
    
binom_dist_over_n(2,2,1000,1/32)

# Curious about the integration result
def summation_integral(minN, maxN, k, p):
    """
    Sums the discrete probabilities of events from minN to maxN for a binomial
    distribution over n with k succesful events that occur with a probability of
    p as a fraction.
    """
    cumulative_prob = 0
    for i in range(minN, maxN + 1):
        cumulative_prob += binom(i,k,p)
    
    return cumulative_prob

a = summation_integral(2,1000,2,1/30)
print(a)
    