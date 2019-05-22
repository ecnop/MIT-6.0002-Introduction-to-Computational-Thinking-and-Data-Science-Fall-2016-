#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 16:36:23 2019

@author: carlosponce
"""

"""
Score = ((60 – (a+b+c+d+e))*F + a*ps1 + b*ps2 + c*ps3 + d*ps4 + e*ps5
Objec<ve:
Given values for F, ps1, ps2, ps3, ps4, ps5
Find values for a, b, c, d, e that maximize score
Constraints:
a, b, c, d, e are each 10 or 0 a + b + c + d + e ≥ 20
"""

import random

#Building the values randomly. First value is F, the rest are ps1 through ps5
def buildGrades(numItems,minVal,maxVal):
    """
    assumes numItems an int corresponding to the amount of graded items in the
    course
    minVal (int) is the minimum value gotten in one of these items
    maxVal (int) is the maximum value gotten in one of these items
    assumes the first item is F, the rest are ps1 through ps(numItems - 1)
    returns a list of numItems values generated randomly between the minVal and
    MaxVal
    """
    list1 = []
    for i in range(numItems):
        list1.append(random.randint(minVal,maxVal))
        
    return list1

#Define a function that gets the score of a given list of grades [F,PS1,...,PS5)
#and choice set list [a,b,c,d,e]
    
def get_score(grades,choices):

    score = 0

    score += grades[0]*(60 - sum(choices))

    for i in range(len(choices)):
        score += grades[i+1]*choices[i]
    
    return score
        

def is_valid(chosen,minScore):
    return (sum(chosen) >= minScore)


#Building the dynamic programming algorithm like the one in chapter13
def maxValue(listGrades, minScore, choiceList = [10, 10, 10, 10, 10, 10], chosenList = []):
    """
    assumes a list of grades (integers) as parameters, a minimum score as a 
    constraint, and a starting choiceList
    returns a tuple with the maxvalue as one value and the 'choices' to make,
    i.e. the values of a through e, as a list, as another value in the tuple
    """        
    #Will be a recursive solution beause we will go down a decision tree of
    #'choose to keep this score or not' and record the highest result that
    #satisfies the constraint given. I didn't need to have a dynamic
    #programming type thing because the problem is specific and no higher
    #order of abstraction for a general solution is required, but it certainly is
    #more effective to build a dynamic programming solution.
    
    if len(choiceList) == 0 : #I could have done this more general, with a parameter but it is trivial
        score = get_score(listGrades,chosenList)
#        print('Chosen list:',chosenList,'|| Score:',score)
        return (score, chosenList)
    else:
        
        
        #calculate score
        score = get_score(listGrades,chosenList)
#        print('Chosen list:',chosenList,'|| Score:',score)
        
        #get best solution from left side
        leftChosen = chosenList[:]
        leftChosen.append(choiceList[0])
        leftScore, leftItems = maxValue(listGrades, minScore, choiceList[1:], leftChosen)
        
        #get best solution from right side
        rightChosen = chosenList[:]
        rightChosen.append(0)
        rightScore, rightItems = maxValue(listGrades, minScore, choiceList[1:], rightChosen)
        
        #compare the three solutions (left, right and parent of these two) and return the
        #highest score with its list. If the answer is not valid, return 0 and an empty list
        
        if not is_valid(chosenList,minScore):
            score, chosenList = (0,[])
        if not is_valid(leftItems,minScore):  
            leftScore, leftItems = (0,[])
        if not is_valid(rightItems,minScore):
            rightScore, rightItems = (0,[])
        
        if max(score, leftScore, rightScore) == score:
            solution = (score, chosenList)
        elif max(score, leftScore, rightScore) == leftScore :
            solution = (leftScore, leftItems)
        else:
            solution = (rightScore, rightItems)
        
        #This is to prin the solution in a five-element list format
        while len(solution[1]) < len(choices):
            solution[1].append(0)
#        print('solution held', solution)
        return solution
    
    
def printGrades(listGrades, Items):
    print('List of grades:\n')
    for i in range(len(Items)):
        print(Items[i]+': '+str(listGrades[i]))
    
def printSolution(solution,choices):
    print('Best solution is:\nFinal Grade:',solution[0])
    
#    while len(solution[1]) < len(choices):
#        solution[1].append(0)
        
        
    for i in range(len(solution[1])):
        print(choices[i]+': '+str(solution[1][i]))
    

Items = ['F','PS1','PS2','PS3','PS4','PS5']
listGrades = buildGrades(7,30,100)
#listGrades = [100,0,0,0,0,0]
printGrades(listGrades, Items)

minScore = 20



solution = maxValue(listGrades, minScore)
choices = ['a','b','c','d','e','f']

print(solution)

#grades = [0,100,100,100,100,100]
#choices1 = [10,10,10,10,10]
#scores1 = get_score(grades,choices1)
#print(scores1)

printSolution(solution,choices)


        
        
        
    
        