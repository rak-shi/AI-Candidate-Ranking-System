# AI Candidate Ranking System

An AI-powered candidate ranking system that scores and ranks resumes/candidate profiles against a job description using a **hybrid retrieval approach** — combining **BM25 lexical matching**, **Sentence-Transformer semantic embeddings**, and **rule-based scoring signals** (skills, experience, education) — with **explainable AI** output for every ranked candidate.

Built as part of the *India Runs on Data & AI* challenge.

---

## ✨ Features

- **Hybrid Ranking Engine** — blends lexical (BM25) and semantic (Sentence-Transformers) relevance with structured profile signals for a final weighted score.
- **Explainable Results** — every ranked candidate comes with a human-readable explanation: matched skills, experience summary, education summary, and individual sub-scores.
- **JD Parsing** — reads job descriptions directly from `.docx` or plain text files.
- **Cached Embeddings** — candidate embeddings are computed once and cached to disk (`processed/embeddings.pkl`) for fast repeated ranking runs.
- **CSV Output** — final ranked list (rank, candidate ID, name, score, explanation) is exported to `output.csv`.

---

## 🧠 How It Works

For a given job description, each candidate is scored using a weighted combination of:

| Signal | Weight | Description |
|---|---|---|
| Semantic similarity (embeddings) | 0.35 | Cosine similarity between JD and candidate profile embeddings (`all-MiniLM-L6-v2`) |
| BM25 relevance | 0.30 | Classic lexical/keyword relevance score |
| Skill match | 0.25 | Fraction of candidate's listed skills explicitly mentioned in the JD |
| Experience | 0.07 | Normalized years of experience + career-history depth bonus |
| Education | 0.03 | Degree level and institution tier |
| Career bonus | +0.05 | Bonus if candidate has held AI/ML/NLP/Search-related roles |

All sub-scores are normalized (Min-Max scaling) before being combined into a single `score` between 0 and 1.

An `ExplanationGenerator` then converts the raw scores and matched signals into a readable explanation string, e.g.:
---

## 📁 Project Structure
AI-Candidate-Ranking-System/

├── main.py                      # Entry point — loads data, runs ranking, writes output.csv

├── check_dataset.py             # Quick utility to inspect a sample candidate record

├── requirements.txt

├── data/

   ├── candidates.jsonl         # Candidate profiles (JSON Lines)

│   └── job_description.docx     # Job description to rank candidates against

├── ranking/

│   ├── bm25_ranker.py           # BM25 lexical ranking

│   ├── embedding_ranker.py      # Sentence-Transformer semantic similarity ranking

│   ├── hybrid_ranker.py         # Combines BM25 + embeddings + rule-based signals

│   └── explanation.py           # Generates human-readable explanations for each rank

├── utils/

│   ├── loader.py                # Loads candidate JSONL data

│   ├── preprocess.py            # Text cleaning utilities

│   ├── create_embeddings.py     # Standalone script to (re)generate candidate embeddings

│   └── logger.py                # Logging configuration

├── processed/

│   └── embeddings.pkl           # Cached candidate embeddings (auto-generated)

└── output.csv                   # Final ranked candidates with explanations
<img width="227" height="386" alt="image" src="https://github.com/user-attachments/assets/152780ed-5760-43a7-a48f-e6429f7f8233" />
