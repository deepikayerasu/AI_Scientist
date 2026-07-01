from langchain_text_splitters import RecursiveCharacterTextSplitter


class PaperChunker:
    """
    Splits long research papers into semantic chunks.

    These chunks are later used for:
    - Embeddings
    - Summarization
    - Retrieval
    - Chat
    """

    def __init__(

        self,

        chunk_size=1000,

        chunk_overlap=200

    ):

        self.chunk_size = chunk_size

        self.chunk_overlap = chunk_overlap

        self.splitter = RecursiveCharacterTextSplitter(

            chunk_size=self.chunk_size,

            chunk_overlap=self.chunk_overlap,

            separators=[

                "\n\n",

                "\n",

                ". ",

                " ",

                ""

            ]

        )

    # --------------------------------------------------------

    def split(self, text):

        """
        Split paper into chunks.
        """

        if text is None:

            return []

        text = text.strip()

        if len(text) == 0:

            return []

        chunks = self.splitter.split_text(text)

        return chunks

    # --------------------------------------------------------

    def chunk_statistics(self, chunks):

        """
        Returns statistics about generated chunks.
        """

        stats = {

            "total_chunks": len(chunks),

            "average_length": 0,

            "largest_chunk": 0,

            "smallest_chunk": 0

        }

        if len(chunks) == 0:

            return stats

        lengths = [

            len(chunk)

            for chunk in chunks

        ]

        stats["average_length"] = int(

            sum(lengths)

            / len(lengths)

        )

        stats["largest_chunk"] = max(lengths)

        stats["smallest_chunk"] = min(lengths)

        return stats

    # --------------------------------------------------------

    def process(self, text):

        """
        Complete chunking pipeline.
        """

        chunks = self.split(text)

        statistics = self.chunk_statistics(chunks)

        return {

            "chunks": chunks,

            "statistics": statistics

        }