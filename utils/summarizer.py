from transformers import pipeline


class PaperSummarizer:
    """
    Research Paper Summarizer

    Improvements
    ------------
    • Loads model only once
    • Skips tiny chunks
    • Never exceeds model token limit
    • Prevents recursive long-summary crashes
    """

    _summarizer = None

    def __init__(self):

        if PaperSummarizer._summarizer is None:

            print("Loading Summarization Model...")

            PaperSummarizer._summarizer = pipeline(
                "summarization",
                model="sshleifer/distilbart-cnn-12-6"
            )

            print("Summarization Model Loaded.")

        self.summarizer = PaperSummarizer._summarizer

    # --------------------------------------------------------

    def summarize_chunk(self, chunk):

        chunk = chunk.strip()

        if len(chunk) < 250:
            return chunk

        words = len(chunk.split())

        max_len = min(120, max(40, words // 2))
        min_len = min(30, max_len // 2)

        try:

            result = self.summarizer(

                chunk,

                max_length=max_len,

                min_length=min_len,

                do_sample=False,

                truncation=True

            )

            return result[0]["summary_text"]

        except Exception:

            return chunk[:400]

    # --------------------------------------------------------

    def summarize_chunks(self, chunks):

        summaries = []

        for chunk in chunks:

            summaries.append(

                self.summarize_chunk(chunk)

            )

        return summaries

    # --------------------------------------------------------

    def executive_summary(self, summaries):

        if len(summaries) == 0:

            return "Unable to generate summary."

        merged = "\n".join(summaries)

        # IMPORTANT
        # Never send huge text to BART

        words = merged.split()

        merged = " ".join(words[:700])

        word_count = len(merged.split())

        max_len = min(180, max(60, word_count // 3))
        min_len = min(60, max_len // 2)

        try:

            result = self.summarizer(

                merged,

                max_length=max_len,

                min_length=min_len,

                do_sample=False,

                truncation=True

            )

            return result[0]["summary_text"]

        except Exception:

            return merged

    # --------------------------------------------------------

    def extract_key_contributions(self, text):

        keywords = [

            "proposed",

            "introduce",

            "introduced",

            "developed",

            "framework",

            "architecture",

            "model",

            "system",

            "novel",

            "contribution"

        ]

        contributions = []

        sentences = text.split(".")

        for sentence in sentences:

            lower = sentence.lower()

            if any(k in lower for k in keywords):

                sentence = sentence.strip()

                if len(sentence) > 20:

                    contributions.append(sentence)

        return contributions[:10]

    # --------------------------------------------------------

    def process(self, chunks, full_text):

        chunk_summaries = self.summarize_chunks(chunks)

        executive = self.executive_summary(

            chunk_summaries

        )

        contributions = self.extract_key_contributions(

            full_text

        )

        return {

            "summary": executive,

            "chunk_summaries": chunk_summaries,

            "key_contributions": contributions

        }