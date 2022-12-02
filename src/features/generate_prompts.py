import logging
import os
from pathlib import Path

import pandas as pd
import pandas_gbq
from dotenv import find_dotenv, load_dotenv
from google.cloud import bigquery
from google.oauth2 import service_account

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

# Set up the credentials
credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)

# define IDs
PROJECT_ID = "mlops-zoomcamp-361419"
DATASET_ID = "gpt3_blog"
TABLE_ID = "medium"


def count_rows():
    # check if table has been updated
    query = f"""
    SELECT COUNT(*) FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
    """

    count = pandas_gbq.read_gbq(query, project_id=PROJECT_ID, credentials=credentials)
    count = count.values[0][0]

    logging.info(f"{count} rows in the table")

    return count


def ingest2bq(client, table_ref, final_path):
    try:
        # check if table exists
        client.get_table(table_ref)
        logging.info("Table exists")

        # load data into table
        df = pd.read_csv(final_path / "final_df.csv")

        # upload data to BigQuery
        df.to_gbq(
            f"{DATASET_ID}.{TABLE_ID}",
            project_id=PROJECT_ID,
            if_exists="replace",
            credentials=credentials,
        )

    except FileNotFoundError:
        logging.error("dataset does not exist")
    except Exception as e:
        logging.error(e)


def generate_prompts(final_path):
    try:
        with open("gpt3-prompts.sql", "r") as f:
            query = f.read()

        # read query from file
        df = pandas_gbq.read_gbq(query, project_id=PROJECT_ID, credentials=credentials)

        # dump results as jsonlines format
        df.to_json(final_path / "prompts.jsonl", orient="records", lines=True)

        # check if file exists
        if os.path.exists(final_path / "prompts.jsonl"):
            logging.info("prompts.jsonl created")

    except FileNotFoundError:
        logging.error("File not found")
    except Exception as e:
        logging.error(e)


def main():

    # define paths
    project_dir = Path(__file__).resolve().parents[2]
    final_path = project_dir / "data" / "2_final"

    # create BigQuery client
    client = bigquery.Client(credentials=credentials, project=PROJECT_ID)

    # define references
    dataset_ref = client.dataset(DATASET_ID)
    table_ref = dataset_ref.table(TABLE_ID)

    count = count_rows()

    if count == 0:
        ingest2bq(client, table_ref, final_path)

    count = count_rows()
    table_exists = client.get_table(table_ref)

    if table_exists and count > 0:
        generate_prompts(final_path)


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    main()
