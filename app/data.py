from google.cloud import bigquery
from models import FishingEffort
from typing import List

GFW_DATASET = "global-fishing-watch.fishing_effort_v3"

def get_gfw_fishing_efforts() -> List[FishingEffort]:
    """
    Get the fishing efforts from Global Fishing Watch through their
    public BigQuery dataset.
    """

    results = []

    # Initialize BigQuery client
    client = bigquery.Client()

    # Initialize the query
    query = "SELECT * FROM {GFW_DATASET}"

    # Execute the query and retrieve results
    query_job = client.query(query)

    # Loop through results and validate each
    for fishing_effort in query_job:
        results.append(FishingEffort.model_validate(fishing_effort))

    return results