# Multi-Agent Execution Flow

## Example request

A user asks:

> Analyze my professional experience and skill gaps,
> create a learning plan, and advise how to position
> my profile for an MLOps role.

## Step 1

The Coordinator receives the complete request.

## Step 2

The Coordinator determines that career analysis is required.

```text
Coordinator
    |
    v
Career Analyst
```

## Step 3

Career Analyst chooses relevant tools.

```text
Career Analyst
    |
    +--> calculate_experience
    |
    +--> analyze_skill_gap
```

## Step 4

Career Analyst returns its findings to the Coordinator.

## Step 5

Coordinator determines that learning planning is required.

```text
Coordinator
    |
    v
Learning Planner
    |
    v
create_learning_plan
```

## Step 6

Learning Planner returns its result.

## Step 7

Coordinator delegates professional-positioning work.

```text
Coordinator
    |
    v
Resume Advisor
    |
    v
analyze_resume_profile
```

## Step 8

Coordinator receives all specialist results.

## Step 9

Coordinator synthesizes a final answer.

## Important distinction

The Coordinator does not directly execute specialist
Python tools.

Instead:

```text
Coordinator
    ↓
Specialist Agent
    ↓
Specialist Tool
```

This separation allows each agent to have:

- its own role;
- its own system prompt;
- its own tools;
- its own reasoning loop;
- its own operational boundaries.
