###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

filename = 'ps1_cow_data.txt'

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    
    #Open the file and assign it to a variable
    print("Loading cow dictionary from file...")
    file = open(filename, 'r')
    
    #Create empty dictionary to append the values of the file
    cow_dict = {}
    
    #For every line in the file append the first item to the dict as a key,
    #and the second item as its assigned value
    for line in file:
        lis = line.rstrip().split(',')
        cow_dict[lis[0]] = int(lis[1])
     
    #Close the file
    file.close()
    
    #Print a confirmation message
    print("  ", len(cow_dict), "cows loaded.")
    
    #Return the dictionary
    return cow_dict

#Testing the load_cows function and some other things...
#dic = load_cows(filename)
#print(dic)
#list1 = []
#for i in dic.keys():
#    list1.append(i)
#key1 = list1[0]
#value1 = dic[key1]
#print(key1,value1)
#print(type(key1),type(value1))
#file = open(filename)
##a = file.read()
##print(a)
#b = ''.join(list(file))
##b = file.readlines()
#print(b)

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    #Create a sorted list of cows, according to their weight and in reverse
    #order (from most heavy to least heavy)
    sorted_cows = sorted(cows, key=cows.__getitem__, reverse = True)
    
    #Create empty list where the trips will be appended
    trip_list = []
    
    #While the list still has cows that have to be taken
    while sorted_cows != []:
        
        #Set an available variable to the weight limit passsed on as a parameter
        avail = limit
        
        #Create an empty list where the cow names will be appended.
        trip = []
        
        #Go through the sorted cow list. If the weight of the cow is lower than
        #or equal to the available weight in the spaceship, append it to trip and
        #update the available weight in the spaceship
        for i in sorted_cows:
            if cows[i] <= avail:
                trip.append(i)
                avail -= cows[i]
        
        #Append the trip to the list of trips (trip_list) created beforehand
        trip_list.append(trip)
        
        #Update the sorted_cows list by removing from it the cows that have
        #already been transported
        for i in trip:
            sorted_cows.remove(i)
        
    #Return the list of trips
    return trip_list
    
##Testing the greedy_cow_transport function
#dic = load_cows(filename)
#trips = greedy_cow_transport(dic)
#print(dic)
#print(trips)

    
# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    
    #Helper function to determine if a list of trips is valid (the cows' weights
    #of each trip don't exceed the limit)
    #Remember that cows_list is a list of lists of possible trips
    def is_valid_list(cows_list, cows_dict, limit): 
        #Set up a flag that will trun false if the condition is not met
        is_valid = True
        #Go through every list inside the cows_list
        for i in range(len(cows_list)):
            #Set up a variable at 0 that represents the total weight of a trip
            sum_weight = 0
            #Go through each element within the inner list (one trip)
            for j in range(len(cows_list[i])):
                #Add the weights of each element in the list according to the 
                #dictionary passed as an argument
                sum_weight += cows_dict.get(cows_list[i][j],0)
            #If the total weight of any of these trips is larger than the limit
            #change the flag to False
            if sum_weight > limit:
                is_valid = False
        #Return the flag
        return is_valid
            
    
    #Enumerate all the possible ways cows can be divided into separate trips
    possible_trips = []
    for partition in get_partitions(cows):
        possible_trips.append(partition)
    
    #Iterate from 1 to the number of items in the cows dictionary. This is 
    #because this is the maximum number of items that a list in possible_trips
    #can have and therefore the maximum number of trips
    for i in range(1,len(cows)):
        #Go through every item in possible_trips
        for j in possible_trips:
            #If the length of the list is equal to the first iterable, i, and
            #the cows' weights on every list within that list fits in the
            #spaceship, return that list, since it must be in the set of 
            #lowest possible amount of trips to make (since we are going from lowest
            #number of trips to highest number of trips)
            if len(j) == i and is_valid_list(j, cows, limit):
                return j
    
    print('Cannot fit at least one cow in the spaceship.')
    
    return
        
##Testing brute_force_cow_transport
#dic = load_cows(filename)
#a = brute_force_cow_transport(dic)
#print(a)


##Testing get_partitions
#L = []
#cows = load_cows(filename)
#b = [1,2,3,4,5,6,7,8,9,10]
#dic = {'first':1,'second':2,'third':3}
#for partitions in get_partitions(dic):
#    L.append(partitions)
##print(b)
#print(L)

# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    
    #Load the dictionary
    cows = load_cows(filename)
    
    #Test greedy_cow_transport
    start1 = time.time()
    greedy = greedy_cow_transport(cows)
    end1 = time.time()
    time_greedy = str(end1 - start1)
    num_greedy = str(len(greedy))
    
    #Test brute_force_cow_transport
    start2 = time.time()
    brute_force = brute_force_cow_transport(cows,limit=10)
    end2 = time.time()
    time_brute_force = str(end2 - start2)
    num_brute_force = str(len(brute_force))
    
    print('Greedy:')
    print('Number of trips returned:', num_greedy+'.')
    print('Processing time:', time_greedy+'.')
    
    print('========================================')
    
    print('Brute Force:')
    print('Number of trips returned:', num_brute_force+'.')
    print('Processing time:', time_brute_force+'.')
    
    return None

compare_cow_transport_algorithms()