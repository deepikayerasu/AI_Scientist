from sentence_transformers import SentenceTransformer
import numpy as np


class EmbeddingGenerator:

    _model = None

    def __init__(self):

        if EmbeddingGenerator._model is None:

            print("Loading Embedding Model...")

            EmbeddingGenerator._model = SentenceTransformer(
                "sentence-transformers/all-MiniLM-L6-v2"
            )

            print("Embedding Model Loaded.")

        self.model = EmbeddingGenerator._model

    # -----------------------------------------------------

    def encode(self, texts):

        if isinstance(texts, str):
            texts = [texts]

        return self.model.encode(
            texts,
            batch_size=32,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False
        )

    # -----------------------------------------------------

    def encode_single(self, text):

        return self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

    # -----------------------------------------------------

    def embedding_dimension(self):

        return self.model.get_embedding_dimension()

    # -----------------------------------------------------

    def similarity(self, a, b):

        return float(np.dot(a, b))

    # -----------------------------------------------------

    def process(self, chunks):

        embeddings = self.encode(chunks)

        return {

            "chunks": chunks,

            "embeddings": embeddings,

            "dimension": self.embedding_dimension(),

            "count": len(chunks)

        }