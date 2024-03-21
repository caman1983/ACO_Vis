import random

from src.utilities.graph import Graph

# THE WHOLE IDEA IS TO PROMOTE LOW COST PATHS

# n = distance to "food"
# t = pheromone level

# step 1: find pheromone level between current node and potential next node
# step 2: calculate inverse of edge weight between current node and potential next node
# step 3: calculate inverse of edge weight between current node and all other connected nodes
# step 4: multiply pheromone levels (trail level) by distance (attractiveness)
# step 5: calculate summation of denominator
# step 6: divide top by bottom

# Eta = inverse of distance
# Tau = current pheromone level
# Q = determines pheromone deposited by each ant - a constant

# todo: SHOULD NOT MODIFY THE GRAPHS STATE, IF IT DOES CREATE METHODS IN GRAPH AND CALL THEM
class Ant:
    def __init__(self, graph: Graph, start_node: str) -> None:
        # pass graph object to class level
        self.graph = graph
        # list to record path taken by ant, begin with starting node
        self.path = [start_node]  # todo: acts as a stack data stucture

        # constant, a record of the home node
        self.STARTING_NODE_ID = start_node

        # for movement
        self.__current_node = start_node  # the ants current node on the graph, beginning as the starting node
        self.__previous_node = None  # Track the previous node to avoid immediate backtracking
        self.__current_position = self.graph.get_node_coordinates(start_node)  # current x,y coordinate values of ant
        self.__target_node_id = None  # initialise as none as a target has not been selected yet
        self.__speed = 9

        #print("Starting node:", self.__current_node) todo: print starting node

    # todo: review func, study this, why does it work
    def move_toward_target(self):

        # get xy coordinates of target node
        target_node_coordinates = self.graph.get_node_coordinates(self.__target_node_id)

        # calculate horizontal difference between ants position and target node
        dx = target_node_coordinates[0] - self.__current_position[0]
        # calculate vertical difference between ants position and target node
        dy = target_node_coordinates[1] - self.__current_position[1]
        # calculate distance to target
        distance = (dx ** 2 + dy ** 2) ** 0.5

        # todo: review
        threshold = max(self.__speed, 5)  # Use speed or a minimum value, e.g., 5 pixels

        if distance > threshold:
            dx /= distance
            dy /= distance
            self.__current_position = (
                self.__current_position[0] + dx * self.__speed,
                self.__current_position[1] + dy * self.__speed,
            )

        else:
            # if ant has reached target node, update ant state todo: change following lines to method

            # Update the previous node before changing the current node
            self.__previous_node = self.__current_node

            # set current position (coordinates) to target node, as target node is reached
            self.__current_position = target_node_coordinates

            # set current node to target node, as target node has been reached
            self.__current_node = self.__target_node_id

            self.__target_node_id = None  # Reset target node to allow selection of a new target

    # this function in just getting probabilities, it is also getting connected nodes, and checking if a node has been visited
    # todo: THIS FUNCTION SHOULD NOT UPDATE ANY STATES - should be in graph class?
    """ Calculates probabilities for traversal of unvisited connected nodes
    
    
    """
    def get_probabilities(self) -> list[tuple[str, float]]:
        probabilities = []
        total = 0
        # todo: hardcoded for now, amend later
        alpha = 1
        beta = 1

        # get list of connected nodes to current node, excluding current and previous node
        connected_nodes = self.graph.get_connected_nodes(self.__current_node, self.__previous_node)

        # iterate through list of traversal nodes
        for node in connected_nodes:

            # get pheromone level between current node and potential next node
            # todo: ensure this works as intended, what if the order is not as expected
            pheromone_level = self.graph.get_pheromone_level((self.__current_node, node))
            # get distance metric between current node and potential next node
            distance = self.graph.get_distance((self.__current_node, node))

            # eta = inverse of distance
            distance_inverse = 1 / distance
            # todo better implement
            if distance <= 0:
                raise Exception("Critical error: Distance between nodes cannot be less then zero")

            # times pheromone level by inverse of distance
            node_potential = pheromone_level * distance_inverse
            probabilities.append((node, node_potential))

            # summation of all node probabilities
            total += node_potential

        # runs upon end of for nodes loop
        # todo: review and comment!!!!!
        normalised_probabilities = [(node_id, round(probability / total, 2)) for node_id, probability in probabilities]
        ##print("------------------------------------")
        ##print("Traversal probabilities:", normalised_probabilities) #todo: print trav possibilities

        return normalised_probabilities
        # todo: returns an empty list if all nodes are visited OR there is nowhere else the ant can go

    # determines and returns next node based on probabilities calculated
    def get_next_node(self, probabilities: list[tuple[str, float]]) -> str:
        # todo: move method to be called outside see main comment

        # todo: REVIEW
        # if ant has somewhere to go (if probabilities list is populated)
        if probabilities:
            # todo, review these 2 lines
            node_id, probability = zip(*probabilities)
            next_node = random.choices(node_id, weights=probability, k=1)[0]

            # Update ant state
            self.path.append(next_node)  # add ants next node to path

            ##print("Path:", self.path)  #todo: print path

            #print("Next target:", next_node) todo: print next target

            return next_node

        # todo: why is this else satisfied when ant has nowhere to go - probabilities list is not populated
        # if probabilities list is empty (ant has nowhere to go) return last node in path
        elif not probabilities:
            #print("Nowhere else to go, backtracking...")

            if len(self.path) > 1:
                self.path.pop()  # Remove current node from path
                backtrack_node = self.path[-1]

                # todo: should return next node, target node is set in main program loop (check main)
                self.set_target_node(backtrack_node)
                return self.__target_node_id

            else:  # todo: why does this else statement run when all nodes are visited?? - if len cond is not satisfied     DOES NOT RUN
                print("all nodes have been visited, returning home...")
                # if ant has nowhere to go, set target node to home node and return home node
                self.set_target_node(self.STARTING_NODE_ID)

                return self.__target_node_id
                # raise Exception(f"Ant at {self.current_node} has no unvisited neighbors to move to.")


    # todo: should this be in ant or graph
    def get_path_length(self):
        total_length = 0

        # iterate i amount of times where i is the length (size of path variable) -1
        # -1 because the last node does not lead to any other node
        for i in range(len(self.path) - 1):
            # get distance between current node element and next node element
            edge_length = self.graph.get_distance((self.path[i], self.path[i+1]))
            total_length += edge_length

        return total_length


    # functions to access and modify private variables, enforcing encapsulation
    # getters setters etc
    # doing this instead of modifying variables from outside their class

    def has_target_node(self) -> bool:
        if self.__target_node_id is not None:
            return True
        else:
            return False

    def set_target_node(self, target_node_id: str):
        self.__target_node_id = target_node_id

    def set_current_node(self, node_id: str):
        self.__current_node = node_id

    def set_previous_node(self, prev_node_id: str):
        self.__previous_node = prev_node_id

    def get_current_position(self):
        return self.__current_position

    def get_current_node(self):
        return self.__current_node

    def get_previous_node(self):
        return self.__previous_node


