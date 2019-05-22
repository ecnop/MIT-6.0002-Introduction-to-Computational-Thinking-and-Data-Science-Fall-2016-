# -*- coding: utf-8 -*-
# Problem Set 3: Simulating robots
# Name:
# Collaborators (discussion):
# Time:

import math
import random

import ps3_visualize
import pylab

# For python 2.7:
from ps3_verify_movement27 import test_robot_movement


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_new_position(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()
        
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        
        return Position(new_x, new_y)

    def __str__(self):  
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))
    
    def get_xy(self):
        # Returns a tuple of the x and y coordinates
        return (self.x,self.y)
    
    def get_xy_floored(self):
        # Returns a tuple of the floored x and y coordinates
        x = math.floor(self.x)
        y = math.floor(self.y)
        return (x,y)


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. Each tile
    has some fixed amount of dirt. The tile is considered clean only when the amount
    of dirt on this tile is 0.
    """
    def __init__(self, width, height, dirt_amount):
        """
        Initializes a rectangular room with the specified width, height, and 
        dirt_amount on each tile.

        width: an integer > 0
        height: an integer > 0
        dirt_amount: an integer >= 0
        """
        # Initialize the main variables just in case I need them later
        self.width = width
        self.height = int(height)
        self.dirt_amount = dirt_amount
        
        # Initialize a dictionary that will map position objects to dirt amounts
        # This is how we will keep track of the tiles and their dirt amounts
        self.tiles = {}
        
        # Create width*height tiles and distribute dirt uniformly to them 
        for i in range(width):
            for j in range(height):
                self.tiles[(i,j)] = dirt_amount
        
    def clean_tile_at_position(self, pos, capacity):
        """
        Mark the tile under the position pos as cleaned by capacity amount of dirt.

        Assumes that pos represents a valid position inside this room.

        pos: a Position object
        capacity: the amount of dirt to be cleaned in a single time-step
                  can be negative which would mean adding dirt to the tile

        Note: The amount of dirt on each tile should be NON-NEGATIVE.
              If the capacity exceeds the amount of dirt on the tile, mark it as 0.
        """
        # Translate the position to a floored (x,y) tuple
        pos = pos.get_xy_floored()
        
        # Reduce the amount of dirt in a tile by the capacity
        self.tiles[pos] -= capacity
        
        # If the resulting amount of dirt is negative, set the amount of dirt to 0
        if self.tiles[pos] < 0:
            self.tiles[pos] = 0

    def is_tile_cleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        
        Returns: True if the tile (m, n) is cleaned, False otherwise

        Note: The tile is considered clean only when the amount of dirt on this
              tile is 0.
        """
        # Returns the boolean result of comparing the amount of dirt in the m,n tile to 0
        return self.tiles[m,n] == 0

    def get_num_cleaned_tiles(self):
        """
        Returns: an integer; the total number of clean tiles in the room
        """
        # Start a counter at 0
        counter = 0
        
        # Go through all the tiles and add one to the counter if the tile has 0 amount of dirt
        for i in self.tiles:
            if self.tiles[i] == 0:
                counter += 1
       
        # Return the counter
        return counter
        
    def is_position_in_room(self, pos):
        """
        Determines if pos is inside the room.

        pos: a Position object.
        Returns: True if pos is in the room, False otherwise.
        """
        # Translate the position to a floored (x,y) tuple
        pos = pos.get_xy_floored()
        
        # Returns the boolean result of searching the position passed as an argument in the tiles dictionary
        return pos in self.tiles
        
    def get_dirt_amount(self, m, n):
        """
        Return the amount of dirt on the tile (m, n)
        
        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer

        Returns: an integer
        """
        # Returns the amount of dirt of the tile m,n. m is the x-value, n the y-value
        return self.tiles[(m,n)]
        
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        # do not change -- implement in subclasses.
        raise NotImplementedError 
        
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        returns: True if pos is in the room and (in the case of FurnishedRoom) 
                 if position is unfurnished, False otherwise.
        """
        # do not change -- implement in subclasses
        raise NotImplementedError         

    def get_random_position(self):
        """
        Returns: a Position object; a random position inside the room
        """
        # do not change -- implement in subclasses
        raise NotImplementedError        


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times, the robot has a particular position and direction in the room.
    The robot also has a fixed speed and a fixed cleaning capacity.

    Subclasses of Robot should provide movement strategies by implementing
    update_position_and_clean, which simulates a single time-step.
    """
    def __init__(self, room, speed, capacity):
        """
        Initializes a Robot with the given speed and given cleaning capacity in the 
        specified room. The robot initially has a random direction and a random 
        position in the room.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        capacity: a positive interger; the amount of dirt cleaned by the robot 
                  in a single time-step
        """
        
        # Initialize data atributes speed, capacity and room
        self.speed = speed
        self.capacity = capacity
        self.room = room
        
        # Give the robot a random direction and position in the room
        # The position of the robot has float attributes and we are using the method stated in the RectangularRoom class
        # The direction corresponds to a random angle between 0 and 360 degrees, as a float
        self.position = room.get_random_position()
        self.direction = round(random.random()*360,1)

    def get_robot_position(self):
        """
        Returns: a Position object giving the robot's position in the room.
        """
        # Returns the position object of the robot
        return self.position

    def get_robot_direction(self):
        """
        Returns: a float d giving the direction of the robot as an angle in
        degrees, 0.0 <= d < 360.0.
        """
        # Returns the direction of the robot
        return self.direction

    def set_robot_position(self, position):
        """
        Set the position of the robot to position.

        position: a Position object.
        """
        # Change the data attribute of position to the one passed down as an argument
        self.position = position

    def set_robot_direction(self, direction):
        """
        Set the direction of the robot to direction.

        direction: float representing an angle in degrees
        """
        # Set the direction of the robot to direction
        self.direction = direction

    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new random position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and mark the tile it is on as having
        been cleaned by capacity amount. 
        """
        # do not change -- implement in subclasses
        raise NotImplementedError

# === Problem 2
class EmptyRoom(RectangularRoom):
    """
    An EmptyRoom represents a RectangularRoom with no furniture.
    """
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        # Return the amount of keys in the tiles dictionary
        return len(self.tiles)
        
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        Returns: True if pos is in the room, False otherwise.
        """
        # Grab the components of the position and floor them
        # Return a boolean checking to see if the position object of the floored
        # components is in the tiles dictionary
        pos = pos.get_xy_floored()
        return (pos in self.tiles)
        
    def get_random_position(self):
        """
        Returns: a Position object; a valid random position (inside the room).
        """
        # Create random x and y floats within the limits given by the room's
        # width and height
        x = round(random.random()*self.width,1)
        y = round(random.random()*self.height,1)
        
        # Return a position object with these coordinates
        return Position(x,y)

class FurnishedRoom(RectangularRoom):
    """
    A FurnishedRoom represents a RectangularRoom with a rectangular piece of 
    furniture. The robot should not be able to land on these furniture tiles.
    """
    def __init__(self, width, height, dirt_amount):
        """ 
        Initializes a FurnishedRoom, a subclass of RectangularRoom. FurnishedRoom
        also has a list of tiles which are furnished (furniture_tiles).
        """
        # This __init__ method is implemented for you -- do not change.
        
        # Call the __init__ method for the parent class
        RectangularRoom.__init__(self, width, height, dirt_amount)
        # Adds the data structure to contain the list of furnished tiles
        self.furniture_tiles = []
        
    def add_furniture_to_room(self):
        """
        Add a rectangular piece of furniture to the room. Furnished tiles are stored 
        as (x, y) tuples in the list furniture_tiles 
        
        Furniture location and size is randomly selected. Width and height are selected
        so that the piece of furniture fits within the room and does not occupy the 
        entire room. Position is selected by randomly selecting the location of the 
        bottom left corner of the piece of furniture so that the entire piece of 
        furniture lies in the room.
        """
        # This addFurnitureToRoom method is implemented for you. Do not change it.
        furniture_width = random.randint(1, self.width - 1)
        furniture_height = random.randint(1, self.height - 1)

        # Randomly choose bottom left corner of the furniture item.    
        f_bottom_left_x = random.randint(0, self.width - furniture_width)
        f_bottom_left_y = random.randint(0, self.height - furniture_height)

        # Fill list with tuples of furniture tiles.
        for i in range(f_bottom_left_x, f_bottom_left_x + furniture_width):
            for j in range(f_bottom_left_y, f_bottom_left_y + furniture_height):
                self.furniture_tiles.append((i,j))             

    def is_tile_furnished(self, m, n):
        """
        Return True if tile (m, n) is furnished.
        """
        # Return the boolean checking to see if the tuple (m,n) is in the 
        # furniture tiles list
        return (m,n) in self.furniture_tiles
        
    def is_position_furnished(self, pos):
        """
        pos: a Position object.

        Returns True if pos is furnished and False otherwise
        """
        # Grab the x and y components of the position object, returns the boolean
        # the checks to see if the tuple of said floored components is in the 
        # tiles list
        pos = pos.get_xy_floored()
        return pos in self.furniture_tiles
        
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        returns: True if pos is in the room and is unfurnished, False otherwise.
        """
        # Grab the floored components of the position passed on as an argument. 
        # Return the boolean checking to see if the position of the floored components
        # is in the tiles dictionary and that the position is not furnished
        pos1 = pos.get_xy_floored()
        return pos1 in self.tiles and not self.is_position_furnished(pos)
        
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room that can be accessed.
        """
        # Go through all the tiles and count the tiles that are valid
        counter = 0
        for i in range(self.width):
            for j in range(self.height):
                if self.is_position_valid(Position(i,j)):
                    counter += 1
        return counter
        
    def get_random_position(self):
        """
        Returns: a Position object; a valid random position (inside the room and not in a furnished area).
        """
        
        # Create an initial invalid position
        position = Position(-1, -1)
        
        # While the position is not valid, change it to a random position
        while not self.is_position_valid(position):
            x = round(random.random()*self.width,1)
            y = round(random.random()*self.height,1)
            position = Position(x, y)
        
        # Return the position, which should be valid because it got out of the while
        return position
        
        

# === Problem 3
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall or furtniture, it *instead*
    chooses a new direction randomly.
    """
    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new random position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and clean the dirt on the tile
        by its given capacity. 
        """
        robot_position = self.get_robot_position()
        new_position = robot_position.get_new_position(self.get_robot_direction(), self.speed)
        if self.room.is_position_valid(new_position):
            self.set_robot_position(new_position)
            self.room.clean_tile_at_position(new_position, self.capacity)
        else:
            random_direction = round(random.random()*360,1)
            self.set_robot_direction(random_direction)
            
        

# Uncomment this line to see your implementation of StandardRobot in action!
#test_robot_movement(StandardRobot, EmptyRoom)
#test_robot_movement(StandardRobot, FurnishedRoom)

## Custom robot test
#room = EmptyRoom(10,10,100)
#robot  = StandardRobot(room, 1, 10)
#pos = (1,5)
#print(room.tiles)

# === Problem 4
class FaultyRobot(Robot):
    """
    A FaultyRobot is a robot that will not clean the tile it moves to and
    pick a new, random direction for itself with probability p rather
    than simply cleaning the tile it moves to.
    """
    p = 0.15

    @staticmethod
    def set_faulty_probability(prob):
        """
        Sets the probability of getting faulty equal to PROB.

        prob: a float (0 <= prob <= 1)
        """
        FaultyRobot.p = prob
    
    def gets_faulty(self):
        """
        Answers the question: Does this FaultyRobot get faulty at this timestep?
        A FaultyRobot gets faulty with probability p.

        returns: True if the FaultyRobot gets faulty, False otherwise.
        """
        return random.random() < FaultyRobot.p
    
    def update_position_and_clean(self):
        """
        Simulate the passage of a single time-step.

        Check if the robot gets faulty. If the robot gets faulty,
        do not clean the current tile and change its direction randomly.

        If the robot does not get faulty, the robot should behave like
        StandardRobot at this time-step (checking if it can move to a new position,
        move there if it can, pick a new direction and stay stationary if it can't)
        """
        # Set a random direction
        random_direction = round(random.random()*360,1)

        # Check if the robot gets faulty. If the robot gets faulty,
        # do not clean the current tile and change its direction randomly.
        # If the robot does not get faulty, the robot should behave like
        # StandardRobot at this time-step (checking if it can move to a new position,
        # move there if it can, pick a new direction and stay stationary if it can't)
        if self.gets_faulty():
            self.set_robot_direction(random_direction)
        else:
            robot_position = self.get_robot_position()
            new_position = robot_position.get_new_position(self.get_robot_direction(), self.speed)
            if self.room.is_position_valid(new_position):
                self.set_robot_position(new_position)
                self.room.clean_tile_at_position(new_position, self.capacity)
            else:
                self.set_robot_direction(random_direction)
                
    
#test_robot_movement(FaultyRobot, EmptyRoom)

# === Problem 5
def run_simulation(num_robots, speed, capacity, width, height, dirt_amount, min_coverage, num_trials,
                  robot_type):
    """
    Runs num_trials trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction min_coverage of the room.

    The simulation is run with num_robots robots of type robot_type, each       
    with the input speed and capacity in a room of dimensions width x height
    with the dirt dirt_amount on each tile.
    
    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    capacity: an int (capacity >0)
    width: an int (width > 0)
    height: an int (height > 0)
    dirt_amount: an int
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                FaultyRobot)
    """
    # Initialize a num_steps list to store the number of steps every simulation takes to complete
    num_steps = []
    
    # Run the simulation num_trials times
    for j in range(num_trials):
    
        # Create an empty room
        room = EmptyRoom(width, height, dirt_amount)
        
        # Create the robots according to the specifications
        robots = ()
        for i in range(num_robots):
            robots += (robot_type(room, speed, capacity),)
            
        # Initialize a steps counter to count the amount of steps it takes to run the simulation
        steps = 0
        
        # While the fraction of clean tiles to total number of tiles is higher than
        # min_coverage, keep running the update and clean function for all robots
        # and add 1 to the steps list
        while (room.get_num_cleaned_tiles() / room.get_num_tiles()) < min_coverage:
            for k in robots:
                k.update_position_and_clean()
            steps += 1
        
        # After leaving the while, append the number of steps to the num_steps list
        num_steps.append(steps)
    
    # Return the average of num_steps it takes to complete the simulation
    return sum(num_steps) / len(num_steps)
    
    


#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 5, 5, 3, 1.0, 50, StandardRobot)))
#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.8, 50, StandardRobot)))
#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.9, 50, StandardRobot)))
#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))
#print ('avg time steps: ' + str(run_simulation(3, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))

# === Problem 6
#
# ANSWER THE FOLLOWING QUESTIONS:
#
# 1)How does the performance of the two robot types compare when cleaning 80%
#       of a 20x20 room?
# The standard robot does better by around p% (faultiness probability) for every number of robots
#    We can also notice how the times/steps is inversely proportional to the number of robots
#
# 2) How does the performance of the two robot types compare when two of each
#       robot cleans 80% of rooms with dimensions 
#       10x30, 20x15, 25x12, and 50x6?
#The standard robots outperform the faulty ones by around 20%, a little higher than p%.
# It also seems like as the aspect ratio increases, the faulty robot's performance gets
#    progressively worse, compared to the standard robot. It is also worth noticing that
#    the higher the aspect ratio, the more time/steps needed by the robots to clean a 
#    room with the same area.

def show_plot_compare_strategies(title, x_label, y_label):
    """
    Produces a plot comparing the two robot strategies in a 20x20 room with 80%
    minimum coverage.
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print ("Plotting", num_robots, "robots...")
        times1.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, StandardRobot))
        times2.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, FaultyRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    
def show_plot_room_shape(title, x_label, y_label):
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = int(300/width)
        print ("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, StandardRobot))
        times2.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, FaultyRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


show_plot_compare_strategies('Time to clean 80% of a 20x20 room, for various numbers of robots','Number of robots','Time / steps')
#show_plot_room_shape('Time to clean 80% of a 300-tile room for various room shapes','Aspect Ratio', 'Time / steps')
