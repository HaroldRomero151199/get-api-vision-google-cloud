import os
from google.oauth2 import service_account

def load_credentials():
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

    return service_account.Credentials.from_service_account_file(credentials_path)