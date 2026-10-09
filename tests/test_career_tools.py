from datetime import date

from tools.career_tools import (
    analyze_skill_gap,
    calculate_experience,
)


def test_calculate_experience():

    result = calculate_experience(
        2020
    )

    assert (
        result["years_of_experience"]
        ==
        date.today().year - 2020
    )


def test_skill_gap():

    result = analyze_skill_gap(
        current_skills=[
            "Python",
            "Docker",
        ],
        target_skills=[
            "Python",
            "Docker",
            "Kubernetes",
        ],
    )

    assert result[
        "missing_skills"
    ] == [
        "Kubernetes"
    ]

    assert set(
        result["matching_skills"]
    ) == {
        "Python",
        "Docker",
    }
