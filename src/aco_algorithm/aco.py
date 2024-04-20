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


# RENAME THIS CLASS? todo: RENAME CLASS
class ACO:
    def __init__(self, graph: Graph, num_ants: int) -> None:
        self.graph = graph

        # self.ants: List[Ant] <- Declare class attribute ants which takes a list of ant objects
        # Ant(graph) <- Create an ant object, passing in the Graph object given in the class constructor
        # for _ in range(num_ants) <- creates an ant object 'num_ants' times
        # [Ant(graph) for _ in range(num_ants)] <- create an ant object for total number of ants

        # Creates an ant object equal to the number in num_ants
        #self.ants: List[Ant] = [Ant(graph, random.choice(list(graph.nodes_dict.keys()))) for _ in range(num_ants)]
        self.ants: List[Ant] = [Ant(graph, "Content_1") for _ in range(num_ants)]   #todo: hardcoded for all ants to start in node1, FOR NOW

    # Done!
    # Calculate average similarity score for the recommendations
    def average_similarity(self, recommendations, sim_data):
        scores = []
        for i in range(len(recommendations)):
            for j in range(i + 1, len(recommendations)):
                scores.append(sim_data.similarity_df.loc[recommendations[i], recommendations[j]])
        return np.mean(scores)

    def calculate_diversity_score(self, recommendations, sim_data):
        # Ensure there are at least 2 items to compare
        if len(recommendations) < 2:
            return 0

        total_dissimilarity = 0
        count = 0

        # Calculate the sum of dissimilarities for all unique pairs
        for i in range(len(recommendations)):
            for j in range(i + 1, len(recommendations)):
                similarity_score = sim_data.similarity_df.loc[recommendations[i], recommendations[j]]
                dissimilarity_score = 1 - similarity_score
                total_dissimilarity += dissimilarity_score
                count += 1

        # Calculate the average dissimilarity (diversity score)
        diversity_score = total_dissimilarity / count
        return diversity_score


    def calculate_coverage(self, total_items_count, recommendations):
        # Number of unique items recommended
        unique_recommended_items_count = len(set(recommendations))

        # Calculate coverage
        coverage = (unique_recommended_items_count / total_items_count) * 100
        return coverage


    def extract_global_recommendations(self, pheromone_threshold=1):
        # Calculate the pheromone threshold based on the specified percentile
        pheromone_values = list(self.graph.pheromone_levels.values())
        if not pheromone_values:  # Ensure there are pheromone values to calculate the threshold
            return []

        # Filter edges by the dynamically calculated pheromone threshold
        filtered_edges = [(edge, level) for edge, level in self.graph.pheromone_levels.items() if level >= pheromone_threshold]

        # Sort filtered edges by pheromone level in descending order
        sorted_edges = sorted(filtered_edges, key=lambda x: x[1], reverse=True)

        # Extract unique nodes from the filtered and sorted edges
        recommendations = set()
        for edge, _ in sorted_edges:
            recommendations.update(edge)

        return list(recommendations)
