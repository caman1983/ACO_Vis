import numpy as np
import pandas as pd


class SimilarityData:
    """
    Manages a similarity matrix for content items, providing functionalities to generate and manipulate the matrix.
    """

    def __init__(self, n_contents: int = 5, similarity_threshold: float = 0.5):
        """
        Initialises the SimilarityMatrix with a specific number of content items and a similarity threshold.

        :param n_contents: The number of content items to include in the similarity matrix.
        :param similarity_threshold: The threshold above which content items are considered similar.
        """
        self.n_contents = n_contents
        self.similarity_threshold = similarity_threshold
        self.content_items = [f"Content_{i + 1}" for i in range(n_contents)]
        self.similarity_matrix = self.generate_similarity_matrix()

    def generate_similarity_matrix(self) -> pd.DataFrame:
        """
        Generates a symmetric similarity matrix with self-similarity set to 0 for reproducibility.

        :return: A pandas DataFrame representing the similarity matrix.
        """
        np.random.seed(10)  # Ensure reproducibility
        similarity_scores = np.random.rand(self.n_contents, self.n_contents)
        similarity_scores = (similarity_scores + similarity_scores.T) / 2  # Make symmetric
        np.fill_diagonal(similarity_scores, 0)  # Set diagonal to 0
        similarity_scores = np.round(similarity_scores, 2)  # Round scores for readability

        return pd.DataFrame(similarity_scores, index=self.content_items, columns=self.content_items)



