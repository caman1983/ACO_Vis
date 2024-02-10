"""
Represents a graph data structure
"""
from typing import Dict, Tuple
from src.node import Node


class Graph:
    def __init__(self):
        # self.nodes = {} <- Example of without type inference

        # A dictionary of Node objects, where the key is the nodeID and the value-pair is the node object
        self.nodes_dict: Dict[
            str, Node] = {}  # <- infers self.nodes is a dictionary with a key of nodeId strings and a pair-value of Node objects

        # A dictionary of edges, where the key is a tuple (pair) of nodeIDs
        # The first element is the starting node id and the second is the ending node id
        # The pair-value is the weight between them
        self.edges: Dict[Tuple[str, str], float] = {}

        # A dictionary to record pheromone levels on an edge between two nodes
        # Dict[Tuple <- infers the variable is a dictionary, where the key is a tuple of strings (startNode & endNode)
        # ,float <- the pair-value, which is the pheromone concentration
        self.pheromone_levels: Dict[Tuple[str, str], float] = {}

    # todo: explain function purpose and action
    def add_node(self, node: Node) -> None:
        # we can access node.id because python can dynamically check at runtime
        # however type inference helps demonstrate why we can access the node object attributes, which is because we assume it is a node object

        # todo: explain this line
        self.nodes_dict[node.id] = node

    # Check if both nodeIDs are present in node dictionary and link with given distance metric if true
    def add_edge(self, start_nodeID: str, end_nodeID: str, distance: float) -> None:
        if start_nodeID in self.nodes_dict and end_nodeID in self.nodes_dict:
            # Adds an item to the dictionary, where the key is a tuple of the start_nodeID and the end node_nodeID
            # The pair-value is the given distance metric
            self.edges[(start_nodeID, end_nodeID)] = distance

            self.pheromone_levels[(start_nodeID, end_nodeID)] = 1.0  # initialise default pheromone level between two nodes

        else:
            raise Exception("One of both of the node ID's do not exist.")