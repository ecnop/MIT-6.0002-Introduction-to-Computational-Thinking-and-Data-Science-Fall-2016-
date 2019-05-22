# Problem Set 4: Simulating the Spread of Disease and Bacteria Population Dynamics
# Name:
# Collaborators (Discussion):
# Time:

import math
import numpy as np
import pylab as pl
import random

#random.seed(0)
##########################
# End helper code
##########################

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleBacteria
    and ResistantBacteria classes to indicate that a bacteria cell does not
    reproduce. You should use NoChildException as is; you do not need to
    modify it or add any code.
    """


def make_one_curve_plot(x_coords, y_coords, x_label, y_label, title):
    """
    Makes a plot of the x coordinates and the y coordinates with the labels
    and title provided.

    Args:
        x_coords (list of floats): x coordinates to graph
        y_coords (list of floats): y coordinates to graph
        x_label (str): label for the x-axis
        y_label (str): label for the y-axis
        title (str): title for the graph
    """
    pl.figure()
    pl.plot(x_coords, y_coords)
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()


def make_two_curve_plot(x_coords,
                        y_coords1,
                        y_coords2,
                        y_name1,
                        y_name2,
                        x_label,
                        y_label,
                        title):
    """
    Makes a plot with two curves on it, based on the x coordinates with each of
    the set of y coordinates provided.

    Args:
        x_coords (list of floats): the x coordinates to graph
        y_coords1 (list of floats): the first set of y coordinates to graph
        y_coords2 (list of floats): the second set of y-coordinates to graph
        y_name1 (str): name describing the first y-coordinates line
        y_name2 (str): name describing the second y-coordinates line
        x_label (str): label for the x-axis
        y_label (str): label for the y-axis
        title (str): the title of the graph
    """
    pl.figure()
    pl.plot(x_coords, y_coords1, label=y_name1)
    pl.plot(x_coords, y_coords2, label=y_name2)
    pl.legend()
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()


##########################
# PROBLEM 1
##########################

class SimpleBacteria(object):
    """A simple bacteria cell with no antibiotic resistance"""

    def __init__(self, birth_prob, death_prob):
        """
        Args:
            birth_prob (float in [0, 1]): Maximum possible reproduction
                probability
            death_prob (float in [0, 1]): Maximum death probability
        """
        # Initializes the SimpleBacteria class object with a birth probability
        # and a death probability
        self.birth_prob = birth_prob
        self.death_prob = death_prob
        

    def is_killed(self):
        """
        Stochastically determines whether this bacteria cell is killed in
        the patient's body at a time step, i.e. the bacteria cell dies with
        some probability equal to the death probability each time step.

        Returns:
            bool: True with probability self.death_prob, False otherwise.
        """
        # Stochastically determine weather the bacteria is killed according to
        # the death probability
        return random.random() < self.death_prob

    def reproduce(self, pop_density):
        """
        Stochastically determines whether this bacteria cell reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes.

        The bacteria cell reproduces with probability
        self.birth_prob * (1 - pop_density).

        If this bacteria cell reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleBacteria (which has the same
        birth_prob and death_prob values as its parent).

        Args:
            pop_density (float): The population density, defined as the
                current bacteria population divided by the maximum population

        Returns:
            SimpleBacteria: A new instance representing the offspring of
                this bacteria cell (if the bacteria reproduces). The child
                should have the same birth_prob and death_prob values as
                this bacteria.

        Raises:
            NoChildException if this bacteria cell does not reproduce.
        """
        # Stochastically determines if the bacteria reproduces according to the
        # birth probability and the population density. If it doesn't reproduce,
        # it raises a NoChildException exception
        if random.random() < self.birth_prob * (1 - pop_density):
            return SimpleBacteria(self.birth_prob, self.death_prob)
        else:
            raise NoChildException('Bacteria did not reproduce')


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any
    antibiotics and his/her bacteria populations have no antibiotic resistance.
    """
    def __init__(self, bacteria, max_pop):
        """
        Args:
            bacteria (list of SimpleBacteria): The bacteria in the population
            max_pop (int): Maximum possible bacteria population size for
                this patient
        """
        # Initializes the patient with a list of bacteria and a maximum population
        self.bacteria = bacteria
        self.max_pop = max_pop

    def get_total_pop(self):
        """
        Gets the size of the current total bacteria population.

        Returns:
            int: The total bacteria population
        """
        # Returns the length of the bacteria list, which is the total bacteria
        # population
        return len(self.bacteria)

    def update(self):
        """
        Update the state of the bacteria population in this patient for a
        single time step. update() should execute the following steps in
        this order:

        1. Determine whether each bacteria cell dies (according to the
           is_killed method) and create a new list of surviving bacteria cells.

        2. Calculate the current population density by dividing the surviving
           bacteria population by the maximum population. This population
           density value is used for the following steps until the next call
           to update()

        3. Based on the population density, determine whether each surviving
           bacteria cell should reproduce and add offspring bacteria cells to
           a list of bacteria in this patient. New offspring do not reproduce.

        4. Reassign the patient's bacteria list to be the list of surviving
           bacteria and new offspring bacteria

        Returns:
            int: The total bacteria population at the end of the update
        """
        # Copy the patient's bacteria list so we don't run into any issues later
        bacteria = self.bacteria[:]
        
        # Create an  surviving bacteria list to append all the surviving bacteria
        surviving_bacteria = [i for i in bacteria if not i.is_killed()]
        
#        # For each bacteria in the original bacteria list, determine if the bacterium
#        # dies. If they don't die, append them to the surviving bacteria list
#        for i in bacteria:
#            if not i.is_killed():
#                surviving_bacteria.append(i)
        
        # Calculate current population density
        pop_density = len(surviving_bacteria) / self.max_pop
        
        # Create a new list of child bacteria to append the newly reproduced bacteria
        child_bacteria = []
        
        # For each surviving bacteria, try to have it reproduce and add it to the 
        # child bacteria list. If it fails, catch the exception and pass to the next
        # bacterium
        for i in surviving_bacteria:
            try:
                child_bacteria.append(i.reproduce(pop_density))
            except:
                pass
        
        # Update the bacteria list in the patient's bacteria attribute list
        self.bacteria = surviving_bacteria + child_bacteria
        
        # return the total bacteria population at the end of the update
        return self.get_total_pop()


##########################
# PROBLEM 2
##########################

def calc_pop_avg(populations, n):
    """
    Finds the average bacteria population size across trials at time step n

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria in trial i at time step j

    Returns:
        float: The average bacteria population size at time step n
    """
    # Initialize a bacteria counter
    total_bacteria = 0
    
    # For every list of bacteria populations, add the amount of bacteria present
    # at timestep n to the total bacteria counter
    for i in range(len(populations)):
        total_bacteria += populations[i][n]
        
    # Return the average of the populations across the population lists
    return total_bacteria / len(populations)

def simulation_without_antibiotic(num_bacteria,
                                  max_pop,
                                  birth_prob,
                                  death_prob,
                                  num_trials):
    """
    Run the simulation and plot the graph for problem 2. No antibiotics
    are used, and bacteria do not have any antibiotic resistance.

    For each of num_trials trials:
        * instantiate a list of SimpleBacteria
        * instantiate a Patient using the list of SimpleBacteria
        * simulate changes to the bacteria population for 300 timesteps,
          recording the bacteria population after each time step. Note
          that the first time step should contain the starting number of
          bacteria in the patient

    Then, plot the average bacteria population size (y-axis) as a function of
    elapsed time steps (x-axis) You might find the make_one_curve_plot
    function useful.

    Args:
        num_bacteria (int): number of SimpleBacteria to create for patient
        max_pop (int): maximum bacteria population for patient
        birth_prob (float in [0, 1]): maximum reproduction
            probability
        death_prob (float in [0, 1]): maximum death probability
        num_trials (int): number of simulation runs to execute

    Returns:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria in trial i at time step j
    """
    # Create an empty list of populations to append the results into
    populations = []
    
    # Create an initial bacteria list with num_bacteria simple bacteria
    initial_bacteria = [SimpleBacteria(birth_prob, death_prob) for i in range(num_bacteria)]
        
    # Create variable for the number of steps per trial
    num_steps = 300
    
    # For each trial
    for trial in range(num_trials):
        
        # Instantaite a patient using the list of initial bacteria
        patient = Patient(initial_bacteria, max_pop)
        
        # Create a list where the number of bacteria after each timestep
        # will be appended. Its first entry is the initial number of bacteria
        bacteria = [num_bacteria]
        
        # For 300 timesteps, update the number of bacteria in the patient and
        # record the number of bacteria in each step 
        for i in range(num_steps - 1):
            bacteria.append(patient.update())
        
        # Append the transient list of bacteria populations to the populations list
        populations.append(bacteria)
    
#    print('Appended', len(populations), 'lists of bacteria.')
#    for i in populations:
#        print(i)
    
    # Create a list to store averages across trials
    average_pops = [calc_pop_avg(populations, i) for i in range(num_steps)]
    
    #Plot the average populations vs timesteps
    make_one_curve_plot(range(num_steps), average_pops, 'Timestep', 'Average bacteria population size', \
                        'Average bacteria population over time')
    
    # Return the populations list
    return populations
    
            

# When you are ready to run the simulation, uncomment the next line
#populations = simulation_without_antibiotic(100, 1000, 0.1, 0.025, 50)

##########################
# PROBLEM 3
##########################

def calc_pop_std(populations, t):
    """
    Finds the standard deviation of populations across different trials
    at time step t by:
        * calculating the average population at time step t
        * compute average squared distance of the data points from the average
          and take its square root

    You may not use third-party functions that calculate standard deviation,
    such as numpy.std. Other built-in or third-party functions that do not
    calculate standard deviation may be used.

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria present in trial i at time step j
        t (int): time step

    Returns:
        float: the standard deviation of populations across different trials at
             a specific time step
    """
    # Claculate the average bacteria population size at timestep t
    avg = calc_pop_avg(populations, t)
    
    # Create a variable to store the sum of the squares of the differences between 
    # the datapoint and the average for all of the populations at timestep t
    tot_sum_squares = 0
    
    # Add all of the squares of the differences between the datapoints and the average
    for i in populations:
        tot_sum_squares += (i[t] - avg)**2
        
    # Return the standard deviation
    return (tot_sum_squares / len(populations))**(1/2)
        

def calc_95_ci(populations, t):
    """
    Finds a 95% confidence interval around the average bacteria population
    at time t by:
        * computing the mean and standard deviation of the sample
        * using the standard deviation of the sample to estimate the
          standard error of the mean (SEM)
        * using the SEM to construct confidence intervals around the
          sample mean

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria present in trial i at time step j
        t (int): time step

    Returns:
        mean (float): the sample mean
        width (float): 1.96 * SEM

        I.e., you should return a tuple containing (mean, width)
    """
    # Compute mean and std of the sample
    mean = calc_pop_avg(populations, t)
    std = calc_pop_std(populations, t)
    
    # Estimate the SEM and calculate the width
    SEM = std / len(populations)**(1/2)
    width = 1.96 * SEM
    
    # Return the mean and the width as a tuple
    return (mean, width)

# Custom test including answer to calling calc_95_ci(populations, 298)
#populations = simulation_without_antibiotic(100, 1000, 0.1, 0.025, 50)
#a = calc_95_ci(populations, 298)
#print(a)
#Answers to mean and width of the 95% confidence interval for timestep 299:
#(759.58, 4.094886112604354)
##########################
# PROBLEM 4
##########################

class ResistantBacteria(SimpleBacteria):
    """A bacteria cell that can have antibiotic resistance."""

    def __init__(self, birth_prob, death_prob, resistant, mut_prob):
        """
        Args:
            birth_prob (float in [0, 1]): reproduction probability
            death_prob (float in [0, 1]): death probability
            resistant (bool): whether this bacteria has antibiotic resistance
            mut_prob (float): mutation probability for this
                bacteria cell. This is the maximum probability of the
                offspring acquiring antibiotic resistance
        """
        # Initialize calling the init method from SimpleBacteria
        SimpleBacteria.__init__(self, birth_prob, death_prob)
        
        # Create data attributes for mut_prob and resistant
        self.resistant = resistant
        self.mut_prob = mut_prob
        
    def get_resistant(self):
        """Returns whether the bacteria has antibiotic resistance"""
        return self.resistant

    def is_killed(self):
        """Stochastically determines whether this bacteria cell is killed in
        the patient's body at a given time step.

        Checks whether the bacteria has antibiotic resistance. If resistant,
        the bacteria dies with the regular death probability. If not resistant,
        the bacteria dies with the regular death probability / 4.

        Returns:
            bool: True if the bacteria dies with the appropriate probability
                and False otherwise.
        """
        # If the bacteria has antibiotic resistance, it dies with regular prob,
        # if not, it dies with regular prob / 4.
        if self.get_resistant():
            return random.random() < self.death_prob
        else:
            return random.random() < self.death_prob / 4
            

    def reproduce(self, pop_density):
        """
        Stochastically determines whether this bacteria cell reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A surviving bacteria cell will reproduce with probability:
        self.birth_prob * (1 - pop_density).

        If the bacteria cell reproduces, then reproduce() creates and returns
        an instance of the offspring ResistantBacteria, which will have the
        same birth_prob, death_prob, and mut_prob values as its parent.

        If the bacteria has antibiotic resistance, the offspring will also be
        resistant. If the bacteria does not have antibiotic resistance, its
        offspring have a probability of self.mut_prob * (1-pop_density) of
        developing that resistance trait. That is, bacteria in less densely
        populated environments have a greater chance of mutating to have
        antibiotic resistance.

        Args:
            pop_density (float): the population density

        Returns:
            ResistantBacteria: an instance representing the offspring of
            this bacteria cell (if the bacteria reproduces). The child should
            have the same birth_prob, death_prob values and mut_prob
            as this bacteria. Otherwise, raises a NoChildException if this
            bacteria cell does not reproduce.
        """
        # Stochastically determines if the bacteria reproduces according to the
        # birth probability and the population density. If it doesn't reproduce,
        # it raises a NoChildException exception
        if random.random() < self.birth_prob * (1 - pop_density):
            if self.get_resistant() or random.random() < self.mut_prob * (1-pop_density):
                return ResistantBacteria(self.birth_prob, self.death_prob, True, self.mut_prob)
            else:
                return ResistantBacteria(self.birth_prob, self.death_prob, False, self.mut_prob)
        else:
            raise NoChildException('Bacteria did not reproduce')


class TreatedPatient(Patient):
    """
    Representation of a treated patient. The patient is able to take an
    antibiotic and his/her bacteria population can acquire antibiotic
    resistance. The patient cannot go off an antibiotic once on it.
    """
    def __init__(self, bacteria, max_pop):
        """
        Args:
            bacteria: The list representing the bacteria population (a list of
                      bacteria instances)
            max_pop: The maximum bacteria population for this patient (int)

        This function should initialize self.on_antibiotic, which represents
        whether a patient has been given an antibiotic. Initially, the
        patient has not been given an antibiotic.

        Don't forget to call Patient's __init__ method at the start of this
        method.
        """
        # Initialize calling the init method in the Patient class and creating the 
        # on_antibiotic data attribute and setting it to False
        Patient.__init__(self, bacteria, max_pop)
        self.on_antibiotic = False

    def set_on_antibiotic(self):
        """
        Administer an antibiotic to this patient. The antibiotic acts on the
        bacteria population for all subsequent time steps.
        """
        # Change the on_antibiotic attribute to True
        self.on_antibiotic = True

    def get_resist_pop(self):
        """
        Get the population size of bacteria cells with antibiotic resistance

        Returns:
            int: the number of bacteria with antibiotic resistance
        """
        # Create a comprehension list of 1s. The 1s will only exist for every bacteria 
        # that have resistance. Return the sum of the list
        return sum([1 for i in self.bacteria if i.get_resistant()])

    def update(self):
        """
        Update the state of the bacteria population in this patient for a
        single time step. update() should execute these actions in order:

        1. Determine whether each bacteria cell dies (according to the
           is_killed method) and create a new list of surviving bacteria cells.

        2. If the patient is on antibiotics, the surviving bacteria cells from
           (1) only survive further if they are resistant. If the patient is
           not on the antibiotic, keep all surviving bacteria cells from (1)

        3. Calculate the current population density. This value is used until
           the next call to update(). Use the same calculation as in Patient

        4. Based on this value of population density, determine whether each
           surviving bacteria cell should reproduce and add offspring bacteria
           cells to the list of bacteria in this patient.

        5. Reassign the patient's bacteria list to be the list of survived
           bacteria and new offspring bacteria

        Returns:
            int: The total bacteria population at the end of the update
        """
        # Copy the patient's bacteria list so we don't run into any issues later
        bacteria = self.bacteria[:]
        
        # Create a surviving bacteria list to append all the surviving bacteria
        surviving_bacteria = [i for i in bacteria if not i.is_killed()]
        
        # If the patient is on antibiotics, the surviving bacteria cells from
        # the surviving_bacteria list only survive further if they are resistant, 
        # if the patient is not antibiotics, don't mess with the surviving_bacteria list
        # We can create a comprehension list for this purpose
        if self.on_antibiotic:
            surviving_bacteria = [i for i in surviving_bacteria[:] if i.get_resistant()]
        
        # Calculate current population density
        pop_density = len(surviving_bacteria) / self.max_pop
        
        # Create a new list of child bacteria to append the newly reproduced bacteria
        child_bacteria = []
        
        # For each surviving bacteria, try to have it reproduce and add it to the 
        # child bacteria list. If it fails, catch the exception and pass to the next
        # bacterium
        for i in surviving_bacteria:
            try:
                child_bacteria.append(i.reproduce(pop_density))
            except:
                pass
        
        # Update the bacteria list in the patient's bacteria attribute list
        self.bacteria = surviving_bacteria + child_bacteria
        
        # return the total bacteria population at the end of the update
        return self.get_total_pop()


##########################
# PROBLEM 5
##########################

def simulation_with_antibiotic(num_bacteria,
                               max_pop,
                               birth_prob,
                               death_prob,
                               resistant,
                               mut_prob,
                               num_trials):
    """
    Runs simulations and plots graphs for problem 4.

    For each of num_trials trials:
        * instantiate a list of ResistantBacteria
        * instantiate a patient
        * run a simulation for 150 timesteps, add the antibiotic, and run the
          simulation for an additional 250 timesteps, recording the total
          bacteria population and the resistance bacteria population after
          each time step

    Plot the average bacteria population size for both the total bacteria
    population and the antibiotic-resistant bacteria population (y-axis) as a
    function of elapsed time steps (x-axis) on the same plot. You might find
    the helper function make_two_curve_plot helpful

    Args:
        num_bacteria (int): number of ResistantBacteria to create for
            the patient
        max_pop (int): maximum bacteria population for patient
        birth_prob (float int [0-1]): reproduction probability
        death_prob (float in [0, 1]): probability of a bacteria cell dying
        resistant (bool): whether the bacteria initially have
            antibiotic resistance
        mut_prob (float in [0, 1]): mutation probability for the
            ResistantBacteria cells
        num_trials (int): number of simulation runs to execute

    Returns: a tuple of two lists of lists, or two 2D arrays
        populations (list of lists or 2D array): the total number of bacteria
            at each time step for each trial; total_population[i][j] is the
            total population for trial i at time step j
        resistant_pop (list of lists or 2D array): the total number of
            resistant bacteria at each time step for each trial;
            resistant_pop[i][j] is the number of resistant bacteria for
            trial i at time step j
    """
    # Create an empty list of populations and resistant populations to append the results into
    populations = []
    resistant_pop = []
    
    # Create an initial bacteria list with num_bacteria resistant bacteria
    initial_bacteria = [ResistantBacteria(birth_prob, death_prob, resistant, mut_prob) for i in range(num_bacteria)]
    
    # Create variable for the number of steps per trial
    num_steps = 400
    
    # For each trial
    for trial in range(num_trials):
        
        # Instantaite a treated patient using the list of initial bacteria
        patient = TreatedPatient(initial_bacteria, max_pop)
        
        # Create the lists where the number of bacteria and number of resistant 
        # bacteria after each timestep will be appended. Their first entry are the 
        # initial number of bacteria and the call to the function get_resist_pop on 
        # the patient created, which should be 0
        bacteria = [num_bacteria]
        resistant_bacteria = [patient.get_resist_pop()]
        
        # For 400 timesteps, update the number of bacteria in the patient and
        # record the number of bacteria in each step 
        # Also get the number of resistant bacteria each timestep and add it to 
        # the resistant_bacteria list
        # Put the antibiotic on the patient at step number 151
        for i in range(num_steps - 1):
            if i == 150:
                patient.set_on_antibiotic()
            bacteria.append(patient.update())
            resistant_bacteria.append(patient.get_resist_pop())
            
        # Append the transient list of bacteria populations to the populations lists
        populations.append(bacteria)
        resistant_pop.append(resistant_bacteria)
    
    # Create a list with the averages across trials for both populations
    average_pops = [calc_pop_avg(populations, i) for i in range(num_steps)]
    average_pops_resistant = [calc_pop_avg(resistant_pop, i) for i in range(num_steps)]
    
    #Plot the average populations vs timesteps
    make_two_curve_plot(range(num_steps), average_pops, average_pops_resistant, 'Average total bacteria',\
                        'Average resistant bacteria', 'Timestep', 'Average bacteria population size', \
                        'Average bacteria population over time')
    
    # Return the populations lists
    return (populations, resistant_pop)


# When you are ready to run the simulations, uncomment the next lines one
# at a time
#total_pop, resistant_pop = simulation_with_antibiotic(num_bacteria=100,
#                                                      max_pop=1000,
#                                                      birth_prob=0.3,
#                                                      death_prob=0.2,
#                                                      resistant=False,
#                                                      mut_prob=0.8,
#                                                      num_trials=50)

# 95% confidence intervals at timestep 299 for Simulation A
#t = 298
#ci_total1 = calc_95_ci(total_pop, t)
#ci_resist1 = calc_95_ci(resistant_pop, t)
#print('ci_total1 =', ci_total1)
#print('ci_resist1 =', ci_resist1)
#Answers:
#ci_total1 = (195.46, 8.863398261885788)
#ci_resist1 = (195.46, 8.863398261885788)
#total_pop, resistant_pop = simulation_with_antibiotic(num_bacteria=100,
#                                                      max_pop=1000,
#                                                      birth_prob=0.17,
#                                                      death_prob=0.2,
#                                                      resistant=False,
#                                                      mut_prob=0.8,
#                                                      num_trials=50)

# 95% confidence intervals at timestep 299 for Simulation B
#t = 298
#ci_total2 = calc_95_ci(total_pop, t)
#ci_resist2 = calc_95_ci(resistant_pop, t)
#print('ci_total1 =', ci_total2)
#print('ci_resist1 =', ci_resist2)
#Answers:
#ci_total1 = (0.0, 0.0)
#ci_resist1 = (0.0, 0.0)