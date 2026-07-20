# Tea Plantation Advisor

Tea Plantation Advisor is a beginner-friendly [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/) demo for agricultural advisory workshops. Leaf guides growers through the tea bush lifecycle and uses Python function tools to recommend the current growth stage from plant age, describe stages in detail, and generate reference illustrations.

## Features

- A single ADK agent with a clear `root_agent` entry point
- Six tea bush growth stages, from nursery propagation to maintenance pruning
- Tools for recommending a stage from plant age, listing stages, and retrieving stage details
- On-demand tea plantation illustrations saved as ADK session artifacts
- A warm, practical agronomist-inspired guide designed to make agent concepts approachable

## Tea growth stages

| Phase | Stage | Age range | Key focus |
| --- | --- | --- | --- |
| Establishment | Nursery & Propagation | 0-6 months | Rooting cuttings under shade |
| Establishment | Transplanting & Field Establishment | 6-18 months | Field planting and mulching |
| Vegetative | Formative Pruning & Framework Building | 18-36 months | Building the plucking table |
| Production | Early / Light Plucking | 36-48 months | First careful harvests |
| Production | Mature Plucking Cycle | 48+ months, ongoing | Regular plucking rounds |
| Maintenance | Maintenance & Rejuvenation Pruning | Recurring / age-triggered | Resetting bush productivity |

## Project structure

```text
.
├── tea_plantation_agent/
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

Image generation uses `gemini-3.1-flash-image` by default. You can override it by
setting `TEA_IMAGE_MODEL` in `.env`. Your Google project or API key must have
access to the selected image model.

## Run the agent

From the repository root, with the virtual environment active, run:

```bash
adk web
```

Open the local URL printed by ADK and select `tea_plantation_agent`.

## Example prompts

Start a conversation:

- "Hi Leaf! My tea plants are 10 months old, what stage are they in?"
- "I just planted a new tea field. What should I expect in the first year?"
- "What growth stages does a tea bush go through?"

Explore stages:

- "Show me all establishment-phase stages."
- "Tell me about STAGE-MAINTENANCE-PRUNE."
- "What are the common issues during the early plucking stage?"

Get a recommendation:

- "My tea plants are 40 months old. What should I be doing right now?"
- "How many months until my 30-month-old plants reach the next stage?"
- "I have a field that's 5 years old and yields are dropping. What stage should it be in?"

Create images:

- "Create a 16:9 image of a young tea plantation being mulched after transplanting."
- "Illustrate a mature tea plantation during a plucking round at sunrise."
- "Make a square reference image for STAGE-NURSERY showing shaded cutting beds."

## How it works

[`tea_plantation_agent/agent.py`](tea_plantation_agent/agent.py) defines the stage catalogue, four function tools, and the ADK agent:

- `list_stages` lists all growth stages or filters them by phase.
- `get_stage_details` returns the complete data for one stage.
- `recommend_stage_for_age` matches a plant's age in months to its current stage and care recommendations.
- `create_plantation_image` generates a PNG and saves it as an ADK session artifact.

Leaf is instructed to ground all stage facts and care recommendations in those tool results while responding as a warm, practical guide focused on real cultivation outcomes.

## Workshop extension ideas

- Add filtering by region or climate to adjust stage timing.
- Add a tool that logs plucking rounds or fertilization history.
- Move the stage catalogue into a JSON file or database.
- Add automated tests for the stage tools.

## Security

Keep API keys and cloud credentials only in your local `.env` file or a secure secret manager. If a secret is ever committed, revoke or rotate it before removing it from Git history.
