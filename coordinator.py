"""
Coordinator for the local multi-agent system.

The coordinator decides which specialist agents
should work on a user's request.
"""

import json
from typing import Any

from ollama import Client

from agents.career_agent import (
    run_career_agent,
)
from agents.learning_agent import (
    run_learning_agent,
)
from agents.resume_agent import (
    run_resume_agent,
)
from config import (
    MAX_COORDINATOR_STEPS,
    OLLAMA_HOST,
    OLLAMA_MODEL,
)


client = Client(
    host=OLLAMA_HOST
)


COORDINATOR_PROMPT = """
You are the Coordinator Agent for a multi-agent
career assistance system.

You have three specialist agents available.

1. run_career_agent
   Use for:
   - professional experience;
   - skill comparison;
   - skill gaps;
   - career analysis.

2. run_learning_agent
   Use for:
   - learning plans;
   - study roadmaps;
   - skill-development plans.

3. run_resume_agent
   Use for:
   - resume positioning;
   - professional profile presentation;
   - skills to highlight for a target role.

Your job is to:

1. Understand the user's overall goal.
2. Delegate relevant subtasks to specialist agents.
3. You may call more than one specialist.
4. Pass enough context in each delegated task.
5. Use specialist results when deciding whether
   another specialist is required.
6. Do not pretend that a specialist was called
   unless you actually call it.
7. Do not invent specialist results.
8. When specialist work is complete, synthesize
   the results into one coherent response.
9. Avoid repeating the same information.
10. If critical information is missing, ask the
    user for it instead of inventing it.

The specialist agents are tools from your
perspective.
"""


AGENT_TOOLS = {
    "run_career_agent": (
        run_career_agent
    ),
    "run_learning_agent": (
        run_learning_agent
    ),
    "run_resume_agent": (
        run_resume_agent
    ),
}


def serialize_result(
    result: Any,
) -> str:
    """
    Convert specialist output into JSON text.
    """

    return json.dumps(
        result,
        ensure_ascii=False,
        default=str,
    )


def run_coordinator(
    user_message: str,
    conversation_history: list[
        dict[str, str]
    ]
    | None = None,
) -> dict:
    """
    Run the coordinator-agent loop.

    The coordinator can delegate work to one
    or more specialist agents.
    """

    messages: list[Any] = [
        {
            "role": "system",
            "content": (
                COORDINATOR_PROMPT
            ),
        }
    ]

    if conversation_history:
        for message in (
            conversation_history[-10:]
        ):
            if message["role"] in {
                "user",
                "assistant",
            }:
                messages.append(
                    {
                        "role": (
                            message["role"]
                        ),
                        "content": (
                            message["content"]
                        ),
                    }
                )

    messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    coordinator_trace = []

    specialist_traces = []

    for step in range(
        1,
        MAX_COORDINATOR_STEPS + 1,
    ):
        response = client.chat(
            model=OLLAMA_MODEL,
            messages=messages,
            tools=list(
                AGENT_TOOLS.values()
            ),
        )

        assistant_message = (
            response.message
        )

        messages.append(
            assistant_message
        )

        tool_calls = (
            assistant_message.tool_calls
            or []
        )

        coordinator_trace.append(
            {
                "step": step,
                "delegations": [
                    call.function.name
                    for call in tool_calls
                ],
            }
        )

        if not tool_calls:
            final_answer = (
                assistant_message.content
                or (
                    "The coordinator finished "
                    "without producing a response."
                )
            )

            return {
                "answer": final_answer,
                "coordinator_trace": (
                    coordinator_trace
                ),
                "specialist_traces": (
                    specialist_traces
                ),
            }

        for call in tool_calls:
            agent_name = (
                call.function.name
            )

            arguments = (
                call.function.arguments
            )

            specialist = (
                AGENT_TOOLS.get(
                    agent_name
                )
            )

            if specialist is None:
                result = {
                    "agent": agent_name,
                    "error": (
                        "Unknown specialist."
                    ),
                }

            else:
                try:
                    result = specialist(
                        **arguments
                    )

                except Exception as error:
                    result = {
                        "agent": agent_name,
                        "error": str(error),
                    }

            specialist_traces.append(
                {
                    "coordinator_step": (
                        step
                    ),
                    "specialist": (
                        agent_name
                    ),
                    "task": arguments,
                    "result": result,
                }
            )

            messages.append(
                {
                    "role": "tool",
                    "tool_name": agent_name,
                    "content": (
                        serialize_result(
                            result
                        )
                    ),
                }
            )

    return {
        "answer": (
            "The coordinator reached its "
            "maximum number of delegation "
            "steps without completing the task."
        ),
        "coordinator_trace": (
            coordinator_trace
        ),
        "specialist_traces": (
            specialist_traces
        ),
    }


if __name__ == "__main__":
    print(
        "Local Multi-Agent Career System"
    )

    print(
        "Type 'exit' to stop."
    )

    history = []

    while True:
        user_input = input(
            "\nYou: "
        ).strip()

        if user_input.lower() in {
            "exit",
            "quit",
        }:
            break

        result = run_coordinator(
            user_message=user_input,
            conversation_history=history,
        )

        print(
            "\nCoordinator:",
            result["answer"],
        )

        history.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        history.append(
            {
                "role": "assistant",
                "content": result[
                    "answer"
                ],
            }
        )
