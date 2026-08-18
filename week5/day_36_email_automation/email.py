from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from anthropic import Anthropic
from dotenv import load_dotenv
import os
import base64
import pickle

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

def get_gmail_service():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as f:
            pickle.dump(creds, f)

    return build('gmail', 'v1', credentials=creds)


def get_emails(service, max_results=5):
    results = service.users().messages().list(
        userId='me',
        maxResults=max_results,
        labelIds=['INBOX']
    ).execute()

    messages = results.get('messages', [])
    emails = []

    for msg in messages:
        txt = service.users().messages().get(
            userId='me',
            id=msg['id']
        ).execute()

        payload = txt['payload']
        headers = payload['headers']

        subject = ""
        sender = ""
        for h in headers:
            if h['name'] == 'Subject':
                subject = h['value']
            if h['name'] == 'From':
                sender = h['value']

        # Body বের করো
        body = ""
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
        elif 'body' in payload:
            data = payload['body'].get('data', '')
            if data:
                body = base64.urlsafe_b64decode(data).decode('utf-8')

        emails.append({
            'id': msg['id'],
            'subject': subject,
            'sender': sender,
            'body': body[:500]
        })

    return emails