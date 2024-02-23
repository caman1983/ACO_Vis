import random

from src import aco
from src.graph import Graph


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

class Ant:
    def __init__(self, graph: Graph, start_node: str) -> None:
        # graph object
        self.graph = graph

        # current node of an entity, beginning as the starting node id
        self.current_node = start_node

        # list to record path taken by ant, begin with starting node
        self.path = [start_node]

        # set to record unvisited nodes, starts with full list of all nodes in graph - starting node
        self.unvisited_nodes = set(graph.nodes_dict) - {start_node}
        # print("For debugging, set of unvisited nodes:", self.unvisited_nodes)

        # for movement
        self.current_position = self.graph.get_node_coordinates(start_node)
        self.target_node_id = None
        self.speed = 1

    # todo: useless func?
    def set_target_node(self, target_node_id: str):
        self.target_node_id = target_node_id

    def move_toward_target(self):
        if self.target_node_id is None:
            raise Exception("Target nodeID is empty")
        else:
            # get xy coordinates of target node
            target_node_coordinates = self.graph.get_node_coordinates(self.target_node_id)

            # calculate horizontal difference between ants position and target node
            dx = target_node_coordinates[0] - self.current_position[0]
            # calculate vertical difference between ants position and target node
            dy = target_node_coordinates[1] - self.current_position[1]

            # calculate distance to target
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance == 0:
                return  # Already at the target, should select a new target

        # convert to unit vector :todo review
        dx, dy = dx / distance, dy / distance

        # Update position based on speed and direction
        self.current_position = (
            self.current_position[0] + dx * self.speed,
            self.current_position[1] + dy * self.speed
        )

        # Check if reached or passed the target node
        if (dx > 0 and self.current_position[0] >= target_node_coordinates[0] or
            dx < 0 and self.current_position[0] <= target_node_coordinates[0]) and \
            (dy > 0 and self.current_position[1] >= target_node_coordinates[1] or
            dy < 0 and self.current_position[1] <= target_node_coordinates[1]):

            self.current_position = target_node_coordinates

            self.current_node = self.target_node_id

            self.target_node_id = None  # Reset target node to allow selection of a new target



    # todo: should be in graph class
    # probability function
    # traverse to next node from current node, based on todo: finish and explain
    def get_probabilities(self) -> list[tuple[str, float]]:
        probabilities = []
        total = 0
        # todo: hardcoded for now, amend later
        alpha = 1
        beta = 1

        # list of connected nodes minus the current node
        # get list of connected nodes to current node
        traversable_nodes = self.graph.get_connected_nodes(self.current_node)

        # iterate through list of traversal nodes
        for node in traversable_nodes:

            # if current node has not been visited
            if node in self.unvisited_nodes:
                # get pheromone level between current node and potential next node
                # todo: ensure this works as intended, what if the order is not as expected
                pheromone_level = self.graph.get_pheromone_level((self.current_node, node))
                # get distance metric between current node and potential next traversable node
                distance = self.graph.get_distance((self.current_node, node))

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

        normalised_probabilities = [(node_id, round(probability / total, 2)) for node_id, probability in probabilities]
        print(normalised_probabilities)
        return normalised_probabilities

    # todo: REVIEW
    def select_next_node(self):
        probabilities = self.get_probabilities()

        # todo: REVIEW
        # if ant has somewhere to do
        if probabilities:
            # todo, review these 2 lines
            node_id, probability = zip(*probabilities)
            next_node = random.choices(node_id, weights=probability, k=1)[0]

            # Update ant state
            self.current_node = next_node
            self.path.append(next_node)
            self.unvisited_nodes.remove(next_node)
            return next_node
        else:

            raise Exception(f"Ant at {self.current_node} has no unvisited neighbors to move to.")
