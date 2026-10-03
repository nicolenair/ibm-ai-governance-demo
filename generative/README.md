# Generative: evaluating a complaint summarisation prompt

[Back to the main README](../README.md)

[run_inference_v2.ipynb](run_inference_v2.ipynb) runs a prompt that summarises customer complaints, then evaluates the results in watsonx.governance as a prompt template. The model is external to watsonx: the notebook calls it directly and sends the inputs and outputs to watsonx.governance for scoring.

## What the notebook does

1. Loads a CSV of complaints (`input`) with reference summaries (`output`).
2. Calls the model for each row. Functions are provided for Anthropic, watsonx.ai and Ollama; add your own for other providers.
3. Sends the records to watsonx.governance and runs the evaluation for a prompt template asset.
4. Repeats this for each lifecycle stage: development, pre-production and production.

Metrics configured:

- **Generative AI quality**: sentence similarity, text quality, ROUGE, METEOR, Flesch readability, SARI, and PII detection on input and output
- **Model health**
- **Drift v2**, in production only

## Prerequisites

- A watsonx.governance instance, on AWS or on Cloud Pak for Data.
- A watsonx project, and a deployment space for the pre-production and production stages.
- A detached prompt template asset for each stage you want to evaluate.
- An API key for the model provider (Anthropic by default).
- A notebook runtime inside a watsonx project. The notebook loads the dataset through the project library, which needs a project token.

## Setup

```bash
cd generative
cp .env.template .env
# fill in .env
```

| Variable | Description |
|----------|-------------|
| `AWS_API_KEY` | watsonx.governance API key (AWS-hosted service) |
| `AWS_ACCOUNT_ID` | Account ID that scopes the token |
| `AWS_WOS_SERVICE_INSTANCE_ID` | watsonx.governance instance ID. This is a different ID from the account ID |
| `MCSP_URL` | Token service URL |
| `AWS_WOS_SERVICE_URL` | OpenScale service URL for your region |
| `ANTHROPIC_API_KEY` | Anthropic API key, if you use Claude |
| `IAM_URL` | IAM URL, if you use a watsonx.ai model |

Then, in the notebook:

- Set `DEPLOYMENT_TYPE` to `aws` or `cpd` in the first cell. For Cloud Pak for Data, fill in the `CPD_*` values there.
- Insert your project token in the cell marked `@hidden_cell`. Remove it again before you commit.
- In each evaluation cell, replace `pta_id`, `project_id` and `space_id` with the IDs of your own prompt template assets, project and space.
- Set `dataset` to the CSV you want to evaluate.

## Run

Run the cells in order. Each evaluation cell under "Workspace & asset specific evaluations" covers one stage, so you can run only the stages you need.

Results appear on the prompt template asset's Evaluate tab in the project or space.

## Files

| File | Rows | Purpose |
|------|------|---------|
| `complaints_dataset.csv` | 20 | Small sample for a quick test |
| `complaints_dataset_2.csv` | 99 | Larger evaluation sets, one per stage |
| `complaints_dataset_3.csv` | 91 | |
| `complaints_dataset_4.csv` | 93 | |

The complaints are synthetic.
