
from typing import Dict, Tuple, List
from src.graph_components.node import Node

class Graph:
    """
    Represents a graph data structure with nodes, edges, and pheromone levels for each edge.
    This class supports operations like adding nodes and edges, updating and evaporating pheromones,
    and querying the graph structure for Ant Colony Optimization purposes.
    """
    def __init__(self):
        self.nodes_dict: Dict[str, Node] = {}
        self.edges_dict: Dict[Tuple[str, str], float] = {}
        self.pheromone_levels: Dict[Tuple[str, str], float] = {}
        self.default_pheromone_level = 1.0


    def add_node(self, node: Node) -> None:
        """
        Adds a node to the graph.

        Parameters:
        node (Node): The node object to be added.
        """
        self.nodes_dict[node.id] = node


    def add_edge(self, start_nodeID: str, end_nodeID: str, distance: float) -> None:
        """
        Adds an edge between two nodes and initialises its pheromone level.

        Parameters:
        start_node_id (str): The starting node's ID.
        end_node_id (str): The ending node's ID.
        distance (float): The distance or weight of the edge.
        """

        # Sort the node ID's to ensure consistency in storage and queries
        sorted_edges = tuple(sorted((start_nodeID, end_nodeID)))

        # If given nodeID's present in nodes dictionary
        if start_nodeID in self.nodes_dict and end_nodeID in self.nodes_dict:
            self.edges_dict[sorted_edges] = distance
            self.pheromone_levels[sorted_edges] = self.default_pheromone_level
            print("Successfully connected", start_nodeID.upper(), "to", end_nodeID.upper(), "in edges dictionary.")
        else:
            raise Exception("One or both of the node ID's do not exist.")


    def update_pheromones(self, start_nodeID: str, end_nodeID: str, new_level: float) -> None:
        """
        Updates the pheromone level on an edge between two nodes.

        Parameters:
        start_node_id (str): The starting node's ID.
        end_node_id (str): The ending node's ID.
        new_level (float): The new pheromone level to add to the existing level.
        """

        sorted_edges = tuple(sorted((start_nodeID, end_nodeID)))
        self.pheromone_levels[sorted_edges] += new_level


    def evaporate(self, evaporation_rate: float) -> None:
        """
        Applies evaporation to all pheromone levels in the graph.

        Parameters:
        evaporation_rate (float): The rate at which pheromones evaporate.
        """
        for edge, level in self.pheromone_levels.items():
            self.pheromone_levels[edge] = level * (1 - evaporation_rate)


    def get_connected_nodes(self, node_id: str, prev_node_id: str) -> List[str]:
        """
        Retrieves nodes connected to a given node, optionally excluding a previous node.

        Parameters:
        node_id (str): The ID of the node to find connections for.
        prev_node_id (str, optional): A node ID to exclude from the results.

        Returns:
        List[str]: A list of node IDs that are connected to the given node.
        """
        connected_nodes = []
        for edges in self.edges_dict.keys():
            if node_id in edges:
                other_node = edges[0] if edges[1] == node_id else edges[1]
                if other_node != prev_node_id:
                    connected_nodes.append(other_node)
        return connected_nodes


    def get_distance(self, edge: Tuple[str, str]) -> float:
        """
        Retrieves the distance or weight for a given edge.

        Parameters:
        edge (Tuple[str, str]): The edge represented as a tuple of node IDs.

        Returns:
        float: The distance or weight of the edge.
        """
        sorted_edges = tuple(sorted(edge))
        return self.edges_dict.get(sorted_edges, 0.0)


    def get_pheromone_level(self, edge: Tuple[str, str]) -> float:
        """
        Retrieves the pheromone level for a given edge.

        Parameters:
        edge (Tuple[str, str]): The edge represented as a tuple of node IDs.

        Returns:
        float: The pheromone level of the edge.
        """
        sorted_edges = tuple(sorted(edge))
        return self.pheromone_levels.get(sorted_edges, 0.0)

    def get_node_coordinates(self, node_id: str):
        node = self.nodes_dict.get(node_id)

        # if node variable is not empty
        if node is not None:
            return node.coordinates
        else:
            raise Exception("Error encountered attempting to retrieve node coordinates")


    def print_node_dict(self) -> None:
        print("Dictionary contains:", self.nodes_dict)
        print("Dictionary Keys:", self.nodes_dict.keys())
        print("Dictionary Values:", self.nodes_dict.values())


    def print_pheromone_levels(self):
        print("Pheromones:", self.pheromone_levels)
