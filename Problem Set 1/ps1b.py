###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    #If the target weight is already stored in the memo, return its value in the memo
    if target_weight in memo:
#        print('using memo')
        return memo[target_weight]

    #If the target weight is 0 it means that the target weight has been reached,
    #so return 0
    elif target_weight == 0:
        return 0
    
    #Create a list to store the minimum egg usage of the different possible branches
    num_eggs_i = []
    
    #Go through each element in the egg weights. If the element is lower than or equal
    #to the target weight, then add 1 plus the minimum number of eggs used for a trip 
    #with target weight (target_weight - 1) to a variable and append it to the previously
    #made list
    for i in egg_weights:
        if i <= target_weight:
            num_eggs = 1 + dp_make_weight(egg_weights,target_weight - i, memo)
            num_eggs_i.append(num_eggs)
    
    #Find the lowest value of all the possible branches and store it in the memo
    min_ = min(num_eggs_i)
    memo[target_weight] = min_ 
#    print(memo)
    
    #Return said minimum value
    return min_
    
    
# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights =", egg_weights)
    print("n =", n)
#    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()