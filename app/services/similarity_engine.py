import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class SimilarityEngine:
    @staticmethod
    def cosine(user_vec: np.ndarray, matrix: np.ndarray) -> np.ndarray:
        return cosine_similarity([user_vec], matrix)[0]
