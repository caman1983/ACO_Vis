""" The algorithm's objective is to find the optimal path through a graph structure based on pheromone trails and lowest distance weightings.

Structure:
    Pheromones: Edges in the graph will have associated pheromone levels, which increase ant more ants traverse along the same path
    Decision rule: Ants will choose their next node based on a probabilistic rule that favors edges with higher pheromone levels and lower distances
    Ant: Each ant will be an agent or entity that moves through the graph

    Behaviour:
    Ants will need to:
    Choose a random starting node
    Select the next node based on the decision rule
    Update pheromones on the traversed edges after completion of a tour
"""
from typing import List

from src.ant import Ant
from src.graph import Graph


class ACO:

    # ants: list[Ant] <- example of declaring an instance variable

    def __init__(self, graph: Graph, num_ants: int) -> None:
        # Instance variables:

        # assign constructor parameters to instance variables/class parameter
        self.graph = graph

        # self.ants: List[Ant] <- Declare class attribute ants which takes a list of ant objects
        # Ant(graph) <- Create an ant object, passing in the Graph object given in the class constructor
        # for _ in range(num_ants) <- creates an ant object 'num_ants' times
        # [Ant(graph) for _ in range(num_ants)] <- create an ant object for total number of ants
        self.ants: List[Ant] = [Ant(graph) for _ in range(num_ants)]


