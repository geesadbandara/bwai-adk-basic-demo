# CodeQuest Academy

CodeQuest Academy is a beginner-friendly, story-driven [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/) demo for university workshops. Its agent, ARIA, acts as a fantasy guildmaster and uses Python function tools to recommend programming quests, describe them, and check whether a student is ready to begin.

## Features

- A single ADK agent with a clear `root_agent` entry point
- Six quests based on common programming challenges
- Tools for listing quests, retrieving details, and checking hero readiness
- A lightweight fantasy theme designed to make agent concepts approachable

## Quest catalogue

| Difficulty | Quest | Boss | Skill focus |
| --- | --- | --- | --- |
| Novice | The Off-By-One Forest | The Fencepost Wolf | Loop boundaries |
| Novice | Null Pointer Swamp | The Segfault Serpent | Null checks |
| Apprentice | The Recursion Labyrinth | The Infinite Loop Hydra | Base cases |
| Apprentice | Big-O Mountain | The Quadratic Time Giant | Algorithm analysis |
| Master | The Merge Conflict Dragon's Lair | The Merge Conflict Dragon | Git branching |
| Master | Deadlock Dungeon | The Deadlock Twins | Concurrency |

## Project structure

```text
.
├── codequest_agent/
│   ├── __init__.py
│   └── agent.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

Local credentials, virtual environments, Python caches, and ADK session data are excluded from Git.

## Prerequisites

- Python 3.10 or newer
- A Google AI Studio API key or a configured Google Cloud project

## Setup

1. Clone the repository and enter its directory.

   ```bash
   git clone <your-repository-url>
   cd <repository-directory>
   ```

2. Create and activate a virtual environment.

   macOS/Linux:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   Windows PowerShell:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Install the dependencies.

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Create your local environment file.

   macOS/Linux:

   ```bash
   cp .env.example .env
   ```

   Windows PowerShell:

   ```powershell
   Copy-Item .env.example .env
   ```

5. Edit `.env` and provide either your Google AI Studio API key or your Vertex AI project settings. Never commit this file.

## Run the agent

From the repository root, with the virtual environment active, run:

```bash
adk web
```

Open the local URL printed by ADK and select `codequest_agent`. Try asking:

- “Show me the novice quests.”
- “Tell me about QUEST-RECURSION.”
- “I am level 4. Am I ready for Big-O Mountain?”

## How it works

[`codequest_agent/agent.py`](codequest_agent/agent.py) defines the quest data, three function tools, and the ADK agent:

- `list_quests` lists all quests or filters them by difficulty.
- `get_quest_details` returns the complete data for one quest.
- `check_quest_readiness` compares a hero's level with the quest requirement.

ARIA is instructed to ground all quest facts and readiness decisions in those tool results.

## Workshop extension ideas

- Add filtering by guild or required level.
- Add a tool that records completed quests and awards XP.
- Move the quest catalogue into a JSON file or database.
- Add automated tests for the quest tools.

## Security

Keep API keys and cloud credentials only in your local `.env` file or a secure secret manager. If a secret is ever committed, revoke or rotate it before removing it from Git history.
