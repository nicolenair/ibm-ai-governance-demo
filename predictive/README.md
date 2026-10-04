# Predictive: hiring model on SageMaker, monitored by watsonx.governance

[Back to the main README](../README.md)

[hiring_sagemaker_openscale.ipynb](hiring_sagemaker_openscale.ipynb) trains a hiring classifier, deploys it to an Amazon SageMaker real-time endpoint, and sets up monitoring for it in watsonx.governance (OpenScale) on AWS.

## What the notebook does

1. Trains a scikit-learn logistic regression locally on `hiring_training_data.csv`. No SageMaker training job is needed.
2. Deploys the model to a SageMaker endpoint using [inference.py](inference.py).
3. Registers the model as an external model in the inventory. Track it in an AI use case from *AI governance → External models* before you go on: this has to happen before the endpoint is subscribed, so that the evaluation results are attached to it.
4. Connects to watsonx.governance and registers Amazon SageMaker as a machine learning provider.
5. Subscribes the endpoint and logs payload and feedback data.
6. Configures and runs the monitors:
   - **Quality**, against labelled feedback data
   - **Fairness**, on the `IsFemale` attribute
   - **Explainability**, for individual predictions
   - **Drift v2**, against a baseline built from the training data
   - **Model health**
7. Registers the same endpoint a second time as a pre-production deployment and evaluates it on the labelled test file, so the model appears in both stages.

## Prerequisites

- An AWS account, and credentials in your shell that can create a SageMaker model and endpoint and write to the account's default SageMaker S3 bucket.
- A SageMaker execution role.
- An AWS access key that watsonx.governance uses to discover and score the endpoint.
- A watsonx.governance instance on AWS and an API key for it.

## Setup

```bash
cd predictive
cp .env.example .env
# fill in .env
```

| Variable | Description |
|----------|-------------|
| `AWS_REGION` | Region where the SageMaker endpoint runs |
| `SAGEMAKER_ROLE_ARN` | SageMaker execution role |
| `ENDPOINT_NAME` | Name for the endpoint (default `hiring-model-endpoint`) |
| `OPENSCALE_AWS_ACCESS_KEY_ID`, `OPENSCALE_AWS_SECRET_ACCESS_KEY` | Access key watsonx.governance uses to reach the endpoint |
| `IBM_API_KEY` | watsonx.governance API key |
| `PLATFORM_URL`, `OPENSCALE_URL` | Platform and OpenScale URLs for your region |
| `OPENSCALE_INSTANCE_ID` | Instance ID, from the Insights UI |
| `SERVICE_PROVIDER_NAME` | Display name for the SageMaker provider |
| `IBM_ACCOUNT_ID` | IBM account ID (not the AWS account ID), used to register the external model |
| `INVENTORY_ID` | ID of the inventory to save the external model in. The registration cell lists the valid IDs if this one is wrong |
| `DB_CREDENTIALS` | Only needed if the instance has no data mart yet |
| `DATA_DIR`, `LABEL`, `PROTECTED_ATTRIBUTE` | Data location, label column and fairness attribute |

## Run

Open the notebook and run the cells in order. The first cell installs the dependencies. Deploying the endpoint takes about 5 to 8 minutes.

The service issues short-lived tokens. If a call returns 401 partway through, run `refresh_token()` and retry the cell.

When the notebook finishes, open `https://<region>.aws.data.ibm.com/aiopenscale/insights` and select the endpoint to see the results.

## Files

| File | Purpose |
|------|---------|
| `hiring_training_data.csv` | Training data, with header |
| `hiring_train_ll.csv` | The same data with no header and the label first |
| `hiring_payload_data.csv`, `hiring_payload_data_2.csv` | Two batches of scoring requests for payload logging |
| `hiring_eval_data_1.csv` | Labelled data for the quality monitor and pre-production evaluation |
| `inference.py` | SageMaker inference script, written by the notebook |
| `sagemaker_model/` | Model parameters and archives produced by the notebook |

## Clean up

The SageMaker endpoint is billed while it is running. Delete it when you are done, along with the subscription, using the last cell of the notebook.
