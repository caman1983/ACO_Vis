"""
Represents a graph data structure
"""
from typing import Dict, Tuple, List
from src.utilities.node import Node


class Graph:
    # todo: should the methods add_edge & add_node access the node.id instead?
    def __init__(self):
        # self.nodes = {} <- Example of without type inference

        # A dictionary of Node objects, where the key is the nodeID and the value-pair is the node object
        self.nodes_dict: Dict[
            str, Node] = {}  # <- infers self.nodes is a dictionary with a key of nodeId strings and a pair-value of Node objects

        # A dictionary of edges, where the key is a tuple (pair) of nodeIDs
        # The first element is the starting node id and the second is the ending node id
        # The pair-value is the weight between them
        self.edges_dict: Dict[Tuple[str, str], float] = {}

        # A dictionary to record pheromone levels on an edge between two nodes
        # Dict[Tuple <- infers the variable is a dictionary, where the key is a tuple of strings (startNode & endNode)
        # ,float <- the pair-value, which is the pheromone concentration
        # if a tuple of two nodes exists, an edge is present between them on the graph

        # key is tuple of connected nodeID's, pair value is pheromone level
        self.pheromone_levels: Dict[Tuple[str, str], float] = {}

        self.default_pheromone_level = 1

    # todo: explain function purpose and action
    def add_node(self, node: Node) -> None:
        # we can access node.id because python can dynamically check at runtime
        # however type inference helps demonstrate why we can access the node object attributes, which is because we assume it is a node object

        # todo: explain this line
        self.nodes_dict[node.id] = node
        # print(node.id)

    # Check if both nodeIDs are present in node dictionary and link with given distance metric if true
    def add_edge(self, start_nodeID: str, end_nodeID: str, distance: float) -> None:
        # Sort the node ID's to ensure consistency in storage and queries - order does not matter
        sorted_edges = tuple(sorted((start_nodeID, end_nodeID)))

        # If given nodeID's present in nodes dictionary
        if start_nodeID in self.nodes_dict and end_nodeID in self.nodes_dict:
            # Adds an item to the dictionary, where the key is a tuple of the start_nodeID and the end node_nodeID
            # The pair-value is the given distance metric
            # Add nodes to edges dictionary
            self.edges_dict[sorted_edges] = distance

            # initialise default pheromone level between two nodes
            self.pheromone_levels[sorted_edges] = self.default_pheromone_level

            print("Successfully connected", start_nodeID.upper(), "to", end_nodeID.upper(), "in edges dictionary.")

        else:
            raise Exception("One or both of the node ID's do not exist.")

    # todo: should this function node be in the ACO class?
    def update_pheromones(self, start_nodeID: str, end_nodeID: str, new_level: float) -> None:
        sorted_edges = tuple(sorted((start_nodeID, end_nodeID)))

        # if (start_nodeID, end_nodeID) in self.pheromone_levels: # todo: not working as intended, commented out for now
        # if start node and end node present and linked (a tuple of the two exists) update pheromone levels to given float
        self.pheromone_levels[sorted_edges] += new_level

        # else:
        # raise Exception("An edge between", start_nodeID, "and", end_nodeID, "does not exist.")

    # todo: should this not be in the aco class?
    # todo: review maths behind this (pheromone evaporation rule) CHANGE THIS FUNCTION
    def evaporate(self, evaporation_rate: float) -> None:
        # todo: explain these lines
        # iterates through pheromone_level dictionary, where edge = key (tuple) and pheromone_level = pair value
        for edge, pheromone_level in self.pheromone_levels.items():
            # change current edges pheromone level by evaporation rate
            self.pheromone_levels[edge] = pheromone_level * (1 - evaporation_rate)

    # if given node id present in dictionary key,
    # returns a list of connected edges, excluding given node
    # todo: explain this function
    # get connected nodes to given node
    def get_connected_nodes(self, node_id: str, prev_node_id: str) -> List[str]:
        connected_nodes = []
        # iterate through tuple key in edges dictionary
        for edges in self.edges_dict.keys():
            # check if node_id present in keys
            if node_id in edges:
                # todo: review
                other_node = edges[0] if edges[1] == node_id else edges[1]
                if other_node != prev_node_id:
                    connected_nodes.append(other_node)
        # return list of connected nodes, excluding given node and previous node
        return connected_nodes

    # returns distance between two given nodes (edges_dictionary key)
    # todo: why does sorting work
    def get_distance(self, edge: Tuple[str, str]) -> float:
        sorted_edges = tuple(sorted(edge))
        # .get = return pair value for given key
        # if key not present, return 0.0
        return self.edges_dict.get(sorted_edges, 0.0)

    # return pheromone level for given key in dictionary (tuple of edges)
    def get_pheromone_level(self, edge: Tuple[str, str]) -> float:
        sorted_edges = tuple(sorted(edge))
        return self.pheromone_levels.get(sorted_edges, 0.0)

    def get_node_coordinates(self, node_id: str):
        node = self.nodes_dict.get(node_id)

        # if node variable is not empty
        if node is not None:
            return node.coordinates
        else:
            raise Exception("add error message")

    # print node dictionary contents in readable format
    def print_node_dict(self) -> None:
        print("Dictionary contains:", self.nodes_dict)
        print("Dictionary Keys:", self.nodes_dict.keys())
        print("Dictionary Values:", self.nodes_dict.values())

    def print_pheromone_levels(self):
        print("Pheromones:", self.pheromone_levels)


    # returns a list of items which are related to each other including some novel options due to random spawns
    # use case: a user wants a list of related content within a specific genre
    # addresses cold start!


    # returns a list of items which are related to a given node (starting_node)
    # use case: a user wants a list of content related to a piece of content he's just consumed
    def extract_local_recommendations(self):
        # todo: Return recommendations based on a given node
        pass
