import re

from google.cloud import logging


def fetch_and_display_logs(project_id, filter_str):
    # Initialize a client
    client = logging.Client(project=project_id)

    # Fetch logs using the specified filter
    entries = client.list_entries(filter_=filter_str)

    # Display fetched logs
    for entry in entries:
        # print(f"Log Name: {entry.log_name}, Timestamp: {entry.timestamp}, Message: {entry.payload}")
        match = re.search(r'id: (\d+).*?Count of mismatch records is(\d+)', entry.payload['message'])
        if match:
            id = match.group(1)
            mismatch_count = match.group(2)
            print(f"Id: {id}, Mismatch Count: {mismatch_count}")


if __name__ == "__main__":
    # Replace 'your-project-id' with your GCP project ID
    project_id = 'girish-dev'

    # Replace 'your-filter-string' with the filter string you want to apply
    filter_str = 'resource.type="cloud_dataproc_cluster" "Count of mismatch records is"'

    # Fetch and display logs
    fetch_and_display_logs(project_id, filter_str)
