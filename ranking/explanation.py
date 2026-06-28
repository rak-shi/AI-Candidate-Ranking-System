class ExplanationGenerator:
    """
    Generates human-readable explanations for why a candidate
    was ranked highly.
    """

    def __init__(self):
        pass

    def extract_skills(self, candidate):
        """
        Extract skills from candidate profile.
        """

        skills = candidate.get("skills", [])
        extracted = []

        if isinstance(skills, list):
            for skill in skills:
                if isinstance(skill, dict):
                    extracted.append(skill.get("name", "").strip())
                else:
                    extracted.append(str(skill).strip())

        return extracted

    def matched_skills(self, candidate, job_description):
        """
        Find matching skills between candidate and JD.
        """

        jd = job_description.lower()
        matched = []

        skills = self.extract_skills(candidate)

        for skill in skills:
            if skill and skill.lower() in jd:
                matched.append(skill)

        return matched

    def experience_summary(self, candidate):
        """
        Create a short experience summary.
        """

        experience = candidate.get("career_history", [])

        if not experience:
            return "No prior experience listed."

        companies = []

        for exp in experience:

            if not isinstance(exp, dict):
                continue

            title = exp.get("title", "")
            company = exp.get("company", "")

            if title and company:
                companies.append(f"{title} at {company}")
            elif title:
                companies.append(title)
            elif company:
                companies.append(company)

        if companies:
            return "Worked as " + ", ".join(companies[:2])

        return f"{len(experience)} experience entries found."

    def education_summary(self, candidate):
        """
        Create education summary.
        """

        education = candidate.get("education", [])

        if not education:
            return "Education details unavailable."

        first = education[0]

        if isinstance(first, dict):

            degree = first.get("degree", "")
            institute = first.get("institution", "")

            if degree and institute:
                return f"{degree} from {institute}"
            elif degree:
                return degree
            elif institute:
                return institute

        return "Education information available."

    def generate(self, candidate, job_description, ranking_result):
        """
        Generate explanation string.
        """

        matched = self.matched_skills(
            candidate,
            job_description
        )

        exp = self.experience_summary(candidate)
        edu = self.education_summary(candidate)

        explanation = []

        if matched:
            explanation.append(
                "Matched skills: " +
                ", ".join(matched[:6])
            )

        explanation.append(exp)
        explanation.append(edu)

        explanation.append(
            f"Semantic similarity score: {ranking_result['embedding']:.3f}"
        )

        explanation.append(
            f"BM25 relevance score: {ranking_result['bm25']:.3f}"
        )

        explanation.append(
            f"Overall ranking score: {ranking_result['score']:.3f}"
        )

        return " | ".join(explanation)