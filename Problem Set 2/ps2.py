# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer: the graph's nodes represent the different buildings in campus,
# and the graph's edges represent the paths from building (source) to building
# (destination). The distances are represented as weighted edges in the graph.
#

filename = 'mit_map.txt'

# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """

    print("Loading map from file...")
    
    # Open the file and assign to the variable file
    file = open(map_filename, 'r')
    
    # Create an empty node set to add all the different node names from file. By
    # using the set type we can omit any duplicate nodes in the file
    # Additionally, create a list of all the weighted edges, to be able to add them to the 
    # graph later
    node_names = set([])
    weighted_edges = []
    for line in file:
#        print(line)
        a, b, c, d = tuple(line.split())
#        a = int(a)
#        b = int(b)
        c = int(c)
        d = int(d)
        node_names.add(a)
        node_names.add(b)
        weighted_edges.append(WeightedEdge(Node(a), Node(b), c, d))
    
    # Transform th node_names into a list of nodes and put them in a nodes list
    nodes = []
    for i in node_names:
        nodes.append(Node(i))
        
    # Create the graph and add all of the nodes and edges to it
    graph = Digraph()
    for i in nodes:
        graph.add_node(i)
    for j in weighted_edges:
        graph.add_edge(j)
    
    # Print a message saying how many edges and nodes were loaded
    print('    '+ str(len(nodes))+ ' nodes loaded.')
    print('    '+ str(len(weighted_edges))+ ' weighted edges loaded.\n')

    # Close the file
    file.close()
    
    return graph
        
    
    
    
# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out
#def test_load_map(filename):
#    graph = load_map(filename)
#    
#    print('Running load_map test...\n')
#    
#    print('Expected output:')
#    print('a->b (1,1)')
#    print('a->c (1,1)')
#    print('a->d (1,1)')
#    print('b->c (1,1)')
#    print('c->d (1,1)')
#    
#    print('\nActual output:')
#    print(graph)
#
#test_load_map('test_load_map.txt')

#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function
# 
# What is the objective function for this problem? What are the constraints?
#
# Answer:
#
# The objective function is:
# min distance traveled from node start to node end
# mathematically = min e.distancetravelled(start, start + 1) + e.distancetravelled(start + 1, start + 2)
# + ... + e.distancetravelled(end - 1, end), where e stands for edges, and the 
# parenthesis are (source node, destination node)
#    
# The constraints is the max_dist_outdoors, so:
# The sum of the distance travelled outdoors must be less than a given parameter
# mathematically = sum(e.distanceoutdoors(i,i+1), from i = start to i+1 = end) <= max_dist_outdoors

# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist,
                  best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    # If the start and end nodes are not in the digraph, raise a ValueError
    if not (Node(start) in digraph.nodes and Node(end) in digraph.nodes):
        raise ValueError('Node not in graph')
    # If we found the end node, return the path passed on as an argument
    elif start == end:
#        print('Current complete path =',path[0])
#        print('Current complete distance =', path[1])
#        print('Current complete outdoor distance =', path[2],'\n')
        return path
    else:
        # Look into every destination node, given by the edges stored in that node
        # Have to use 'Node(start)' because start is given as a string
        for destEdge in digraph.edges[Node(start)]:
            # Check to see if the destination node is already in the path
            # Don't continue if it is already in the path -> we don't want to enter an
            # infinite cycle
            nextNodeName = destEdge.get_destination().get_name()
#            print('Current path =', path)
#            print('Current edge =', destEdge)
#            print('Current best_dist =', best_dist)
            if nextNodeName not in path[0]:
                # Add the current destination node's name to the path and update the distances in the path
                # It's important to copy the list because we don't want to change the original path lists
                updated_list_path = path[0][:]
                updated_path = path[:]
                updated_path[0] = updated_list_path + [nextNodeName]
                updated_path[1] += destEdge.get_total_distance()
                updated_path[2] += destEdge.get_outdoor_distance()
#                print('Updated path =', updated_path)
                # Keep looking for the shortest path if the total traveled distance
                # is lower than the best distance and if the total distance outdoors
                # is lower than the max
                # Ended up separating the max_dist_outdoors condition because the code was going in 
                # to the recursive step, even though max_dist_outdoors was zero and the path it
                # was going into had a non-zero outdoor distance. This was happening because the if condition
                # was returning true due to the best_dist == None condition always being true until the code found
                # the first complete path to the end node (best_dist is initalized at None). 
                if best_dist == None or updated_path[1] < best_dist:
                    if updated_path[2] <= max_dist_outdoors:
                        newPath = get_best_path(digraph, nextNodeName, end, updated_path, max_dist_outdoors, best_dist, best_path)
                        # If the method returns a path, that is, if it finds the end, update best_dist 
                        # and best_path
                        if newPath != None:
#                            print('Updated path:',updated_path)
#                            print('New path:',newPath)
                            best_dist = newPath[1]
                            best_path = newPath[0]
    # If best_dist is None, it means that the code couldn't find a path according to the
    # constraints, therefore return None in that case, if best_dist is not None, then
    # return a tuple of the best path and the best distance
    if not best_dist == None:
        return (best_path, best_dist)      
    else:
        return None
                
                

                


# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    best_dist = None
    best_path = None
    path = [[start],0,0]
    
    # result shoulud be in the order best_path, best_dist, unless it returns none
    result = get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist, best_path)
    
    # If the result is None, it means that no path satisfies the constraints given -> rais a Value Error
    # If the best distance is higher than the max_total_dist, raise a value error
    # Otherwise, return result[0], which is best path as a list of strings
    if result == None:
        raise ValueError('No path satisfies constraints')
    elif result[1] > max_total_dist:
        raise ValueError('Total distance is higher than maximum allowable total distance')
    else:
        return result[0]


# Testing directed_dfs
#test_load_map.txt
digraph = load_map('test_load_map.txt')
best_path = directed_dfs(digraph, 'a', 'd', 100, 100)
print('Best path is =',best_path)

# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


#if __name__ == "__main__":
#    unittest.main()
