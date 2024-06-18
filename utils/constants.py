from enum import Enum


class CONSTANT:
    PROJECT_ID = 'girish-dev'
    TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
    GCP_CREDENTIALS_CATALOG_DEV = 'gcp_girish-dev_cred'


class MismatchReport:
    TIMEFRAME_HOURS = "MISMATCH_REPORT_TIMEFRAME_HOURS"
    SENDER_EMAIL = "MISMATCH_SENDER_EMAIL"
    RECIPIENT_EMAIL = "MISMATCH_RECIPIENT_EMAIL"
    DEFAULT_EMAIL = "Girish.Venkatareddy@gmail.com"
    DAG_ID = "mismatch_report"


class ScheduleDag(Enum):
    mismatch_report = "0 7 * * *"