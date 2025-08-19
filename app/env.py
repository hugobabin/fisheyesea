from dotenv import get_key

ENV_PATH = "../.env"

def get_bigquery_api_key():
    return get_key(ENV_PATH, "BIGQUERY_API_KEY")
