# IBM AI Governance Demo

Demo assets that show watsonx.governance governing three kinds of AI, none of which has to run on IBM technology:

| Module | What is governed | Where it runs | Start here |
|--------|------------------|---------------|------------|
| [predictive/](predictive/) | A hiring classifier (logistic regression) | Amazon SageMaker endpoint | [predictive/README.md](predictive/README.md) |
| [generative/](generative/) | A complaint summarisation prompt | Anthropic Claude (or watsonx.ai, Ollama) | [generative/README.md](generative/README.md) |
| [agentic/](agentic/) | A multi-agent investment committee assistant | watsonx Orchestrate, with an external LangGraph agent | [agentic/README.md](agentic/README.md) |

Each module is self-contained: it has its own README, its own `.env` file and its own data. Run any one of them without the others.

## What each module shows

- **Predictive**: train and deploy a model on SageMaker, subscribe it in watsonx.governance, then monitor quality, fairness, drift and explainability in production and pre-production.
- **Generative**: evaluate a prompt template against a labelled dataset in development, pre-production and production, with text quality, similarity and PII metrics.
- **Agentic**: bring agents built in watsonx Orchestrate into the Governance console inventory through AI Asset Discovery, and pull their evaluation metrics in through metrics sync.

## Repository structure

```
ibm-ai-governance-demo/
├── predictive/     # SageMaker hiring model + watsonx.governance monitors (notebook)
├── generative/     # Prompt template evaluation for complaint summarisation (notebook)
├── agentic/        # Governance console integration for the investment agent demo
└── README.md
```

## Prerequisites

- A watsonx.governance instance. The notebooks are written for watsonx.governance as a Service on AWS; the generative notebook also supports Cloud Pak for Data.
- Python 3.10 or later, with Jupyter.
- Module-specific accounts and keys, listed in each module's README.

## Quick start

```bash
git clone https://github.com/nicolenair/ibm-ai-governance-demo.git
cd ibm-ai-governance-demo
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install jupyter
```

Then follow the README of the module you want to run.

## Handling credentials

- Each module reads its settings from a `.env` file that is ignored by git. Copy the module's `.env.example` or `.env.template` and fill it in. Never commit a `.env` file.
- Notebook outputs can contain account IDs, instance IDs and resource names. Clear outputs before committing:

  ```bash
  jupyter nbconvert --clear-output --inplace predictive/*.ipynb generative/*.ipynb
  ```

## Data

All datasets in this repository are synthetic and exist only to demonstrate monitoring. The hiring data includes a gender attribute (`IsFemale`) on purpose, so that the fairness monitor has something to measure. Do not use the model or the data for real hiring decisions.
