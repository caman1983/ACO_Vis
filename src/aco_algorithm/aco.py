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
import random
from typing import List
import numpy as np

from src.aco_algorithm.ant import Ant
from src.utilities.graph import Graph

#RENAME THIS CLASS? todo: RENAME CLASS
class ACO:
    def __init__(self, graph: Graph, num_ants: int) -> None:
        self.graph = graph

        # self.ants: List[Ant] <- Declare class attribute ants which takes a list of ant objects
        # Ant(graph) <- Create an ant object, passing in the Graph object given in the class constructor
        # for _ in range(num_ants) <- creates an ant object 'num_ants' times
        # [Ant(graph) for _ in range(num_ants)] <- create an ant object for total number of ants

        # Creates an ant object equal to the number in num_ants
        self.ants: List[Ant] = [Ant(graph, random.choice(list(graph.nodes_dict.keys()))) for _ in range(num_ants)]
        #self.ants: List[Ant] = [Ant(graph, "Content_1") for _ in range(num_ants)]   #todo: hardcoded for all ants to start in node1, FOR NOW


    # comment
    # Calculate average similarity score for the recommendations
    def average_similarity(self, recommendations, sim_data):
        scores = []
        for i in range(len(recommendations)):
            for j in range(i + 1, len(recommendations)):
                scores.append(sim_data.similarity_df.loc[recommendations[i], recommendations[j]])
        return np.mean(scores)




