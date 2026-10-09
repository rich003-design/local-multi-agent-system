from coordinator import (
    run_coordinator,
)


def test_coordinator_returns_answer():

    result = run_coordinator(
        """
        I know Python and Docker.
        I want Python, Docker and Kubernetes.
        Identify my skill gap.
        """
    )

    assert "answer" in result

    assert (
        "coordinator_trace"
        in result
    )

    assert (
        "specialist_traces"
        in result
    )

    assert result[
        "answer"
    ]
