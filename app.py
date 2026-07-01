import os
import streamlit as st

from utils.config import (
    APP_TITLE,
    PAGE_ICON,
    LAYOUT,
    PAPERS_DIR,
    MAX_PREVIEW_CHARACTERS
)

from utils.pdf_parser import PDFParser
from utils.metadata_extractor import MetadataExtractor
from utils.section_detector import SectionDetector
from utils.chunker import PaperChunker
from utils.embeddings import EmbeddingGenerator
from utils.vector_store import VectorStore
from utils.summarizer import PaperSummarizer
from utils.analyzer import ResearchAnalyzer
from utils.chat_engine import ChatEngine


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT
)


# ==========================================================
# SESSION STATE
# ==========================================================

default_state = {

    "paper": None,

    "metadata": None,

    "sections": None,

    "chunks": None,

    "embeddings": None,

    "vector_store": None,

    "summary": None,

    "analysis": None,

    "chat_engine": None

}

for key in default_state:

    if key not in st.session_state:

        st.session_state[key] = default_state[key]


# ==========================================================
# LOAD AI MODELS (LOAD ONLY ONCE)
# ==========================================================

@st.cache_resource
def load_embedding_model():

    return EmbeddingGenerator()


@st.cache_resource
def load_summarizer():

    return PaperSummarizer()


embedding_model = load_embedding_model()

summarizer = load_summarizer()


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("📚 AI Scientist")

    st.markdown("---")

    st.subheader("Modules")

    st.success("PDF Parser")

    st.success("Metadata Extractor")

    st.success("Section Detector")

    st.success("Chunk Generator")

    st.success("Sentence Embeddings")

    st.success("FAISS Search")

    st.success("AI Summarizer")

    st.success("Research Analyzer")

    st.success("Chat Engine")

    st.markdown("---")

    st.info("Version 3.0")


# ==========================================================
# HEADER
# ==========================================================

st.title("📚 AI Scientist")

st.caption(
    "AI Powered Research Paper Understanding Engine"
)

st.markdown("---")


# ==========================================================
# FILE UPLOADER
# ==========================================================

uploaded_file = st.file_uploader(

    "Upload Research Paper",

    type=["pdf"]

)

if uploaded_file:

    save_path = os.path.join(

        PAPERS_DIR,

        uploaded_file.name

    )

    with open(save_path, "wb") as f:

        f.write(uploaded_file.getbuffer())

    with st.spinner("Analyzing Research Paper..."):

        parser = PDFParser(save_path)

        paper = parser.extract()

        metadata = MetadataExtractor(

            paper["text"],

            paper["metadata"]

        ).extract()

        detector = SectionDetector(

            paper["text"]

        )

        sections = detector.extract()

        chunker = PaperChunker()

        chunk_result = chunker.process(

            paper["text"]

        )

        chunks = chunk_result["chunks"]

        embedding_result = embedding_model.process(

            chunks

        )

        vector_store = VectorStore()

        vector_store.build(

            chunks,

            embedding_result["embeddings"]

        )

        summary = summarizer.process(

            chunks,

            paper["text"]

        )

        analyzer = ResearchAnalyzer()

        analysis = analyzer.analyze(

            paper["text"]

        )

        chat_engine = ChatEngine(

            vector_store,

            embedding_model

        )

        st.session_state.paper = paper

        st.session_state.metadata = metadata

        st.session_state.sections = sections

        st.session_state.chunks = chunks

        st.session_state.embeddings = embedding_result

        st.session_state.vector_store = vector_store

        st.session_state.summary = summary

        st.session_state.analysis = analysis

        st.session_state.chat_engine = chat_engine

    st.success("Research Paper Processed Successfully.")


# ==========================================================
# LOAD DATA
# ==========================================================

if st.session_state.paper is not None:

    paper = st.session_state.paper

    metadata = st.session_state.metadata

    sections = st.session_state.sections

    summary = st.session_state.summary

    analysis = st.session_state.analysis

    chat_engine = st.session_state.chat_engine

    st.markdown("---")

    st.header("📊 Paper Statistics")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(

            "Pages",

            paper["pages"]

        )

    with c2:

        st.metric(

            "Words",

            paper["words"]

        )

    with c3:

        st.metric(

            "Characters",

            paper["characters"]

        )

    with c4:

        st.metric(

            "Reading Time",

            f"{paper['reading_time']} min"

        )
    # ==========================================================
    # METADATA
    # ==========================================================

        # ==========================================================
    # METADATA
    # ==========================================================

    st.markdown("---")
    st.header("🧠 Paper Metadata")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📄 Title")
        st.write(metadata.get("title", "Not Found"))

        st.subheader("👨‍💻 Authors")

        authors = metadata.get("authors", [])

        if authors:

            for author in authors:

                st.write("•", author)

        else:

            st.info("Not Found")

        st.subheader("🏢 Publisher")
        st.write(metadata.get("publisher", "Not Found"))

        st.subheader("📚 Publication")
        st.write(metadata.get("publication", "Not Found"))

        st.subheader("📅 Year")
        st.write(metadata.get("year", "Not Found"))

    with col2:

        st.subheader("🌍 Research Domain")

        domains = metadata.get("domain", [])

        if domains:

            for d in domains:

                st.write("•", d)

        else:

            st.info("Not Found")

        st.subheader("🏛 Affiliations")

        affiliations = metadata.get("affiliations", [])

        if affiliations:

            for a in affiliations:

                st.write("•", a)

        else:

            st.info("Not Found")

        st.subheader("📧 Emails")

        emails = metadata.get("emails", [])

        if emails:

            for e in emails:

                st.write(e)

        else:

            st.info("Not Found")

    st.subheader("📑 Keywords")

    keywords = metadata.get("keywords", [])

    if keywords:

        st.write(", ".join(keywords))

    else:

        st.info("Not Found")

    st.subheader("📄 Abstract")

    st.text_area(

        "Abstract",

        metadata.get("abstract", ""),

        height=220

    )

    # ==========================================================
    # DETECTED SECTIONS
    # ==========================================================

    st.markdown("---")

    st.header("📑 Detected Sections")

    section_titles = {

        "abstract": "Abstract",

        "introduction": "Introduction",

        "literature_review": "Literature Review",

        "methodology": "Methodology",

        "architecture": "Architecture",

        "algorithm": "Algorithm",

        "experimental_setup": "Experimental Setup",

        "results": "Results",

        "discussion": "Discussion",

        "conclusion": "Conclusion",

        "future_work": "Future Work",

        "references": "References"

    }

    for key, title in section_titles.items():

        with st.expander(title):

            content = sections.get(key, "")

            if content.strip():

                st.write(content)

            else:

                st.info("Section not detected.")

    # ==========================================================
    # PDF PREVIEW
    # ==========================================================

    st.markdown("---")

    st.header("📖 PDF Preview")

    st.text_area(

        "Extracted Text",

        paper["text"][:MAX_PREVIEW_CHARACTERS],

        height=450

    )

    # ==========================================================
    # PAGE VIEWER
    # ==========================================================

    st.markdown("---")

    st.header("📄 Individual Page Viewer")

    page_numbers = [

        page["page_number"]

        for page in paper["page_data"]

    ]

    selected_page = st.selectbox(

        "Choose Page",

        page_numbers

    )

    for page in paper["page_data"]:

        if page["page_number"] == selected_page:

            st.text_area(

                f"Page {selected_page}",

                page["text"],

                height=350

            )

            break

    # ==========================================================
    # AI SUMMARY
    # ==========================================================

    st.markdown("---")

    st.header("📝 AI Summary")

    st.subheader("Executive Summary")

    st.write(

        summary["summary"]

    )

    st.subheader("Key Contributions")

    if summary["key_contributions"]:

        for item in summary["key_contributions"]:

            st.write("•", item)

    else:

        st.info("No contributions detected.")
            # ==========================================================
    # RESEARCH ANALYSIS
    # ==========================================================

        # ==========================================================
    # RESEARCH ANALYSIS
    # ==========================================================

    st.markdown("---")
    st.header("🔬 AI Research Analysis")

    # -----------------------------
    # Research Domain
    # -----------------------------

    domains = analysis.get("domain", [])

    if domains:

        st.subheader("🌍 Research Domain")

        cols = st.columns(min(len(domains), 3))

        for i, domain in enumerate(domains):

            cols[i % len(cols)].success(domain)

    # -----------------------------
    # Analysis Sections
    # -----------------------------

    analysis_titles = {

        "problem": "🎯 Research Problem",

        "research_gap": "📉 Research Gap",

        "objective": "🎯 Research Objective",

        "methodology": "⚙️ Methodology",

        "dataset": "🗂 Dataset",

        "algorithm": "🤖 Algorithms / Models",

        "metrics": "📊 Evaluation Metrics",

        "results": "📈 Results",

        "novel_contributions": "💡 Novel Contributions",

        "strengths": "✅ Strengths",

        "limitations": "⚠️ Limitations",

        "applications": "🏭 Applications",

        "future_work": "🚀 Future Work",

        "technical_keywords": "🏷 Technical Keywords"

    }

    for key, title in analysis_titles.items():

        with st.expander(title, expanded=False):

            values = analysis.get(key, [])

            if values:

                if isinstance(values, list):

                    for item in values:

                        st.write("•", item)

                else:

                    st.write(values)

            else:

                st.info("Not detected.")

    # ==========================================================
    # CHUNK INFORMATION
    # ==========================================================

    st.markdown("---")

    st.header("📊 Chunk Information")

    st.metric(

        "Total Chunks",

        len(st.session_state.chunks)

    )

    with st.expander("View Generated Chunks"):

        for i, chunk in enumerate(

            st.session_state.chunks,

            start=1

        ):

            st.markdown(f"### Chunk {i}")

            st.write(chunk)

            st.markdown("---")

    # ==========================================================
    # CHAT WITH PAPER
    # ==========================================================

    # ==========================================================
    # CHAT WITH RESEARCH PAPER (QWEN POWERED)
    # ==========================================================

    st.markdown("---")

    st.header("🤖 AI Research Assistant")

    st.caption(
        "Ask questions about the uploaded research paper."
    )

    question = st.text_input(
        "Ask your question",
        placeholder="Example: What is the main contribution of this paper?"
    )

    col1, col2 = st.columns([1, 5])

    with col1:

        ask = st.button(
            "🚀 Ask",
            use_container_width=True
        )

    with col2:

        st.empty()

    if ask:

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Qwen is analyzing the research paper..."
            ):

                response = chat_engine.ask(question)

            st.success("Answer Generated")

            # --------------------------------------------------
            # AI ANSWER
            # --------------------------------------------------

            st.subheader("🤖 AI Answer")

            st.markdown(
                response["answer"]
            )

            # --------------------------------------------------
            # QUESTION TYPE
            # --------------------------------------------------

            st.subheader("📌 Question Type")

            st.info(
                response["question_type"]
                .replace("_", " ")
                .title()
            )

            # --------------------------------------------------
            # CONFIDENCE
            # --------------------------------------------------

            st.subheader("📊 Confidence")

            confidence = response["confidence"]

            st.progress(confidence / 100)

            st.write(
                f"Confidence Score : {confidence}%"
            )

            # --------------------------------------------------
            # CONTEXT
            # --------------------------------------------------

            with st.expander(
                "📄 Context Used By AI"
            ):

                st.write(
                    response["context"]
                )

            # --------------------------------------------------
            # SOURCE CHUNKS
            # --------------------------------------------------

            with st.expander(
                "📚 Retrieved Source Chunks"
            ):

                for i, result in enumerate(
                    response["results"],
                    start=1
                ):

                    st.markdown(
                        f"### Chunk {i}"
                    )

                    st.caption(
                        f"Similarity Score : {result['score']:.4f}"
                    )

                    st.write(
                        result["chunk"]
                    )

                    st.markdown("---")

    # ==========================================================
    # VECTOR STORE INFORMATION
    # ==========================================================

    st.markdown("---")

    st.header("🧠 Embedding Information")

    vector_stats = st.session_state.vector_store.statistics()

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            "Embedding Dimension",

            vector_stats["dimension"]

        )

    with c2:

        st.metric(

            "Vectors",

            vector_stats["vectors"]

        )

    with c3:

        st.metric(

            "Stored Chunks",

            vector_stats["chunks"]

        )

    # ==========================================================
    # PROJECT STATUS
    # ==========================================================

    st.markdown("---")

    st.header("🚀 AI Scientist Pipeline")

    st.success("✅ PDF Parsing")

    st.success("✅ Metadata Extraction")

    st.success("✅ Section Detection")

    st.success("✅ Smart Chunking")

    st.success("✅ Sentence Embeddings")

    st.success("✅ FAISS Semantic Search")

    st.success("✅ AI Summarization")

    st.success("✅ Research Analysis")

    st.success("✅ Chat With Paper")

    st.info("📄 Report Generator (Coming Soon)")

    st.markdown("---")

    st.caption(

        "AI Scientist v3 | Semantic Research Paper Understanding System"

    )

else:

    st.info(

        "👆 Upload a PDF research paper to begin."

    )