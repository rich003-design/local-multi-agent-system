
"""
Streamlit UI for the local multi-agent system.
"""

import streamlit as st

from coordinator import (
    run_coordinator,
)


WELCOME_MESSAGE = """
Hello! I am the coordinator for a local
multi-agent career system.

I can delegate tasks to:

- Career Analyst
- Learning Planner
- Resume Advisor

Give me a career goal that requires one or more
of these specialists.
"""


def initialize_session():
    """
    Initialize Streamlit state.
    """

    if "messages" not in (
        st.session_state
    ):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    WELCOME_MESSAGE
                ),
            }
        ]

    if "coordinator_trace" not in (
        st.session_state
    ):
        st.session_state[
            "coordinator_trace"
        ] = []

    if "specialist_traces" not in (
        st.session_state
    ):
        st.session_state[
            "specialist_traces"
        ] = []


def reset_conversation():
    """
    Reset conversation state.
    """

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                WELCOME_MESSAGE
            ),
        }
    ]

    st.session_state[
        "coordinator_trace"
    ] = []

    st.session_state[
        "specialist_traces"
    ] = []


st.set_page_config(
    page_title=(
        "Local Multi-Agent System"
    ),
    page_icon="🤖",
    layout="wide",
)


initialize_session()


st.title(
    "🤖 Local Multi-Agent Career System"
)

st.caption(
    "Coordinator + specialized local "
    "Ollama agents"
)


with st.sidebar:

    st.header(
        "Agent Team"
    )

    st.markdown(
        """
        **Coordinator**
        Routes and combines work.

        **Career Analyst**
        Experience and skill gaps.

        **Learning Planner**
        Learning roadmaps.

        **Resume Advisor**
        Profile and resume positioning.
        """
    )

    if st.button(
        "Clear conversation",
        use_container_width=True,
    ):
        reset_conversation()
        st.rerun()

    if st.session_state[
        "coordinator_trace"
    ]:

        st.divider()

        with st.expander(
            "Coordinator Trace"
        ):
            st.json(
                st.session_state[
                    "coordinator_trace"
                ]
            )

    if st.session_state[
        "specialist_traces"
    ]:

        with st.expander(
            "Specialist Traces"
        ):
            st.json(
                st.session_state[
                    "specialist_traces"
                ]
            )


for message in (
    st.session_state.messages
):

    with st.chat_message(
        message["role"]
    ):
        st.markdown(
            message["content"]
        )


user_prompt = st.chat_input(
    "Give the agent team a task..."
)


if user_prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    with st.chat_message(
        "user"
    ):
        st.markdown(
            user_prompt
        )

    history = (
        st.session_state.messages[
            :-1
        ]
    )

    with st.chat_message(
        "assistant"
    ):

        try:

            with st.status(
                (
                    "Coordinator is "
                    "delegating work..."
                ),
                expanded=True,
            ) as status:

                result = (
                    run_coordinator(
                        user_message=(
                            user_prompt
                        ),
                        conversation_history=(
                            history
                        ),
                    )
                )

                status.update(
                    label=(
                        "Agent team "
                        "completed the task."
                    ),
                    state="complete",
                    expanded=False,
                )

            answer = result[
                "answer"
            ]

            st.markdown(
                answer
            )

            st.session_state[
                "coordinator_trace"
            ] = result[
                "coordinator_trace"
            ]

            st.session_state[
                "specialist_traces"
            ] = result[
                "specialist_traces"
            ]

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

        except Exception as error:

            st.error(
                "The multi-agent system "
                "could not complete the task."
            )

            st.exception(
                error
            )
