import re
from collections import Counter
from utils.llm_engine import LLMEngine


class ChatEngine:
    """
    AI Scientist

    Advanced Semantic Chat Engine

    Features
    --------
    ✓ Better semantic retrieval
    ✓ Query cleaning
    ✓ Query expansion
    ✓ Duplicate removal
    ✓ Context ranking
    ✓ Confidence score
    ✓ Better final context
    """

    def __init__(

        self,

        vector_store,

        embedding_model

    ):

        self.vector_store = vector_store

        self.embedding_model = embedding_model
        self.llm = LLMEngine()

        self.stop_words = {

            "what",
            "which",
            "when",
            "where",
            "why",
            "who",
            "how",
            "is",
            "are",
            "was",
            "were",
            "the",
            "a",
            "an",
            "of",
            "for",
            "to",
            "about",
            "tell",
            "explain",
            "describe"

        }

        self.query_expansion = {

            "algorithm":[

                "method",
                "technique",
                "model",
                "framework"

            ],

            "dataset":[

                "data",
                "benchmark",
                "corpus"

            ],

            "accuracy":[

                "performance",
                "evaluation",
                "metric"

            ],

            "result":[

                "results",
                "performance",
                "evaluation"

            ],

            "future":[

                "future work",
                "future scope"

            ],

            "objective":[

                "goal",
                "purpose",
                "aim"

            ],

            "domain":[

                "field",
                "research area",
                "application"

            ]

        }
            # ---------------------------------------------------------
    # CLEAN QUERY
    # ---------------------------------------------------------

    def clean_query(self, question):

        question = question.lower()

        question = re.sub(

            r"[^a-zA-Z0-9\s]",

            " ",

            question

        )

        words = []

        for word in question.split():

            if word not in self.stop_words:

                words.append(word)

        return " ".join(words)

    # ---------------------------------------------------------
    # EXPAND QUERY
    # ---------------------------------------------------------

    def expand_query(self, question):

        words = question.split()

        expanded = list(words)

        for word in words:

            if word in self.query_expansion:

                expanded.extend(

                    self.query_expansion[word]

                )

        return " ".join(expanded)

    # ---------------------------------------------------------
    # REMOVE DUPLICATE CHUNKS
    # ---------------------------------------------------------

    def remove_duplicates(self, results):

        unique = []

        seen = set()

        for result in results:

            chunk = result["chunk"].strip()

            key = chunk.lower()[:250]

            if key not in seen:

                unique.append(result)

                seen.add(key)

        return unique

    # ---------------------------------------------------------
    # COMPUTE CONFIDENCE
    # ---------------------------------------------------------

    def confidence(self, results):

        if len(results) == 0:

            return 0

        scores = [

            r["score"]

            for r in results

        ]

        score = sum(scores) / len(scores)

        score = max(

            0,

            min(

                100,

                int(score * 100)

            )

        )

        return score

    # ---------------------------------------------------------
    # SEMANTIC SEARCH
    # ---------------------------------------------------------

    def search(

        self,

        question,

        top_k=6

    ):

        if question is None:

            return []

        question = question.strip()

        if len(question) == 0:

            return []

        clean = self.clean_query(

            question

        )

        expanded = self.expand_query(

            clean

        )

        embedding = self.embedding_model.encode_single(

            expanded

        )

        results = self.vector_store.search(

            embedding,

            top_k

        )

        results = self.remove_duplicates(

            results

        )

        return results

    # ---------------------------------------------------------
    # BUILD CONTEXT
    # ---------------------------------------------------------

    def build_context(

        self,

        results

    ):

        context = []

        for result in results:

            chunk = result["chunk"].strip()

            if len(chunk) > 30:

                context.append(chunk)

        context = "\n\n".join(context)

        return context[:3500]
        # ---------------------------------------------------------
    # DETECT QUESTION TYPE
    # ---------------------------------------------------------

    def detect_question_type(self, question):

        question = question.lower()

        mapping = {

            "domain": ["domain", "field", "research area"],

            "algorithm": ["algorithm", "model", "technique"],

            "dataset": ["dataset", "data", "corpus"],

            "methodology": ["method", "methodology", "approach"],

            "results": ["result", "performance", "accuracy"],

            "future_work": ["future", "scope"],

            "objective": ["objective", "goal", "purpose"],

            "problem": ["problem", "challenge", "issue"]

        }

        for category, keywords in mapping.items():

            for keyword in keywords:

                if keyword in question:

                    return category

        return "general"

    

        # ---------------------------------------------------------
    # ASK
    # ---------------------------------------------------------

    def ask(self, question, top_k=6):

        # Retrieve relevant chunks from FAISS
        results = self.search(question, top_k)
                # If nothing relevant was found, return immediately
        if not results:

            return {
                "question": question,
                "question_type": "general",
                "confidence": 0,
                "answer": "No relevant information was found in the uploaded paper.",
                "context": "",
                "results": []
            }

        # Build context from retrieved chunks
        context = self.build_context(results)
        if len(context) > 7000:
           context = context[:7000]


        # Generate answer using Qwen (Ollama)
        answer = self.llm.ask(
            question=question,
            context=context
        )

        # Compute confidence score
        confidence = self.confidence(results)

        # Detect question type
        question_type = self.detect_question_type(question)

        # Return response
        return {
            "question": question,
            "question_type": question_type,
            "confidence": confidence,
            "answer": answer,
            "context": context,
            "results": results
        }
    # ---------------------------------------------------------
    # PRINT RESULTS
    # ---------------------------------------------------------

    def print_results(

        self,

        question,

        top_k=5

    ):

        response = self.ask(

            question,

            top_k

        )

        print("\n")

        print("=" * 70)

        print("AI SCIENTIST CHAT")

        print("=" * 70)

        print("Question :")

        print(response["question"])

        print()

        print("Type :")

        print(response["question_type"])

        print()

        print("Confidence :")

        print(f"{response['confidence']}%")

        print()

        print("Answer")

        print("-" * 70)

        print(response["answer"])

        print()

        print("Retrieved Chunks")

        print("-" * 70)

        for i, result in enumerate(

            response["results"],

            start=1

        ):

            print(f"Rank {i}")

            print(

                f"Similarity : {result['score']:.4f}"

            )

            print(result["chunk"][:400])

            print("-" * 70)