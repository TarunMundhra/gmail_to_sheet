from gmail_service import (
    get_gmail_service,
    fetch_unread_messages,
    get_message_details,
    mark_as_read,
)
from email_parser import parse_email
from state_manager import load_state, save_state
from sheets_service import append_row

# TODO: replace with your actual Spreadsheet ID and Sheet name
SPREADSHEET_ID = "16VAGHcDsRclIk6mbDmPcF_0ZQ40ApFa9-puYs6fkUoc"
SHEET_NAME = "Sheet1"


def main():
    gmail_service = get_gmail_service()
    processed_ids = load_state()

    messages = fetch_unread_messages(gmail_service)

    if not messages:
        print("No unread emails found.")
        return

    new_count = 0

    for msg in messages:
        msg_id = msg["id"]

        if msg_id in processed_ids:
            continue

        full_message = get_message_details(gmail_service, msg_id)
        email_data = parse_email(full_message)

        row = [
            email_data["from"],
            email_data["subject"],
            email_data["date"],
            email_data["content"],
        ]

        append_row(SPREADSHEET_ID, SHEET_NAME, row)

        mark_as_read(gmail_service, msg_id)
        processed_ids.add(msg_id)
        new_count += 1

    save_state(processed_ids)
    print(f"Processed {new_count} new emails.")


if __name__ == "__main__":
    main()
