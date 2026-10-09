"""
Career Analyst specialist agent.
"""

import json

from ollama import Client

from config import (
    MAX_AGENT_STEPS,
    OLLAMA_HOST,
    OLLAMA_MODEL,
)

from tools.career_tools import (
    analyze_skill_gap,
    calculate_experience,
)


client = Client(
    host=OLLAMA_HOST
)


SYSTEM_PROMPT = """
You are the Career Analyst Agent.

Your responsibilities are limited to:

- professional experience analysis;
- current skill analysis;
- target skill comparison;
- skill-gap identification.

Use your tools whenever they provide a reliable
calculation or comparison.

Do not create learning plans.
Do not provide resume advice.
Do not pretend to be another specialist.

Return a concise factual result that another
coordinator agent can use.
"""


TOOLS = {
    "calculate_experience": (
        calculate_experience
    ),
    "analyze_skill_gap": (
        analyze_skill_gap
    ),
}


def run_career_agent(
    task: str,
) -> dict:
    """
    Execute the Career Analyst specialist.
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
                    "career_analyst"
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
        "agent": "career_analyst",
        "answer": (
            "Career Analyst reached its "
            "maximum number of steps."
        ),
        "trace": trace,
    }
