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

                # summation of all node probabilities??
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

        else:
            return
            raise Exception(f"Ant at {self.current_node} has no unvisited neighbors to move to.")

