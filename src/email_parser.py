import base64


def parse_email(message):
    """
    Extract sender, subject, date, and plain text body from Gmail message.
    """
    payload = message.get("payload", {})
    headers = payload.get("headers", [])

    email_data = {
        "from": "",
        "subject": "",
        "date": "",
        "content": ""
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
    def extract_body(parts):
        for part in parts:
            if part.get("mimeType") == "text/plain":
                data = part.get("body", {}).get("data")
                if data:
                    return base64.urlsafe_b64decode(data).decode("utf-8")

            # Handle nested parts
            if part.get("parts"):
                result = extract_body(part.get("parts"))
                if result:
                    return result
        return ""

    parts = payload.get("parts", [])
    email_data["content"] = extract_body(parts)

    return email_data
