import random

from src.utilities.graph import Graph


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

# todo: SHOULD NOT MODIFY THE GRAPHS STATE, IF IT DOES CREATE METHODS IN GRAPH AND CALL THEM
class Ant:
    def __init__(self, graph: Graph, start_node: str) -> None:
        # pass graph object to class level
        self.graph = graph
        # list to record path taken by ant, begin with starting node
        self.path = [start_node]

        # constant, a record of the home node
        self.STARTING_NODE_ID = start_node

        # set to record unvisited nodes, starts with full list of all nodes in graph - starting node
        self.__unvisited_nodes = set(graph.nodes_dict) - {start_node}
        # print("For debugging, set of unvisited nodes:", self.unvisited_nodes)

        # for movement
        self.__current_node = start_node  # the ants current node on the graph, beginning as the starting node
        self.__current_position = self.graph.get_node_coordinates(start_node)  # current x,y coordinate values of ant
        self.__target_node_id = None  # initialise as none as a target has not been selected yet
        self.__speed = 50

        print("Starting node:", self.__current_node)

    # todo: review func
    def move_toward_target(self):

        # get xy coordinates of target node
        target_node_coordinates = self.graph.get_node_coordinates(self.__target_node_id)

        # calculate horizontal difference between ants position and target node
        dx = target_node_coordinates[0] - self.__current_position[0]
        # calculate vertical difference between ants position and target node
        dy = target_node_coordinates[1] - self.__current_position[1]

        # calculate distance to target
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance == 0:
            return  # Already at the target, should select a new target
            # return because the function should no longer run, the ant should stop "moving" towards target

        # convert to unit vector :todo review
        dx, dy = dx / distance, dy / distance

        # Update position based on speed and direction
        self.__current_position = (
            self.__current_position[0] + dx * self.__speed,
            self.__current_position[1] + dy * self.__speed
        )

        # if ant has reached target node
        # Check if reached or passed the target node
        if (dx > 0 and self.__current_position[0] >= target_node_coordinates[0] or
            dx < 0 and self.__current_position[0] <= target_node_coordinates[0]) and \
                (dy > 0 and self.__current_position[1] >= target_node_coordinates[1] or
                 dy < 0 and self.__current_position[1] <= target_node_coordinates[1]):
            # if ant has reached target node, update state
            self.__current_position = target_node_coordinates

            self.__current_node = self.__target_node_id

            self.__target_node_id = None  # Reset target node to allow selection of a new target

    # todo: should be in graph class
    # probability function
    # traverse to next node from current node, based on todo: finish and explain

    # this function in just getting probabilities, it is also getting connected nodes, and checking if a node has been visited
    # todo: CHANGE FUNCTION NAME, it is returning a list of connected nodes and their probabilities
    def get_probabilities(self) -> list[tuple[str, float]]:
        probabilities = []
        total = 0
        # todo: hardcoded for now, amend later
        alpha = 1
        beta = 1

        # list of connected nodes minus the current node
        # get list of connected nodes to current node
        connected_nodes = self.graph.get_connected_nodes(self.__current_node)

        # iterate through list of traversal nodes
        for node in connected_nodes:

            # if current node has not been visited
            if node in self.__unvisited_nodes:
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
        # todo: review and comment!!!!!
        normalised_probabilities = [(node_id, round(probability / total, 2)) for node_id, probability in probabilities]
        print("Traversal probabilities:", normalised_probabilities)
        return normalised_probabilities

    # determines and returns next node based on probabilities calculated
    def get_next_node(self, probabilities: list[tuple[str, float]]) -> str:
        # todo: move method to be called outside see main comment

        # todo: REVIEW
        # if ant has somewhere to go
        if probabilities:
            # todo, review these 2 lines
            node_id, probability = zip(*probabilities)
            next_node = random.choices(node_id, weights=probability, k=1)[0]

            # Update ant state
            # self.current_node = next_node
            self.path.append(next_node)
            print("Path:", self.path)
            self.__unvisited_nodes.remove(next_node)
            print("Next target:", next_node)
            return next_node

        # todo: why is this else satisfied when ant has nowhere to go
        # if probabilities list is empty, change to if all nodes are explored
        elif not probabilities:
            print("reached")

            # if ant has nowhere to go, set target node to home node and return home node
            self.set_target_node(self.STARTING_NODE_ID)

            return self.__target_node_id
            # raise Exception(f"Ant at {self.current_node} has no unvisited neighbors to move to.")

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

    def get_current_position(self):
        return self.__current_position
