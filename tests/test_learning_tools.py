from tools.learning_tools import (
    create_learning_plan,
)


def test_learning_plan():

    result = create_learning_plan(
        skills=[
            "Python",
            "MLflow",
        ],
        weeks=4,
    )

    assert (
        result["duration_weeks"]
        == 4
    )

    assert len(
        result["plan"]
    ) == 4

    assert result[
        "skills"
    ] == [
        "Python",
        "MLflow",
    ]
