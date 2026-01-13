import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scope required to read emails and mark them as read
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

TOKEN_PATH = "token.json"
CREDENTIALS_PATH = "credentials/credentials.json"


def get_gmail_service():
    creds = None

    # Load existing token if available
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    # If no valid credentials, perform OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save token for future runs
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    return service


def fetch_unread_messages(service, max_results=10):
    """
    Fetch unread emails from inbox
    """
    response = service.users().messages().list(
        userId="me",
        labelIds=["INBOX", "UNREAD"],
        maxResults=max_results
    ).execute()

    messages = response.get("messages", [])
    return messages


def get_message_details(service, message_id):
    """
    Fetch full message details for a given message ID
    """
    message = service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()

    payload = message.get("payload", {})
    headers = payload.get("headers", [])

    email_data = {
        "from": "",
        "subject": "",
        "date": "",
        "body": ""
    }

    for header in headers:
        name = header.get("name")
        value = header.get("value")

        if name == "From":
            email_data["from"] = value
        elif name == "Subject":
            email_data["subject"] = value
        elif name == "Date":
            email_data["date"] = value

    # Extract plain text body
    parts = payload.get("parts", [])
    for part in parts:
        if part.get("mimeType") == "text/plain":
            data = part.get("body", {}).get("data")
            if data:
                email_data["body"] = base64.urlsafe_b64decode(data).decode("utf-8")
                break

    return email_data


def mark_as_read(service, message_id):
    """
    Mark email as read
    """
    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={"removeLabelIds": ["UNREAD"]}
    ).execute()
