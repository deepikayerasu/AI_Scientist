import re


class SectionDetector:
    """
    AI Scientist

    Robust Research Paper Section Detector

    Supports:

    ✓ IEEE Papers
    ✓ Springer Papers
    ✓ ACM Papers
    ✓ Elsevier Papers
    ✓ Numbered headings
    ✓ Roman headings
    ✓ Uppercase headings
    """

    def __init__(self, text):

        self.text = text

        self.lines = [

            line.strip()

            for line in text.splitlines()

            if line.strip()

        ]

        self.clean_text = "\n".join(

            self.lines

        )

        self.sections = {}

    # ---------------------------------------------------------
    # HEADING NORMALIZATION
    # ---------------------------------------------------------

    def normalize_heading(self, heading):

        heading = heading.upper()

        heading = re.sub(

            r"^[IVXLCDM0-9.\-\s]+",

            "",

            heading

        )

        heading = heading.strip()

        return heading

    # ---------------------------------------------------------
    # HEADING MATCHER
    # ---------------------------------------------------------

    def is_heading(self, line):

        line = line.strip()

        if len(line) < 3:

            return False

        if len(line) > 80:

            return False

        patterns = [

            r"^[IVXLCDM]+\.",

            r"^[0-9]+\.",

            r"^[0-9]+\s",

            r"^[A-Z][A-Z\s\-]{3,}$"

        ]

        for pattern in patterns:

            if re.match(

                pattern,

                line

            ):

                return True

        return False

    # ---------------------------------------------------------
    # FIND ALL HEADINGS
    # ---------------------------------------------------------

    def detect_headings(self):

        headings = []

        for i, line in enumerate(self.lines):

            if self.is_heading(line):

                normalized = self.normalize_heading(

                    line

                )

                headings.append(

                    (

                        i,

                        normalized,

                        line

                    )

                )

        return headings

    # ---------------------------------------------------------
    # STANDARD SECTION MAP
    # ---------------------------------------------------------

    SECTION_MAP = {

        "ABSTRACT":[

            "ABSTRACT"

        ],

        "INTRODUCTION":[

            "INTRODUCTION",

            "BACKGROUND"

        ],

        "RELATED WORK":[

            "RELATED WORK",

            "LITERATURE REVIEW",

            "PREVIOUS WORK"

        ],

        "METHODOLOGY":[

            "METHODOLOGY",

            "METHOD",

            "METHODS",

            "PROPOSED METHOD",

            "PROPOSED SYSTEM",

            "SYSTEM DESIGN"

        ],

        "ARCHITECTURE":[

            "ARCHITECTURE",

            "SYSTEM ARCHITECTURE"

        ],

        "IMPLEMENTATION":[

            "IMPLEMENTATION"

        ],

        "EXPERIMENTS":[

            "EXPERIMENT",

            "EXPERIMENTAL SETUP",

            "EXPERIMENTS"

        ],

        "RESULTS":[

            "RESULT",

            "RESULTS",

            "RESULTS AND DISCUSSION",

            "DISCUSSION"

        ],

        "CONCLUSION":[

            "CONCLUSION",

            "CONCLUSIONS"

        ],

        "FUTURE WORK":[

            "FUTURE WORK"

        ],

        "REFERENCES":[

            "REFERENCES",

            "BIBLIOGRAPHY"

        ]

    }
        # ---------------------------------------------------------
    # FIND STANDARD SECTION NAME
    # ---------------------------------------------------------

    def identify_section(self, heading):

        heading = heading.upper()

        for standard_name, aliases in self.SECTION_MAP.items():

            for alias in aliases:

                if alias in heading:

                    return standard_name

        return None

    # ---------------------------------------------------------
    # EXTRACT SECTIONS
    # ---------------------------------------------------------

    def extract_sections(self):

        headings = self.detect_headings()

        extracted = {}

        if len(headings) == 0:

            return extracted

        for i in range(len(headings)):

            start_index = headings[i][0]

            heading = headings[i][1]

            section_name = self.identify_section(

                heading

            )

            if section_name is None:

                continue

            if i == len(headings) - 1:

                end_index = len(self.lines)

            else:

                end_index = headings[i + 1][0]

            content = "\n".join(

                self.lines[

                    start_index + 1:end_index

                ]

            )

            content = self.clean_section(

                content

            )

            extracted[section_name] = content

        return extracted

    # ---------------------------------------------------------
    # CLEAN SECTION
    # ---------------------------------------------------------

    def clean_section(self, text):

        text = re.sub(

            r"\[[0-9]+\]",

            "",

            text

        )

        text = re.sub(

            r"\([0-9]+\)",

            "",

            text

        )

        text = re.sub(

            r"\s+",

            " ",

            text

        )

        text = text.strip()

        return text

    # ---------------------------------------------------------
    # FALLBACK ABSTRACT
    # ---------------------------------------------------------

    def extract_abstract(self):

        lower = self.clean_text.lower()

        start = lower.find(

            "abstract"

        )

        if start == -1:

            return ""

        end = lower.find(

            "introduction",

            start

        )

        if end == -1:

            end = start + 2500

        return self.clean_section(

            self.clean_text[

                start:end

            ]

        )

    # ---------------------------------------------------------
    # FALLBACK INTRODUCTION
    # ---------------------------------------------------------

    def extract_introduction(self):

        lower = self.clean_text.lower()

        start = lower.find(

            "introduction"

        )

        if start == -1:

            return ""

        end = lower.find(

            "related work",

            start

        )

        if end == -1:

            end = lower.find(

                "literature review",

                start

            )

        if end == -1:

            end = start + 5000

        return self.clean_section(

            self.clean_text[

                start:end

            ]

        )

    # ---------------------------------------------------------
    # FALLBACK CONCLUSION
    # ---------------------------------------------------------

    def extract_conclusion(self):

        lower = self.clean_text.lower()

        start = lower.rfind(

            "conclusion"

        )

        if start == -1:

            return ""

        end = lower.find(

            "references",

            start

        )

        if end == -1:

            end = len(self.clean_text)

        return self.clean_section(

            self.clean_text[

                start:end

            ]

        )
        # ---------------------------------------------------------
    # FALLBACK METHODOLOGY
    # ---------------------------------------------------------

    def extract_methodology(self):

        keywords = [

            "methodology",

            "method",

            "methods",

            "proposed method",

            "proposed system",

            "system design",

            "implementation"

        ]

        lower = self.clean_text.lower()

        for key in keywords:

            start = lower.find(key)

            if start != -1:

                end = start + 5000

                return self.clean_section(

                    self.clean_text[start:end]

                )

        return ""

    # ---------------------------------------------------------
    # FALLBACK RESULTS
    # ---------------------------------------------------------

    def extract_results(self):

        keywords = [

            "results",

            "results and discussion",

            "discussion",

            "experimental results",

            "performance evaluation"

        ]

        lower = self.clean_text.lower()

        for key in keywords:

            start = lower.find(key)

            if start != -1:

                end = start + 5000

                return self.clean_section(

                    self.clean_text[start:end]

                )

        return ""

    # ---------------------------------------------------------
    # FALLBACK REFERENCES
    # ---------------------------------------------------------

    def extract_references(self):

        lower = self.clean_text.lower()

        start = lower.rfind("references")

        if start == -1:

            start = lower.rfind("bibliography")

        if start == -1:

            return ""

        return self.clean_section(

            self.clean_text[start:]

        )

    # ---------------------------------------------------------
    # FUTURE WORK
    # ---------------------------------------------------------

    def extract_future_work(self):

        keywords = [

            "future work",

            "future scope",

            "scope for future work"

        ]

        lower = self.clean_text.lower()

        for key in keywords:

            start = lower.find(key)

            if start != -1:

                end = start + 3000

                return self.clean_section(

                    self.clean_text[start:end]

                )

        return ""

    # ---------------------------------------------------------
    # FINAL OUTPUT
    # ---------------------------------------------------------

    def extract(self):

        detected = self.extract_sections()

        final_sections = {

            "abstract":

                detected.get(

                    "ABSTRACT",

                    self.extract_abstract()

                ),

            "introduction":

                detected.get(

                    "INTRODUCTION",

                    self.extract_introduction()

                ),

            "literature_review":

                detected.get(

                    "RELATED WORK",

                    ""

                ),

            "methodology":

                detected.get(

                    "METHODOLOGY",

                    self.extract_methodology()

                ),

            "architecture":

                detected.get(

                    "ARCHITECTURE",

                    ""

                ),

            "implementation":

                detected.get(

                    "IMPLEMENTATION",

                    ""

                ),

            "experimental_setup":

                detected.get(

                    "EXPERIMENTS",

                    ""

                ),

            "results":

                detected.get(

                    "RESULTS",

                    self.extract_results()

                ),

            "discussion":

                detected.get(

                    "RESULTS",

                    self.extract_results()

                ),

            "conclusion":

                detected.get(

                    "CONCLUSION",

                    self.extract_conclusion()

                ),

            "future_work":

                detected.get(

                    "FUTURE WORK",

                    self.extract_future_work()

                ),

            "references":

                detected.get(

                    "REFERENCES",

                    self.extract_references()

                )

        }

        return final_sections
    