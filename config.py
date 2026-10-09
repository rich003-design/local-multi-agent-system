"""
Central configuration for the multi-agent system.
"""

import os

from dotenv import load_dotenv


load_dotenv()


OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen3:4b",
)

OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434",
)

MAX_COORDINATOR_STEPS = int(
    os.getenv(
        "MAX_COORDINATOR_STEPS",
        "6",
    )
)

MAX_AGENT_STEPS = int(
    os.getenv(
        "MAX_AGENT_STEPS",
        "5",
    )
)
