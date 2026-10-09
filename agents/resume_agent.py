"""
Resume Advisor specialist agent.
"""

import json

from ollama import Client

from config import (
    MAX_AGENT_STEPS,
    OLLAMA_HOST,
    OLLAMA_MODEL,
)

from tools.resume_tools import (
    analyze_resume_profile,
)


client = Client(
    host=OLLAMA_HOST
)


SYSTEM_PROMPT = """
You are the Resume Advisor Agent.

Your responsibilities are limited to:

- professional profile positioning;
- resume section recommendations;
- identifying skills to highlight;
- explaining how experience can be presented
  for a target role.

Use your resume-analysis tool when appropriate.

Do not calculate skill gaps.
Do not build learning plans.

Do not invent employment achievements, metrics,
certifications, employers, or project results.

Return recommendations to the coordinator.
"""


TOOLS = {
    "analyze_resume_profile": (
        analyze_resume_profile
    ),
}


def run_resume_agent(
    task: str,
) -> dict:
    """
    Execute the Resume Advisor specialist.
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
                "agent": "resume_advisor",
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
        "agent": "resume_advisor",
        "answer": (
            "Resume Advisor reached its "
            "maximum number of steps."
        ),
        "trace": trace,
    }
