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
        print("For debugging, set of unvisited nodes:", self.unvisited_nodes)

    # todo: CURRENTLY ONLY RETURNS PROBABILITY OF TRAVERSING TO NODE IN NUMERATOR
    # probability function
    # traverse to next node from current node, based on todo: finish and explain
    # todo: ask chatGPT if this function is written ok REMOVE BEFORE WEDNESDAY
    def select_next_node(self) -> float:
        probabilities = []

        # todo: hardcoded for now, amend later
        alpha = 1
        beta = 1

        # list of connected nodes minus the current node
        # get list of connected nodes to current node
        traversable_nodes = self.graph.get_connected_nodes(self.current_node)

        # iterate through list of traversal nodes
        print(self.unvisited_nodes)
        for node in traversable_nodes:
            print(node, "for debugging.")

            # if current node has not been visited
            if node in self.unvisited_nodes:

                # get pheromone level between current node and potential next node
                # todo: ensure this works as intended, what if the order is not as expected
                pheromone_level = self.graph.get_pheromone_level((self.current_node, node))

                # get distance metric between current node and potential next node
                distance = self.graph.get_distance((self.current_node, node))

                # eta = inverse of distance
                distance_inverse = 1 / distance
                # todo better implement
                if distance < 0:
                    print(distance)
                    raise Exception("Critical error: Distance between nodes cannot be less then zero")

                else:
                    # store attractiveness of selected node as first item in list, then attractiveness of every other node as every other element

                    # times pheromone level by inverse of distance

                    prob = pheromone_level * distance_inverse
                    probabilities.append(prob)

        numerator = probabilities[0]
        denominator = 0
        for element in probabilities:
            denominator += element

        return numerator / denominator
