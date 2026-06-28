import os
import pickle
from sentence_transformers import SentenceTransformer
from tqdm import tqdm


def build_candidate_text(candidate):
    """
    Convert a candidate profile into a single text string.
    Adjust keys based on your dataset.
    """

    name = candidate.get("name", "")
    summary = candidate.get("summary", "")
    skills = candidate.get("skills", [])

    if isinstance(skills, list):
        skills = " ".join(str(skill) for skill in skills)

    experience = candidate.get("experience", "")
    education = candidate.get("education", "")

    return f"{name} {summary} {skills} {experience} {education}"


def generate_embeddings(candidates):

    model = SentenceTransformer("all-MiniLM-L6-v2")

    texts = [
        build_candidate_text(candidate)
        for candidate in candidates
    ]

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        batch_size=64,
        convert_to_numpy=True
    )

    os.makedirs("processed", exist_ok=True)

    with open("processed/embeddings.pkl", "wb") as f:
        pickle.dump(embeddings, f)

    print("Embeddings saved successfully!")


if __name__ == "__main__":

    import json

    candidates = []

    with open("data/candidates.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            candidates.append(json.loads(line))

    generate_embeddings(candidates)