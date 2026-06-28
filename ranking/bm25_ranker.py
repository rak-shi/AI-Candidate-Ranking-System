from rank_bm25 import BM25Okapi
import re


class BM25Ranker:
    def __init__(self):
        self.bm25 = None
        self.candidates = None
        self.tokenized_corpus = None

    def preprocess(self, text):
        """
        Clean and tokenize text.
        """
        if not text:
            return []

        text = str(text).lower()
        text = re.sub(r"[^a-z0-9 ]", " ", text)

        return text.split()

    def build_candidate_text(self, candidate):
        """
        Convert candidate profile into searchable text.
        Modify fields according to your dataset.
        """

        fields = []

        # Name
        fields.append(str(candidate.get("name", "")))

        # Summary
        fields.append(str(candidate.get("summary", "")))

        # Skills
        skills = candidate.get("skills", [])

        if isinstance(skills, list):
            skill_names = []

            for skill in skills:
                if isinstance(skill, dict):
                    skill_names.append(skill.get("name", ""))
                else:
                    skill_names.append(str(skill))

            fields.append(" ".join(skill_names))

        else:
            fields.append(str(skills))

        # Experience
        experience = candidate.get("career_history", [])

        if isinstance(experience, list):
            exp_text = []

            for exp in experience:
                if isinstance(exp, dict):
                    exp_text.append(exp.get("title", ""))
                    exp_text.append(exp.get("company", ""))
                    exp_text.append(exp.get("description", ""))

            fields.append(" ".join(exp_text))

        # Education
        education = candidate.get("education", [])

        if isinstance(education, list):
            edu_text = []

            for edu in education:
                if isinstance(edu, dict):
                    edu_text.append(edu.get("degree", ""))
                    edu_text.append(edu.get("institution", ""))

            fields.append(" ".join(edu_text))

        return " ".join(fields)

    def fit(self, candidates):
        """
        Build BM25 index.
        """

        self.candidates = candidates

        corpus = []

        for candidate in candidates:
            text = self.build_candidate_text(candidate)
            corpus.append(self.preprocess(text))

        self.tokenized_corpus = corpus
        self.bm25 = BM25Okapi(corpus)

    def rank(self, job_description, top_k=100):
        """
        Rank candidates using BM25.
        """

        query_tokens = self.preprocess(job_description)

        scores = self.bm25.get_scores(query_tokens)

        ranked = sorted(
            zip(self.candidates, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return ranked[:top_k]