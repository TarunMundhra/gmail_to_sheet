import json
import os

STATE_FILE = "processed_state.json"


def load_state():
    """
    Load processed Gmail message IDs from local state file.
    Returns a set of message IDs.
    """
    if not os.path.exists(STATE_FILE):
        return set()

    with open(STATE_FILE, "r") as f:
        data = json.load(f)

    return set(data.get("processed_message_ids", []))


def save_state(processed_ids):
    """
    Save processed Gmail message IDs to local state file.
    """
    with open(STATE_FILE, "w") as f:
        json.dump(
            {"processed_message_ids": list(processed_ids)},
            f,
            indent=2
        )
