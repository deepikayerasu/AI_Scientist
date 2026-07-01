import re
from collections import Counter


class ResearchAnalyzer:
    """
    AI Scientist

    Advanced Research Paper Analyzer

    Extracts

    ✓ Research Domain
    ✓ Research Problem
    ✓ Research Gap
    ✓ Objective
    ✓ Methodology
    ✓ Algorithms
    ✓ Dataset
    ✓ Evaluation Metrics
    ✓ Results
    ✓ Novel Contributions
    ✓ Strengths
    ✓ Limitations
    ✓ Applications
    ✓ Future Work
    """

    def __init__(self):

        self.categories = {

            "problem":[

                "problem",
                "challenge",
                "issue",
                "motivation",
                "difficulty",
                "lack",
                "fails",
                "limitations of existing"

            ],

            "objective":[

                "objective",
                "aim",
                "goal",
                "purpose",
                "this paper proposes",
                "we propose",
                "this work presents"

            ],

            "methodology":[

                "method",
                "methodology",
                "framework",
                "architecture",
                "approach",
                "pipeline",
                "workflow",
                "system design",
                "implementation"

            ],

            "algorithm":[

                "algorithm",
                "dijkstra",
                "a*",
                "astar",
                "cnn",
                "rnn",
                "lstm",
                "gru",
                "bert",
                "transformer",
                "xgboost",
                "random forest",
                "svm",
                "decision tree",
                "knn",
                "naive bayes"

            ],

            "dataset":[

                "dataset",
                "benchmark",
                "corpus",
                "data set",
                "kaggle",
                "uci",
                "imagenet",
                "cifar",
                "mnist"

            ],

            "metrics":[

                "accuracy",
                "precision",
                "recall",
                "f1",

                "auc",

                "specificity",

                "latency",

                "delay",

                "packet delivery ratio",

                "throughput",

                "rmse",

                "mae",

                "mse"

            ],

            "results":[

                "results",

                "performance",

                "experimental results",

                "evaluation",

                "improved",

                "achieved",

                "obtained"

            ],

            "limitations":[

                "limitation",

                "limitations",

                "drawback",

                "future challenge",

                "constraint"

            ],

            "future_work":[

                "future work",

                "future scope",

                "future research",

                "in future",

                "can be extended"

            ]

        }

        self.domain_keywords = {

            "Artificial Intelligence":[

                "artificial intelligence",

                "machine learning",

                "deep learning",

                "neural network"

            ],

            "Computer Vision":[

                "image",

                "vision",

                "cnn",

                "object detection"

            ],

            "Natural Language Processing":[

                "bert",

                "language model",

                "nlp",

                "text"

            ],

            "Networking":[

                "routing",

                "mesh",

                "network",

                "wifi",

                "wireless",

                "ble"

            ],

            "Cyber Security":[

                "attack",

                "security",

                "malware",

                "intrusion"

            ],

            "Internet of Things":[

                "iot",

                "sensor",

                "embedded"

            ]

        }
            # --------------------------------------------------------
    # TEXT CLEANING
    # --------------------------------------------------------

    def clean_sentence(self, sentence):

        sentence = re.sub(r"\[[0-9,\s]+\]", "", sentence)
        sentence = re.sub(r"\([0-9,\s]+\)", "", sentence)
        sentence = re.sub(r"\s+", " ", sentence)

        return sentence.strip()

    # --------------------------------------------------------
    # SENTENCE SPLITTING
    # --------------------------------------------------------

    def split_sentences(self, text):

        sentences = re.split(

            r'(?<=[.!?])\s+',

            text

        )

        cleaned = []

        for sentence in sentences:

            sentence = self.clean_sentence(sentence)

            if len(sentence) < 25:
                continue

            if len(sentence) > 500:
                continue

            cleaned.append(sentence)

        return cleaned

    # --------------------------------------------------------
    # SENTENCE SCORE
    # --------------------------------------------------------

    def sentence_score(self, sentence, keywords):

        lower = sentence.lower()

        score = 0

        for keyword in keywords:

            if keyword in lower:

                score += 2

        if any(word in lower for word in [

            "proposed",
            "propose",
            "introduced",
            "developed",
            "designed",
            "implemented",
            "achieved",
            "improved"

        ]):

            score += 3

        if any(char.isdigit() for char in sentence):

            score += 1

        if len(sentence.split()) > 12:

            score += 1

        return score

    # --------------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------------

    def remove_duplicates(self, sentences):

        unique = []
        seen = set()

        for sentence in sentences:

            key = sentence.lower()

            if key not in seen:

                unique.append(sentence)

                seen.add(key)

        return unique

    # --------------------------------------------------------
    # FIND BEST SENTENCES
    # --------------------------------------------------------

    def find_best_sentences(

        self,

        text,

        keywords,

        max_results=5

    ):

        sentences = self.split_sentences(text)

        scored = []

        for sentence in sentences:

            score = self.sentence_score(

                sentence,

                keywords

            )

            if score > 0:

                scored.append(

                    (

                        score,

                        sentence

                    )

                )

        scored.sort(

            key=lambda x: x[0],

            reverse=True

        )

        results = []

        for score, sentence in scored:

            results.append(sentence)

            if len(results) >= max_results:

                break

        return self.remove_duplicates(results)

    # --------------------------------------------------------
    # DOMAIN DETECTION
    # --------------------------------------------------------

    def detect_domain(self, text):

        text = text.lower()

        scores = Counter()

        for domain, keywords in self.domain_keywords.items():

            for keyword in keywords:

                if keyword in text:

                    scores[domain] += 1

        if len(scores) == 0:

            return [

                "General Computer Science"

            ]

        return [

            domain

            for domain, _ in

            scores.most_common(3)

        ]
        # --------------------------------------------------------
    # RESEARCH GAP
    # --------------------------------------------------------

    def detect_research_gap(self, text):

        keywords = [

            "however",
            "existing",
            "traditional",
            "limited",
            "lack",
            "challenge",
            "problem",
            "fails",
            "insufficient"

        ]

        return self.find_best_sentences(

            text,

            keywords,

            max_results=3

        )

    # --------------------------------------------------------
    # NOVEL CONTRIBUTIONS
    # --------------------------------------------------------

    def detect_contributions(self, text):

        keywords = [

            "proposed",
            "we propose",
            "our contribution",
            "novel",
            "introduced",
            "developed",
            "designed",
            "implemented",
            "framework"

        ]

        return self.find_best_sentences(

            text,

            keywords,

            max_results=5

        )

    # --------------------------------------------------------
    # STRENGTHS
    # --------------------------------------------------------

    def detect_strengths(self, text):

        keywords = [

            "efficient",
            "robust",
            "improved",
            "better",
            "accurate",
            "fast",
            "real-time",
            "scalable",
            "lightweight"

        ]

        return self.find_best_sentences(

            text,

            keywords,

            max_results=5

        )

    # --------------------------------------------------------
    # LIMITATIONS
    # --------------------------------------------------------

    def detect_limitations(self, text):

        keywords = [

            "limitation",
            "limitations",
            "drawback",
            "future work",
            "constraint",
            "unable",
            "cannot",
            "restricted"

        ]

        return self.find_best_sentences(

            text,

            keywords,

            max_results=5

        )

    # --------------------------------------------------------
    # APPLICATIONS
    # --------------------------------------------------------

    def detect_applications(self, text):

        keywords = [

            "application",
            "used in",
            "can be used",
            "deployment",
            "real-world",
            "industry",
            "healthcare",
            "transportation",
            "education"

        ]

        return self.find_best_sentences(

            text,

            keywords,

            max_results=5

        )

    # --------------------------------------------------------
    # TECHNICAL KEYWORDS
    # --------------------------------------------------------

    def technical_keywords(self, text):

        words = re.findall(

            r"[A-Za-z][A-Za-z0-9\-\+]{3,}",

            text

        )

        stopwords = {

            "this","that","their","there","using","method",
            "methods","paper","results","system","approach",
            "proposed","research","study","analysis"

        }

        counter = Counter()

        for word in words:

            word = word.lower()

            if word not in stopwords:

                counter[word] += 1

        return [

            word.title()

            for word, _ in

            counter.most_common(20)

        ]

    # --------------------------------------------------------
    # ANALYZE PAPER
    # --------------------------------------------------------

    def analyze(self, text):

        analysis = {}

        analysis["domain"] = self.detect_domain(text)

        analysis["problem"] = self.find_best_sentences(

            text,

            self.categories["problem"]

        )

        analysis["research_gap"] = self.detect_research_gap(

            text

        )

        analysis["objective"] = self.find_best_sentences(

            text,

            self.categories["objective"]

        )

        analysis["methodology"] = self.find_best_sentences(

            text,

            self.categories["methodology"]

        )

        analysis["dataset"] = self.find_best_sentences(

            text,

            self.categories["dataset"]

        )

        analysis["algorithm"] = self.find_best_sentences(

            text,

            self.categories["algorithm"]

        )

        analysis["metrics"] = self.find_best_sentences(

            text,

            self.categories["metrics"]

        )

        analysis["results"] = self.find_best_sentences(

            text,

            self.categories["results"]

        )

        analysis["novel_contributions"] = self.detect_contributions(

            text

        )

        analysis["strengths"] = self.detect_strengths(

            text

        )

        analysis["limitations"] = self.detect_limitations(

            text

        )

        analysis["applications"] = self.detect_applications(

            text

        )

        analysis["future_work"] = self.find_best_sentences(

            text,

            self.categories["future_work"]

        )

        analysis["technical_keywords"] = self.technical_keywords(

            text

        )

        return analysis

    # --------------------------------------------------------
    # PRINT ANALYSIS
    # --------------------------------------------------------

    def print_analysis(self, analysis):

        print("\n")

        print("=" * 70)

        print("AI SCIENTIST - RESEARCH ANALYSIS")

        print("=" * 70)

        for field, values in analysis.items():

            print(f"\n{field.upper()}")

            print("-" * 70)

            if not values:

                print("Not Found")
                continue

            if isinstance(values, list):

                for item in values:

                    print("•", item)

            else:

                print(values)