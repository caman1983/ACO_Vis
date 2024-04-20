import numpy as np
import pandas as pd


class Similarity_DF:
    def __init__(self, n_contents=5, similarity_threshold=0.5):
        self.n_contents = n_contents
        self.similarity_threshold = similarity_threshold
        self.content_items = [f"Content_{i + 1}" for i in range(n_contents)]
        self.similarity_df = self.generate_similarity_matrix()

    def generate_similarity_matrix(self):
        """
        Generates a symmetric similarity matrix with self-similarity set to 0.
        """
        np.random.seed(10)  # Ensure reproducibility
        similarity_scores = np.random.rand(self.n_contents, self.n_contents)
        similarity_scores = (similarity_scores + similarity_scores.T) / 2
        similarity_scores = np.round(similarity_scores, 2)
        np.fill_diagonal(similarity_scores, 0)

        return pd.DataFrame(similarity_scores, index=self.content_items, columns=self.content_items)
