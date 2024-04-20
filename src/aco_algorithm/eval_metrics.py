import numpy as np


class EvalMetrics:
    """
       A class for ACO-related calculations. This class is not intended to be instantiated.
       All methods are static and operate on provided inputs.
       """
    def __init__(self, graph):
        self.graph = graph


    @staticmethod
    # Calculate average similarity score for the recommendations
    def average_similarity(recommendations, sim_data):
        scores = []
        for i in range(len(recommendations)):
            for j in range(i + 1, len(recommendations)):
                scores.append(sim_data.similarity_matrix.loc[recommendations[i], recommendations[j]])
        return np.mean(scores)

    @staticmethod
    def calculate_diversity_score(recommendations, sim_data):
        # Ensure there are at least 2 items to compare
        if len(recommendations) < 2:
            return 0

        total_dissimilarity = 0
        count = 0

        # Calculate the sum of dissimilarities for all unique pairs
        for i in range(len(recommendations)):
            for j in range(i + 1, len(recommendations)):
                similarity_score = sim_data.similarity_matrix.loc[recommendations[i], recommendations[j]]
                dissimilarity_score = 1 - similarity_score
                total_dissimilarity += dissimilarity_score
                count += 1

        # Calculate the average dissimilarity (diversity score)
        diversity_score = total_dissimilarity / count
        return diversity_score

    @staticmethod
    def calculate_coverage(total_items_count, recommendations):
        # Number of unique items recommended
        unique_recommended_items_count = len(set(recommendations))

        # Calculate coverage
        coverage = (unique_recommended_items_count / total_items_count) * 100
        return coverage

    # @staticmethod
    # def extract_global_recommendations(graph, pheromone_threshold=1):
    #     # Calculate the pheromone threshold based on the specified percentile
    #     pheromone_values = list(graph.pheromone_levels.values())
    #     if not pheromone_values:  # Ensure there are pheromone values to calculate the threshold
    #         return []
    #
    #     # Filter edges by the dynamically calculated pheromone threshold
    #     filtered_edges = [(edge, level) for edge, level in graph.pheromone_levels.items() if
    #                       level >= pheromone_threshold]
    #
    #     # Sort filtered edges by pheromone level in descending order
    #     sorted_edges = sorted(filtered_edges, key=lambda x: x[1], reverse=True)
    #
    #     # Extract unique nodes from the filtered and sorted edges
    #     recommendations = set()
    #     for edge, _ in sorted_edges:
    #         recommendations.update(edge)
    #
    #     return list(recommendations)





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