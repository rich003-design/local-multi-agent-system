# Multi-Agent Architecture

## Overview

The application uses a hierarchical multi-agent architecture.

A Coordinator Agent receives the user's overall request and
delegates work to specialized agents.

## Components

### Coordinator Agent

Responsibilities:

- understand the overall request;
- choose appropriate specialists;
- delegate subtasks;
- consume specialist results;
- decide whether additional work is required;
- synthesize the final response.

### Career Analyst Agent

Responsibilities:

- professional experience;
- skill comparison;
- skill-gap analysis.

Tools:

- `calculate_experience`
- `analyze_skill_gap`

### Learning Planner Agent

Responsibilities:

- learning roadmaps;
- study sequencing;
- weekly learning plans.

Tool:

- `create_learning_plan`

### Resume Advisor Agent

Responsibilities:

- professional positioning;
- resume structure;
- skills to highlight.

Tool:

- `analyze_resume_profile`

## Architecture

```text
                     User
                      |
                      v
               Coordinator Agent
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
       Career      Learning     Resume
       Analyst     Planner      Advisor
          |           |           |
          v           v           v
       Career      Learning     Resume
       Tools       Tools        Tools
          |           |           |
          +-----------+-----------+
                      |
                      v
               Coordinator
                      |
                      v
                 Final Answer
```

## Delegation

Specialist agents are exposed as callable tools to the
Coordinator Agent.

The coordinator therefore chooses agents using the same
tool-calling mechanism that specialist agents use to choose
Python functions.

## Safety boundaries

Each specialist receives only the tools necessary for its role.

The system does not expose:

- arbitrary shell execution;
- arbitrary Python execution;
- unrestricted filesystem access;
- unrestricted network actions.

## Loop limits

The coordinator and specialist agents have independent
maximum-step limits to prevent uncontrolled loops.
