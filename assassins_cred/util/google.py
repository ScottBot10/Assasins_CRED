import json
import os

from google.auth.transport.requests import Request as _Request
from google.oauth2.credentials import Credentials as _Credentials
from google_auth_oauthlib.flow import InstalledAppFlow as _InstalledAppFlow

from assassins_cred import config as _config


_SCOPES = ['https://www.googleapis.com/auth/contacts.readonly',
           'https://www.googleapis.com/auth/directory.readonly',
           'https://www.googleapis.com/auth/spreadsheets.readonly']


def create_token(creds_file: str = _config.io.forms.creds_file,
                 token_file: str = _config.io.forms.token_file,
                 scopes=None) -> _Credentials:
    if scopes is None:
        scopes = _SCOPES
    else:
        scopes = list(set(scopes) | set(_SCOPES))
    creds = None
    if os.path.exists(token_file):
        with open(token_file) as f:
            js = json.load(f)
        if all(scope in js['scopes'] for scope in scopes):
            creds = _Credentials.from_authorized_user_file(token_file, scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(_Request())
        else:
            flow = _InstalledAppFlow.from_client_secrets_file(
                creds_file, scopes)
            creds = flow.run_local_server(port=0)
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    return creds
