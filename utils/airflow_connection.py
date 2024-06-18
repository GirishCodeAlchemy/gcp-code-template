import json

from airflow.models import Connection
from google.oauth2 import service_account
from utils.logging import get_logging_client

logger = get_logging_client()


def get_google_cloud_credentials(connection_id):
    logger.info(f"Fetching google credentails from Connection ID- {connection_id}")
    conn = Connection.get_connection_from_secrets(connection_id)
    key_json = json.loads(conn.extra_dejson['keyfile_dict'])
    credentials = service_account.Credentials.from_service_account_info(
        key_json)
    return credentials
