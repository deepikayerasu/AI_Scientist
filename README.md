# 🧠 AI Scientist

> AI-powered Research Paper Analysis using Retrieval-Augmented Generation (RAG), FAISS, Ollama (Qwen 2.5), and Streamlit.

---

## 📌 Overview

AI Scientist is an intelligent research paper assistant that helps researchers and students understand scientific papers through semantic search and local Large Language Models (LLMs).

Instead of manually reading lengthy papers, users can upload a PDF and interact with it through natural language questions.

The system extracts metadata, summarizes the paper, performs semantic retrieval using FAISS, and generates contextual answers using the Qwen 2.5 model running locally with Ollama.

---

# 🚀 Features

- 📄 Upload research papers (PDF)
- 🧠 Metadata extraction
- 📑 Automatic summarization
- 🔍 Semantic chunk generation
- 📚 FAISS Vector Search
- 🤖 Chat with research papers
- 📊 Research analysis
- 📂 Section detection
- ⚡ Local LLM (Qwen 2.5 + Ollama)
- 💻 Streamlit Interface

---

# 🏗️ System Architecture

```
                PDF Research Paper
                       │
                       ▼
              PDF Text Extraction
                       │
                       ▼
              Metadata Extraction
                       │
                       ▼
              Section Detection
                       │
                       ▼
               Semantic Chunking
                       │
                       ▼
        Sentence Transformer Embeddings
                       │
                       ▼
                  FAISS Index
                       │
                       ▼
                 Relevant Chunks
                       │
                       ▼
               Qwen 2.5 (Ollama)
                       │
                       ▼
                  AI Response
```

---

# 🛠️ Tech Stack

| Technology | Purpose |
|------------|----------|
| Python | Backend |
| Streamlit | User Interface |
| Ollama | Local LLM Runtime |
| Qwen 2.5 | Large Language Model |
| FAISS | Vector Database |
| Sentence Transformers | Embeddings |
| PyMuPDF | PDF Parsing |
| Transformers | Summarization |

---

# 📂 Project Structure

```
AI_Scientist/

│── app.py
│── requirements.txt
│── README.md
│── .gitignore

├── utils
│   ├── analyzer.py
│   ├── chat_engine.py
│   ├── chunker.py
│   ├── config.py
│   ├── embeddings.py
│   ├── keyword_extractor.py
│   ├── llm_engine.py
│   ├── metadata_extractor.py
│   ├── pdf_parser.py
│   ├── report_generator.py
│   ├── section_detector.py
│   ├── summarizer.py
│   └── vector_store.py

├── assets
├── data
├── models
├── reports
└── temp
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/deepikayerasu/AI_Scientist.git

cd AI_Scientist
```

Install dependencies

```bash
pip install -r requirements.txt
```

Install Ollama

```bash
https://ollama.com
```

Download Qwen

```bash
ollama pull qwen2.5:7b
```

Run

```bash
streamlit run app.py
```

---

# 💬 Example Questions

- What problem does this paper solve?
- What methodology is proposed?
- Which dataset is used?
- What are the main contributions?
- What are the limitations?
- Explain this paper in simple words.
- Compare methodology and results.
- Summarize the entire paper.

---

# 📈 Future Improvements

- Multi-paper comparison
- Research gap detection
- Knowledge Graph
- Citation-aware RAG
- Literature Survey Generator
- Research Proposal Generator

---

# 👨‍💻 Author

**Deepika Yerasu**

AI & Machine Learning Student
