import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingRanker:

    def __init__(self, embedding_path="processed/embeddings.pkl"):

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        with open(embedding_path, "rb") as f:
            self.candidate_embeddings = pickle.load(f)

    def encode_job_description(self, job_description):
        """
        Convert Job Description into embedding.
        """

        embedding = self.model.encode(
            job_description,
            convert_to_numpy=True
        )

        return embedding.reshape(1, -1)

    def rank(self, candidates, job_description, top_k=100):
        """
        Rank candidates using semantic similarity.
        """

        jd_embedding = self.encode_job_description(job_description)

        similarities = cosine_similarity(
            jd_embedding,
            self.candidate_embeddings
        )[0]

        ranked = sorted(
            zip(candidates, similarities),
            key=lambda x: x[1],
            reverse=True
        )

        return ranked[:top_k]

    def get_similarity_scores(self, job_description):
        """
        Returns similarity score for every candidate.
        Useful for hybrid ranking.
        """

        jd_embedding = self.encode_job_description(job_description)

        scores = cosine_similarity(
            jd_embedding,
            self.candidate_embeddings
        )[0]

        return scores