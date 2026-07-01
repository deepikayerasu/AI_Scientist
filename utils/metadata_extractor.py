import re
from collections import Counter


class MetadataExtractor:
    """
    AI Scientist Metadata Extractor

    Features
    --------
    ✓ Better title detection
    ✓ Better author detection
    ✓ PDF metadata support
    ✓ Email extraction
    ✓ Affiliation detection
    ✓ Domain classification
    ✓ DOI detection
    ✓ Keyword extraction
    """

    PUBLISHERS = [

        "IEEE",
        "Springer",
        "Elsevier",
        "ACM",
        "Nature",
        "Wiley",
        "MDPI",
        "ScienceDirect",
        "Taylor & Francis"

    ]

    DOMAIN_KEYWORDS = {

        "Artificial Intelligence": [

            "artificial intelligence",
            "machine learning",
            "deep learning",
            "neural network",
            "transformer",
            "llm",
            "large language model"

        ],

        "Computer Vision": [

            "computer vision",
            "image",
            "cnn",
            "object detection",
            "segmentation"

        ],

        "Natural Language Processing": [

            "nlp",
            "bert",
            "text classification",
            "language model"

        ],

        "Networking": [

            "network",
            "routing",
            "mesh",
            "wifi",
            "wireless",
            "packet",
            "ble"

        ],

        "IoT": [

            "iot",
            "sensor",
            "embedded",
            "internet of things"

        ],

        "Cyber Security": [

            "malware",
            "cyber",
            "security",
            "intrusion",
            "attack"

        ],

        "Cloud Computing": [

            "cloud",
            "container",
            "virtualization",
            "kubernetes"

        ]

    }

    # ---------------------------------------------------------

    def __init__(

        self,

        text,

        metadata=None

    ):

        self.text = text

        self.metadata = metadata if metadata else {}

        self.lines = [

            line.strip()

            for line in text.splitlines()

            if line.strip()

        ]

        self.first_page = "\n".join(

            self.lines[:80]

        )

    # ---------------------------------------------------------
    # CLEAN TEXT
    # ---------------------------------------------------------

    def clean_text(

        self,

        text

    ):

        text = re.sub(

            r"\s+",

            " ",

            text

        )

        return text.strip()

    # ---------------------------------------------------------
    # TITLE
    # ---------------------------------------------------------

    def extract_title(self):

        pdf_title = (

            self.metadata.get("title")

            or ""

        ).strip()

        if len(pdf_title) > 15:

            return pdf_title

        candidates = []

        for line in self.lines[:20]:

            line = line.strip()

            if len(line) < 15:

                continue

            if len(line) > 180:

                continue

            lower = line.lower()

            if any(

                x in lower

                for x in [

                    "abstract",

                    "keywords",

                    "index terms",

                    "doi",

                    "copyright"

                ]

            ):

                continue

            score = 0

            if len(line.split()) >= 5:

                score += 2

            if line == line.title():

                score += 1

            if not line.endswith("."):

                score += 1

            if ":" not in line:

                score += 1

            candidates.append(

                (

                    score,

                    line

                )

            )

        if candidates:

            candidates.sort(

                reverse=True

            )

            return candidates[0][1]

        return "Not Found"

    # ---------------------------------------------------------
    # AUTHORS
    # ---------------------------------------------------------

    def extract_authors(self):

        authors = []

        pattern = re.compile(

            r"\b([A-Z][a-z]+(?:\s+[A-Z]\.)?(?:\s+[A-Z][a-z]+){1,3})\b"

        )

        for line in self.lines[:30]:

            if len(line) > 120:

                continue

            lower = line.lower()

            if any(

                x in lower

                for x in [

                    "department",

                    "university",

                    "college",

                    "abstract",

                    "keywords"

                ]

            ):

                continue

            matches = pattern.findall(

                line

            )

            for match in matches:

                if match not in authors:

                    authors.append(

                        match

                    )

        if not authors:

            pdf_author = self.metadata.get(

                "author"

            )

            if pdf_author:

                authors.append(

                    pdf_author

                )

        return authors
        # ---------------------------------------------------------
    # EMAILS
    # ---------------------------------------------------------

    def extract_emails(self):

        pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

        emails = re.findall(

            pattern,

            self.text

        )

        return sorted(

            list(

                set(emails)

            )

        )

    # ---------------------------------------------------------
    # AFFILIATIONS
    # ---------------------------------------------------------

    def extract_affiliations(self):

        affiliations = []

        keywords = [

            "university",
            "college",
            "department",
            "school",
            "faculty",
            "laboratory",
            "lab",
            "research center",
            "research centre",
            "institute",
            "academy"

        ]

        for line in self.lines[:50]:

            lower = line.lower()

            if any(

                key in lower

                for key in keywords

            ):

                line = self.clean_text(line)

                if line not in affiliations:

                    affiliations.append(

                        line

                    )

        return affiliations

    # ---------------------------------------------------------
    # DOI
    # ---------------------------------------------------------

    def extract_doi(self):

        pattern = r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+"

        match = re.search(

            pattern,

            self.text

        )

        if match:

            return match.group(0)

        return None

    # ---------------------------------------------------------
    # ABSTRACT
    # ---------------------------------------------------------

    def extract_abstract(self):

        text = self.text

        patterns = [

            r"Abstract\s*(.*?)(?:Keywords|Index Terms|1\.\s*Introduction|I\.\s*Introduction)",

            r"ABSTRACT\s*(.*?)(?:KEYWORDS|INDEX TERMS|1\.\s*INTRODUCTION|I\.\s*INTRODUCTION)"

        ]

        for pattern in patterns:

            match = re.search(

                pattern,

                text,

                re.DOTALL

            )

            if match:

                abstract = self.clean_text(

                    match.group(1)

                )

                if len(abstract) > 80:

                    return abstract

        lower = text.lower()

        start = lower.find(

            "abstract"

        )

        if start != -1:

            end = start + 2500

            return self.clean_text(

                text[start:end]

            )

        return "Not Found"

    # ---------------------------------------------------------
    # KEYWORDS
    # ---------------------------------------------------------

    def extract_keywords(self):

        patterns = [

            r"Keywords\s*[:-]?\s*(.*)",

            r"KEYWORDS\s*[:-]?\s*(.*)",

            r"Index Terms\s*[:-]?\s*(.*)",

            r"INDEX TERMS\s*[:-]?\s*(.*)"

        ]

        for pattern in patterns:

            match = re.search(

                pattern,

                self.text

            )

            if match:

                raw = match.group(1)

                raw = raw.split("\n")[0]

                keywords = [

                    self.clean_text(x)

                    for x in

                    re.split(

                        r",|;",

                        raw

                    )

                    if x.strip()

                ]

                return keywords

        return []

    # ---------------------------------------------------------
    # YEAR
    # ---------------------------------------------------------

    def extract_year(self):

        years = re.findall(

            r"\b(19\d{2}|20\d{2})\b",

            self.first_page

        )

        if years:

            return max(years)

        return None

    # ---------------------------------------------------------
    # PUBLISHER
    # ---------------------------------------------------------

    def extract_publisher(self):

        lower = self.first_page.lower()

        for publisher in self.PUBLISHERS:

            if publisher.lower() in lower:

                return publisher

        return None

    # ---------------------------------------------------------
    # PUBLICATION
    # ---------------------------------------------------------

    def extract_publication(self):

        publication_keywords = [

            "journal",

            "conference",

            "transactions",

            "symposium",

            "proceedings",

            "workshop"

        ]

        for line in self.lines[:60]:

            lower = line.lower()

            if any(

                key in lower

                for key in publication_keywords

            ):

                return self.clean_text(

                    line

                )

        return None
        # ---------------------------------------------------------
    # DOMAIN CLASSIFICATION
    # ---------------------------------------------------------

    def classify_domain(self):

        text = self.text[:20000].lower()

        scores = Counter()

        for domain, keywords in self.DOMAIN_KEYWORDS.items():

            for keyword in keywords:

                if keyword.lower() in text:

                    scores[domain] += 1

        if len(scores) == 0:

            return ["General Computer Science"]

        return [

            domain

            for domain, _ in

            scores.most_common(3)

        ]

    # ---------------------------------------------------------
    # FALLBACK KEYWORDS
    # ---------------------------------------------------------

    def fallback_keywords(self):

        stopwords = {

            "the","is","are","was","were","be","been",

            "of","for","to","in","on","with","and",

            "or","using","use","used","this","that",

            "these","those","paper","proposed","method",

            "results","approach","model","system"

        }

        words = re.findall(

            r"[A-Za-z]{4,}",

            self.text[:12000]

        )

        freq = Counter()

        for word in words:

            word = word.lower()

            if word not in stopwords:

                freq[word] += 1

        keywords = []

        for word, _ in freq.most_common(15):

            keywords.append(

                word.title()

            )

        return keywords

    # ---------------------------------------------------------
    # CONFIDENCE SCORE
    # ---------------------------------------------------------

    def confidence_score(self):

        score = 0

        if self.extract_title() != "Not Found":

            score += 15

        if self.extract_authors():

            score += 15

        if self.extract_abstract() != "Not Found":

            score += 20

        if self.extract_keywords():

            score += 10

        if self.extract_doi():

            score += 10

        if self.extract_year():

            score += 10

        if self.extract_publisher():

            score += 10

        if self.extract_publication():

            score += 10

        return min(score,100)

    # ---------------------------------------------------------
    # FINAL OUTPUT
    # ---------------------------------------------------------

    def extract(self):

        keywords = self.extract_keywords()

        if len(keywords) == 0:

            keywords = self.fallback_keywords()

        result = {

            "title": self.extract_title(),

            "authors": self.extract_authors(),

            "emails": self.extract_emails(),

            "affiliations": self.extract_affiliations(),

            "abstract": self.extract_abstract(),

            "keywords": keywords,

            "doi": self.extract_doi(),

            "year": self.extract_year(),

            "publisher": self.extract_publisher(),

            "publication": self.extract_publication(),

            "domain": self.classify_domain(),

            "confidence": self.confidence_score()

        }

        return result