
# AI Candidate Ranking System

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![SentenceTransformers](https://img.shields.io/badge/Sentence--Transformers-NLP-green)
![BM25](https://img.shields.io/badge/BM25-Ranking-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

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

```text
AI-Candidate-Ranking-System/
│
├── main.py                    # Entry point - loads data, ranks candidates, writes output.csv
├── check_dataset.py           # Utility to inspect sample candidate records
├── requirements.txt
├── README.md
├── output.csv
│
├── data/
│   ├── job_description.docx   # Job description
│   └── candidates.jsonl       # Candidate dataset (not uploaded to GitHub)
│
├── ranking/
│   ├── bm25_ranker.py         # BM25 lexical ranking
│   ├── embedding_ranker.py    # Sentence Transformer semantic similarity
│   ├── hybrid_ranker.py       # Hybrid ranking algorithm
│   └── explanation.py         # Explainable ranking
│
├── utils/
│   ├── loader.py              # Dataset loader
│   ├── preprocess.py          # Text preprocessing
│   ├── create_embeddings.py   # Generate candidate embeddings
│   └── logger.py              # Logging utilities
│
└── processed/
    └── embeddings.pkl         # Generated candidate embeddings (not uploaded)
```
---

# 🏗️ System Architecture

The following diagram illustrates the complete workflow of the AI Candidate Ranking System.

<div align="center">

"<img width="1800" height="2000" alt="architecture" src="https://github.com/user-attachments/assets/057378a8-719f-4507-b007-7da94a763814" />


</div>

The system combines **BM25 lexical retrieval**, **Sentence Transformer semantic similarity**, **skill matching**, **experience scoring**, and **education scoring** to generate an explainable hybrid ranking for each candidate.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/rak-shi/AI-Candidate-Ranking-System.git
cd AI-Candidate-Ranking-System
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your data

Place your candidate dataset and job description inside the `data/` folder:

- `data/candidates.jsonl` — one JSON object per line, each representing a candidate profile (skills, career history, education, etc.)
- `data/job_description.docx` — the job description to rank candidates against (`.docx` or plain text supported)

### 4. Run the ranking pipeline

```bash
python main.py
```

On first run, this will:
1. Load all candidates and the job description.
2. Generate and cache sentence embeddings for every candidate (`processed/embeddings.pkl`).
3. Run the hybrid ranker (BM25 + embeddings + rule-based signals).
4. Generate explanations for each ranked candidate.
5. Save the top-ranked candidates to `output.csv`.

Subsequent runs reuse the cached embeddings, so re-ranking against a new job description is fast — just delete `processed/embeddings.pkl` if your candidate data changes and needs re-embedding.

### 5. Inspect a sample candidate (optional)

```bash
python check_dataset.py
```

---

## 📦 Output

`output.csv` contains the final ranked candidates:

| rank | candidate_id | name | score | explanation |
|---|---|---|---|---|
| 1 | CAND_0088025 | Amit Arora | 0.7646 | Matched skills: ... \| Worked as ... \| Ph.D from ... \| Semantic similarity score: ... \| BM25 relevance score: ... \| Overall ranking score: ... |

---

## 🛠️ Tech Stack

- **Python**
- [`sentence-transformers`](https://www.sbert.net/) (`all-MiniLM-L6-v2`) — semantic embeddings
- [`rank-bm25`](https://github.com/dorianbrown/rank_bm25) — lexical/keyword relevance
- `scikit-learn` — score normalization & cosine similarity
- `pandas` / `numpy` — data handling and scoring
- `python-docx` — job description parsing
- `tqdm`, `nltk`, `joblib` — supporting utilities

---

## 🔮 Possible Improvements

- Configurable scoring weights via a config file instead of hard-coded constants.
- Support for multiple job descriptions in a single run.
- A simple web UI / API for uploading a JD and viewing ranked candidates interactively.
- Unit tests for each ranker component.

---

## 📄 License

This project was built for the *India Runs on Data & AI* challenge. Add a license of your choice (e.g. MIT) if you intend to open-source it more broadly.
