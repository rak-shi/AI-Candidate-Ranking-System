import numpy as np
from sklearn.preprocessing import MinMaxScaler

from ranking.bm25_ranker import BM25Ranker
from ranking.embedding_ranker import EmbeddingRanker


class HybridRanker:

    def __init__(self):

        self.bm25 = BM25Ranker()
        self.embedding = EmbeddingRanker()

    def normalize(self, scores):
        """
        Normalize scores to range [0,1]
        """

        scores = np.array(scores).reshape(-1, 1)

        scaler = MinMaxScaler()

        return scaler.fit_transform(scores).flatten()

    def skill_score(self, candidate, job_description):
        """
        Calculate skill matching score.
        """

        jd = job_description.lower()

        skills = candidate.get("skills", [])

        if not skills:
            return 0

        matched = 0
        total = len(skills)

        for skill in skills:

            if isinstance(skill, dict):
                skill_name = skill.get("name", "")
            else:
                skill_name = str(skill)

            if skill_name.lower() in jd:
                matched += 1

        return matched / total if total else 0

    def experience_score(self, candidate):
        """
        Score based on years of experience and career history.
        """

        profile = candidate.get("profile", {})
        years = profile.get("years_of_experience", 0)

        career = candidate.get("career_history", [])

        score = min(years / 10, 1.0)

        if len(career) >= 3:
            score += 0.05

        return min(score, 1.0)

    def education_score(self, candidate):
        """
        Score education based on degree and institute tier.
        """

        education = candidate.get("education", [])

        if not education:
            return 0

        edu = education[0]

        score = 0.3

        degree = edu.get("degree", "").lower()

        if "ph" in degree:
            score += 0.4
        elif "m.tech" in degree or "m.e" in degree or "m.s" in degree or "m.sc" in degree:
            score += 0.3
        elif "b.tech" in degree or "b.e" in degree or "b.sc" in degree:
            score += 0.2

        tier = edu.get("tier", "")

        if tier == "tier_1":
            score += 0.3
        elif tier == "tier_2":
            score += 0.2
        elif tier == "tier_3":
            score += 0.1

        return min(score, 1.0)

    def career_bonus(self, candidate):
        """
        Give bonus for AI/ML related job titles.
        """

        career = candidate.get("career_history", [])

        keywords = [
            "machine learning",
            "ml",
            "ai",
            "nlp",
            "llm",
            "search",
            "ranking",
            "backend engineer",
            "data scientist",
            "applied scientist",
            "research engineer",
            "ai engineer",
            "ml engineer",
            "computer vision"
        ]

        for job in career:

            title = job.get("title", "").lower()

            if any(keyword in title for keyword in keywords):
                return 0.05

        return 0
    
    def rank(self, candidates, job_description, top_k=100):

        # -------------------------
        # Build BM25 Index
        # -------------------------
        self.bm25.fit(candidates)

        query_tokens = self.bm25.preprocess(job_description)

        bm25_scores = self.bm25.bm25.get_scores(query_tokens)
        bm25_scores = self.normalize(bm25_scores)

        # -------------------------
        # Embedding Similarity
        # -------------------------
        embedding_scores = self.embedding.get_similarity_scores(
            job_description
        )

        embedding_scores = self.normalize(embedding_scores)

        # -------------------------
        # Final Ranking
        # -------------------------

        ranked = []

        for i, candidate in enumerate(candidates):

            skill = self.skill_score(
                candidate,
                job_description
            )

            experience = self.experience_score(candidate)

            education = self.education_score(candidate)

            career_bonus = self.career_bonus(candidate)

            # Final Hybrid Score
            final_score = (
                0.35 * embedding_scores[i]
                + 0.30 * bm25_scores[i]
                + 0.25 * skill
                + 0.07 * experience
                + 0.03 * education
                + career_bonus
            )

            ranked.append({

                "candidate": candidate,

                "score": round(float(final_score), 4),

                "bm25": round(float(bm25_scores[i]), 4),

                "embedding": round(float(embedding_scores[i]), 4),

                "skill_score": round(float(skill), 4),

                "experience_score": round(float(experience), 4),

                "education_score": round(float(education), 4),

                "career_bonus": round(float(career_bonus), 4)

            })

        ranked.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return ranked[:top_k]