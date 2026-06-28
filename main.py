import os
import json
import pickle
import pandas as pd

from docx import Document
from sentence_transformers import SentenceTransformer

from ranking.hybrid_ranker import HybridRanker
from ranking.explanation import ExplanationGenerator


# ----------------------------
# Load Candidates
# ----------------------------
def load_candidates(file_path):

    candidates = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            candidates.append(json.loads(line))

    return candidates


# ----------------------------
# Load Job Description
# ----------------------------
def load_job_description(path):

    if path.endswith(".docx"):

        doc = Document(path)

        return "\n".join(
            paragraph.text
            for paragraph in doc.paragraphs
        )

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ----------------------------
# Convert Candidate to Text
# ----------------------------
def build_candidate_text(candidate):

    profile = candidate.get("profile", {})

    fields = []

    fields.append(profile.get("anonymized_name", ""))
    fields.append(profile.get("headline", ""))
    fields.append(profile.get("summary", ""))

    # Skills
    skills = candidate.get("skills", [])
    skill_names = []

    for skill in skills:
        skill_names.append(skill.get("name", ""))

    fields.append(" ".join(skill_names))

    # Career History
    career = candidate.get("career_history", [])

    for job in career:
        fields.append(job.get("title", ""))
        fields.append(job.get("company", ""))
        fields.append(job.get("description", ""))

    # Education
    education = candidate.get("education", [])

    for edu in education:
        fields.append(edu.get("degree", ""))
        fields.append(edu.get("institution", ""))

    return " ".join(fields)


# ----------------------------
# Generate Embeddings
# ----------------------------
def generate_embeddings(candidates):

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    texts = [
        build_candidate_text(candidate)
        for candidate in candidates
    ]

    embeddings = model.encode(
        texts,
        batch_size=64,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    os.makedirs(
        "processed",
        exist_ok=True
    )

    with open(
        "processed/embeddings.pkl",
        "wb"
    ) as f:

        pickle.dump(
            embeddings,
            f
        )

    print("Embeddings saved.")


# ----------------------------
# Main
# ----------------------------
def main():

    candidate_file = "data/candidates.jsonl"

    jd_file = "data/job_description.docx"

    output_file = "output.csv"

    print("Loading candidates...")

    candidates = load_candidates(
        candidate_file
    )

    print(
        "Candidates:",
        len(candidates)
    )

    print("Loading JD...")

    job_description = load_job_description(
        jd_file
    )

    if not os.path.exists(
        "processed/embeddings.pkl"
    ):

        print(
            "Generating embedding" \
            "" \
            "s..."
        )

        generate_embeddings(
            candidates
        )

    print("Ranking...")

    ranker = HybridRanker()

    ranked = ranker.rank(
        candidates,
        job_description,
        top_k=100
    )

    explainer = ExplanationGenerator()

    rows = []

    for index, result in enumerate(
        ranked,
        start=1
    ):

        candidate = result["candidate"]

        explanation = explainer.generate(
            candidate,
            job_description,
            result
        )

        rows.append({

            "rank": index,

            "candidate_id": candidate.get("candidate_id", ""),

            "name": candidate.get("profile", {}).get("anonymized_name", ""),

            "score":
                round(
                    result["score"],
                    4
                ),

            "explanation":
                explanation

        })

    df = pd.DataFrame(rows)

    df.to_csv(
        output_file,
        index=False
    )

    print(
        "Done!"
    )

    print(
        "Saved:",
        output_file
    )


if __name__ == "__main__":

    main()