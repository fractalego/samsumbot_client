import os
import logging
import numpy as np

from typing import List, Tuple
from gensim.models import KeyedVectors
from sentence_transformers import SentenceTransformer

_path = os.path.dirname(__file__)
_logger = logging.getLogger(__file__)


class DenseRetriever:
    _threshold_length = 5

    def __init__(self, model_name):
        self._sentence_model = SentenceTransformer(model_name, device="cpu")
        self._embeddings_model = KeyedVectors(768)

    def add_text_and_index(self, text: str, index: str):
        embeddings = self._get_embeddings_from_text(text)
        self._embeddings_model.add_vectors([index], [embeddings])
        self._embeddings_model.fill_norms(force=True)

    def get_indices_and_scores_from_text(
        self, text: str, topn: int = 5
    ) -> List[Tuple[str, float]]:
        embeddings = self._get_embeddings_from_text(text)
        return self._embeddings_model.similar_by_vector(embeddings, topn=topn)

    def _get_embeddings_from_text(self, text: str) -> "numpy.array":
        return self._sentence_model.encode(text)

    def get_dot_product(self, lhs: str, rhs: str) -> float:
        lhs_vector = self._sentence_model.encode(lhs)
        rhs_vector = self._sentence_model.encode(rhs)
        return (
            np.dot(lhs_vector, rhs_vector)
            / np.linalg.norm(lhs_vector)
            / np.linalg.norm(rhs_vector)
        )
