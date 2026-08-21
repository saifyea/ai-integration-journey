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

flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json',  # same folder এ থাকলে এটাই যথেষ্ট
    SCOPES
)

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


def get_emails(service, max_results=10):
    results = service.users().messages().list(
        userId='me',
        maxResults=max_results,
        # ✅ no-reply বাদ দাও
        q="NOT from:no-reply NOT from:noreply NOT from:notifications"
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

        # no-reply skip করো
        if any(x in sender.lower() for x in
               ['no-reply', 'noreply', 'notification']):
            continue

        # Body বের করো
        body = ""
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data', '')
                    if data:
                        body = base64.urlsafe_b64decode(
                            data
                        ).decode('utf-8')
        elif 'body' in payload:
            data = payload['body'].get('data', '')
            if data:
                body = base64.urlsafe_b64decode(
                    data
                ).decode('utf-8')

        emails.append({
            'id': msg['id'],
            'subject': subject,
            'sender': sender,
            'body': body[:500]
        })

    print(f"✅ Real emails found: {len(emails)}")
    return emails

def categorize_email(email):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        system="""Email categorize করো।
শুধু একটা category দাও:
ORDER, COMPLAINT, INQUIRY, SPAM, OTHER""",
        messages=[{
            "role": "user",
            "content": f"""
Subject: {email['subject']}
From: {email['sender']}
Body: {email['body'][:200]}

Category:"""
        }]
    )
    return response.content[0].text.strip()


def generate_reply(email, category):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        system="""তুমি Saif's Kids Store এর customer service।
Professional email reply লেখো।

Store Info:
- Products: Map Puzzle ৳450, Drawing Board ৳350, Flash Cards ৳250
- Delivery: ঢাকায় ১-২ দিন, বাইরে ৩-৫ দিন
- Return: ৭ দিন""",
        messages=[{
            "role": "user",
            "content": f"""
Email থেকে reply দাও:
Subject: {email['subject']}
From: {email['sender']}
Body: {email['body'][:300]}
Category: {category}

Professional reply লেখো:"""
        }]
    )
    return response.content[0].text


# Main Program
def main():
    print("📧 Gmail AI Assistant চালু!")

    service = get_gmail_service()
    print("✅ Gmail connected!")

    emails = get_emails(service, max_results=5)
    print(f"✅ {len(emails)} emails found!")

    for i, email in enumerate(emails, 1):
        print(f"\n{'='*50}")
        print(f"Email {i}:")
        print(f"From: {email['sender']}")
        print(f"Subject: {email['subject']}")

        category = categorize_email(email)
        print(f"Category: {category}")

        if category in ["ORDER", "INQUIRY", "COMPLAINT"]:
            reply = generate_reply(email, category)
            print(f"\nAI Reply:\n{reply}")

main()