# Gmail to Google Sheets Automation

**Name:** Tarun Mundhra

---

## Project Overview

This project is a Python automation system that reads real incoming emails from a Gmail account and logs them into a Google Sheet using official Google APIs.

The system connects to:
- Gmail API
- Google Sheets API

Only unread emails from the inbox are processed. Each qualifying email is appended as a new row in a Google Sheet.

---

## Objective

For every qualifying email, the following details are stored in Google Sheets:

| Column | Description |
|------|------------|
| From | Sender email address |
| Subject | Email subject |
| Date | Date and time received |
| Content | Plain text email body |

---

## High-Level Architecture

The system works as follows:

1. User authenticates using OAuth 2.0
2. Gmail API fetches unread inbox emails
3. Email content is parsed into structured fields
4. Google Sheets API appends the data as new rows
5. State is stored locally to avoid duplicate processing

(Architecture diagram provided separately as a hand-drawn image)

---

## Project Structure

gmail-to-sheets/
│
├── src/
│ ├── gmail_service.py
│ ├── sheets_service.py
│ ├── email_parser.py
│ └── main.py
│
├── credentials/
│ └── credentials.json (not committed)
│
├── config.py
├── requirements.txt
├── .gitignore
└── README.md


---

## Setup Instructions

### 1. Clone the repository
```bash
git clone <repository_url>
cd gmail-to-sheets
python -m venv venv
