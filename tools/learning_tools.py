"""
Tools owned by the Learning Planner Agent.
"""


def create_learning_plan(
    skills: list[str],
    weeks: int = 8,
) -> dict:
    """
    Create a weekly learning plan.

    Args:
        skills:
            Skills to learn.

        weeks:
            Number of weeks available.

    Returns:
        Structured learning plan.
    """

    cleaned_skills = [
        skill.strip()
        for skill in skills
        if skill.strip()
    ]

    if not cleaned_skills:
        raise ValueError(
            "At least one skill is required."
        )

    if weeks < 1:
        raise ValueError(
            "weeks must be at least 1."
        )

    plan = []

    for week in range(
        1,
        weeks + 1,
    ):
        skill = cleaned_skills[
            (week - 1)
            % len(cleaned_skills)
        ]

        plan.append(
            {
                "week": week,
                "focus": skill,
                "activities": [
                    (
                        f"Learn the core concepts "
                        f"of {skill}"
                    ),
                    (
                        f"Complete a hands-on "
                        f"{skill} exercise"
                    ),
                    (
                        f"Build or improve a small "
                        f"project using {skill}"
                    ),
                    (
                        f"Document what you learned "
                        f"about {skill}"
                    ),
                ],
            }
        )

    return {
        "duration_weeks": weeks,
        "skills": cleaned_skills,
        "plan": plan,
    }
