"""
Tools owned by the Career Analyst Agent.
"""

from datetime import date


def calculate_experience(
    start_year: int,
) -> dict:
    """
    Calculate approximate professional experience.

    Args:
        start_year:
            Year the professional career started.

    Returns:
        Experience information.
    """

    current_year = date.today().year

    if start_year < 1900:
        raise ValueError(
            "start_year must be 1900 or later."
        )

    if start_year > current_year:
        raise ValueError(
            "start_year cannot be in the future."
        )

    return {
        "start_year": start_year,
        "current_year": current_year,
        "years_of_experience": (
            current_year - start_year
        ),
    }


def analyze_skill_gap(
    current_skills: list[str],
    target_skills: list[str],
) -> dict:
    """
    Compare current skills with target skills.

    Args:
        current_skills:
            Skills currently possessed.

        target_skills:
            Skills desired for the target role.

    Returns:
        Matching and missing skills.
    """

    current_map = {
        skill.strip().lower(): skill.strip()
        for skill in current_skills
        if skill.strip()
    }

    target_map = {
        skill.strip().lower(): skill.strip()
        for skill in target_skills
        if skill.strip()
    }

    current_keys = set(
        current_map
    )

    target_keys = set(
        target_map
    )

    matching_keys = sorted(
        current_keys & target_keys
    )

    missing_keys = sorted(
        target_keys - current_keys
    )

    return {
        "matching_skills": [
            target_map[key]
            for key in matching_keys
        ],
        "missing_skills": [
            target_map[key]
            for key in missing_keys
        ],
    }
