"""
Tools owned by the Resume Advisor Agent.
"""


def analyze_resume_profile(
    current_skills: list[str],
    target_role: str,
    years_experience: int | None = None,
) -> dict:
    """
    Generate structured resume-positioning guidance.

    This tool does not rewrite a resume.
    It provides structured inputs that the
    Resume Advisor Agent can reason about.

    Args:
        current_skills:
            Skills currently possessed.

        target_role:
            Target job role.

        years_experience:
            Approximate professional experience.

    Returns:
        Structured profile information.
    """

    skills = [
        skill.strip()
        for skill in current_skills
        if skill.strip()
    ]

    if not target_role.strip():
        raise ValueError(
            "target_role is required."
        )

    result = {
        "target_role": target_role.strip(),
        "skills_to_highlight": skills,
        "recommended_sections": [
            "Professional Summary",
            "Technical Skills",
            "Professional Experience",
            "Projects",
            "Education and Certifications",
        ],
        "positioning_guidance": [
            (
                "Lead with experience relevant "
                "to the target role."
            ),
            (
                "Connect technical skills to "
                "measurable project outcomes."
            ),
            (
                "Highlight hands-on projects for "
                "newly developed skills."
            ),
            (
                "Use role-relevant terminology "
                "accurately and naturally."
            ),
        ],
    }

    if years_experience is not None:
        result[
            "years_experience"
        ] = years_experience

    return result
