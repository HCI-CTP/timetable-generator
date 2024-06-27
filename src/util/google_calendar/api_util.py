import os
import httplib2

from oauth2client.service_account import ServiceAccountCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource

# if modifying these scopes, delete the file token.json
# retrieve https://developers.google.com/calendar/api/auth

SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_KEY_FILE = './secrets/service-credentials.json'

def get_oauth2_creds() -> ServiceAccountCredentials:
    creds = None

    if os.path.exists(SERVICE_ACCOUNT_KEY_FILE):
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            filename=SERVICE_ACCOUNT_KEY_FILE,
            scopes=SCOPES,
        )
    
    return creds

def get_service() -> Resource:
    http_auth = get_oauth2_creds().authorize(httplib2.Http())
    return build("calendar", "v3", http=http_auth)