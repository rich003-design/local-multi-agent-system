"""
Learning Planner specialist agent.
"""

import json

from ollama import Client

from config import (
    MAX_AGENT_STEPS,
    OLLAMA_HOST,
    OLLAMA_MODEL,
)

from tools.learning_tools import (
    create_learning_plan,
)


client = Client(
    host=OLLAMA_HOST
)


SYSTEM_PROMPT = """
You are the Learning Planner Agent.

Your responsibilities are limited to:

- learning roadmaps;
- study sequencing;
- weekly learning plans;
- practical learning activities.

Use the learning-plan tool when the user requests
a structured plan.

Do not calculate professional experience.
Do not perform resume analysis.

Return a practical result that the coordinator
can combine with other specialist results.
"""


TOOLS = {
    "create_learning_plan": (
        create_learning_plan
    ),
}


def run_learning_agent(
    task: str,
) -> dict:
    """
    Execute the Learning Planner specialist.
    """

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": task,
        },
    ]

    trace = []

    for step in range(
        1,
        MAX_AGENT_STEPS + 1,
    ):
        response = client.chat(
            model=OLLAMA_MODEL,
            messages=messages,
            tools=list(
                TOOLS.values()
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

        trace.append(
            {
                "step": step,
                "tool_calls": [
                    call.function.name
                    for call in tool_calls
                ],
            }
        )

        if not tool_calls:
            return {
                "agent": (
                    "learning_planner"
                ),
                "answer": (
                    assistant_message.content
                ),
                "trace": trace,
            }

        for call in tool_calls:
            tool_name = (
                call.function.name
            )

            arguments = (
                call.function.arguments
            )

            function = TOOLS.get(
                tool_name
            )

            if function is None:
                result = {
                    "error": (
                        f"Unknown tool: "
                        f"{tool_name}"
                    )
                }

            else:
                try:
                    result = function(
                        **arguments
                    )
                except Exception as error:
                    result = {
                        "error": str(error)
                    }

            trace.append(
                {
                    "tool": tool_name,
                    "arguments": arguments,
                    "result": result,
                }
            )

            messages.append(
                {
                    "role": "tool",
                    "tool_name": tool_name,
                    "content": json.dumps(
                        result
                    ),
                }
            )

    return {
        "agent": "learning_planner",
        "answer": (
            "Learning Planner reached its "
            "maximum number of steps."
        ),
        "trace": trace,
    }
