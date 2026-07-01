import faiss
import numpy as np


class VectorStore:
    """
    FAISS Vector Store for Research Papers.

    Stores:
        - Embeddings
        - Corresponding text chunks

    Supports:
        - Similarity Search
        - Top-K Retrieval
    """

    def __init__(self):

        self.index = None

        self.chunks = []

        self.dimension = None

    # ---------------------------------------------------------

    def build(self, chunks, embeddings):
        """
        Build FAISS index.
        """

        if len(chunks) == 0:
            raise ValueError("No chunks provided.")

        if len(embeddings) == 0:
            raise ValueError("No embeddings provided.")

        self.dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(
            self.dimension
        )

        embeddings = np.asarray(
            embeddings,
            dtype=np.float32
        )

        self.index.add(
            embeddings
        )

        self.chunks = chunks

        print(
            f"FAISS Index Created ({len(chunks)} chunks)"
        )

    # ---------------------------------------------------------

    def search(self,
               query_embedding,
               top_k=5):
        """
        Semantic Search.
        """

        if self.index is None:
            raise ValueError(
                "Vector store has not been built."
            )

        query_embedding = np.asarray(
            [query_embedding],
            dtype=np.float32
        )

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, idx in zip(
            scores[0],
            indices[0]
        ):

            if idx == -1:
                continue

            results.append(

                {

                    "chunk": self.chunks[idx],

                    "score": float(score)

                }

            )

        return results

    # ---------------------------------------------------------

    def chunk_count(self):

        return len(self.chunks)

    # ---------------------------------------------------------

    def save(self,
             path):

        if self.index is None:

            raise ValueError(
                "No FAISS index found."
            )

        faiss.write_index(
            self.index,
            path
        )

        print(
            "FAISS index saved."
        )

    # ---------------------------------------------------------

    def load(self,
             path):

        self.index = faiss.read_index(
            path
        )

        self.dimension = self.index.d

        print(
            "FAISS index loaded."
        )

    # ---------------------------------------------------------

    def statistics(self):

        return {

            "dimension": self.dimension,

            "vectors": self.index.ntotal
            if self.index
            else 0,

            "chunks": len(
                self.chunks
            )

        }

    # ---------------------------------------------------------

    def clear(self):

        self.index = None

        self.chunks = []

        self.dimension = None