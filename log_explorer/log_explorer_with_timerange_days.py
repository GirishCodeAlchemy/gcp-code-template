import re
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import plotly.graph_objects as go
from google.cloud import logging
from tabulate import tabulate


class LogAnalyzer:
    def __init__(self, project_id, filter_str):
        self.project_id = project_id
        self.filter_str = filter_str

    def display_dict_as_table(self, data):
        """Prints a dictionary in a table format using the tabulate library."""
        table_data = [[key, value] for key, value in data.items()]
        print(tabulate(table_data, headers=["ClubId", "MismatchCount"]))

    def display_dict_as_bargrap_using_matplotlib(self, data, time_range):
        """Displays a bar graph from the dictionary using matplotlib."""
        plt.barh(list(data.keys()), list(data.values()))
        plt.xlabel('MismatchCount')
        plt.ylabel('ClubId')
        plt.title(f'Mismatch Count for Each ClubId\n{time_range}')
        plt.show()

    def display_dict_as_bargraph(self, data, time_range):
        """Displays a bar graph from the dictionary and saves it as an HTML file."""
        fig = go.Figure(go.Bar(
            x=list(data.values()),
            y=list(data.keys()),
            orientation='h'
        ))

        fig.update_layout(
            title={
                'text': 'Mismatch Count for Each ClubId',
                'x': 0.5,
                'y': 0.95,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title='MismatchCount',
            yaxis_title='ClubId',
            hovermode='y',
            annotations=[dict(
                x=0.5,
                y=-0.1,
                xref='paper',
                yref='paper',
                text=f'{time_range}',
                showarrow=False,
                font=dict(
                    size=10,
                    color='black'
                )
            )]
        )
        fig.write_image("mismatch_count.png")
        fig.write_html("mismatch_count.html")
        # fig.show()

    def fetch_logs(self, num_days=None):
        client = logging.Client(project=self.project_id)
        filter_str = self.filter_str

        if num_days is not None:
            end_timestamp = datetime.utcnow()
            start_timestamp = end_timestamp - timedelta(days=num_days)
            start_timestamp_str = start_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
            end_timestamp_str = end_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
            filter_str += f' timestamp>="{start_timestamp_str}" timestamp<="{end_timestamp_str}"'

        entries = client.list_entries(filter_=filter_str)
        mismatch_sum = 0
        earliest_timestamp = None
        latest_timestamp = None
        club_mismatch_dict = {}

        for entry in entries:
            timestamp = entry.timestamp
            message = entry.payload['message']

            if earliest_timestamp is None or timestamp < earliest_timestamp:
                earliest_timestamp = timestamp
            if latest_timestamp is None or timestamp > latest_timestamp:
                latest_timestamp = timestamp

            match = re.search(r'ClubId: (\d+).*?Count of mismatch records is(\d+)', message)
            if match:
                club_id = match.group(1)
                mismatch_count = int(match.group(2))
                mismatch_sum += mismatch_count
                club_mismatch_dict.setdefault(club_id, 0)
                club_mismatch_dict[club_id] += mismatch_count

        if earliest_timestamp and latest_timestamp:
            time_range = f"Time Range: {earliest_timestamp} to {latest_timestamp}"
        else:
            time_range = "Time range not specified."

        if mismatch_sum > 0:
            print(f"\nTotal Mismatch Count: {mismatch_sum}")
            print(time_range)
            self.display_dict_as_table(club_mismatch_dict)
            self.display_dict_as_bargraph(club_mismatch_dict, time_range)
        else:
            print("\nNo logs found with mismatch records.")


if __name__ == "__main__":
    project_id = 'girish-dev'
    filter_str = 'resource.type="cloud_dataproc_cluster" "Count of mismatch records is"'
    log_analyzer = LogAnalyzer(project_id, filter_str)

    num_days = 2  # Number of days for the time range
    log_analyzer.fetch_logs(num_days)
