import csv
from dataclasses import asdict
from typing import List

from app.schemas import TelegramUserInfo


def save_users_to_csv(users: List[TelegramUserInfo], filename: str = "channel_users.csv"):
    file_exists = False
    try:
        with open(filename, "r", encoding="utf-8") as f:
            file_exists = True
    except FileNotFoundError:
        pass

    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=asdict(users[0]).keys())
        if not file_exists:
            writer.writeheader()
        for user in users:
            writer.writerow(asdict(user))
