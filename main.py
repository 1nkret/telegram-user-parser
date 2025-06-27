import csv
from dataclasses import dataclass, asdict
from typing import Optional, List
from dotenv import load_dotenv
from os import getenv

from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import Channel, InputPeerEmpty


@dataclass
class TelegramChannelInfo:
    title: Optional[str]
    username: Optional[str]
    id: Optional[int]
    about: Optional[str]
    participants_count: Optional[int]


@dataclass
class TelegramUserInfo:
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]


def auth_with_password(session_name: str, api_id: int, api_hash: str, phone: str, password: Optional[str] = None):
    client = TelegramClient(session_name, api_id, api_hash)
    client.connect()

    if not client.is_user_authorized():
        print("🔐 Вход по номеру телефона...")
        client.send_code_request(phone)
        code = input("Введите код из Telegram: ")
        try:
            client.sign_in(phone, code)
        except SessionPasswordNeededError:
            if password is None:
                raise ValueError("Требуется пароль двухфакторной аутентификации, но пароль не передан.")
            print("⚠️ Требуется пароль двухфакторной авторизации.")
            client.sign_in(password=password)

    return client


def parse_private_channel_users_iter(api_id, api_hash, phone, password, target_title: str, session='channel_parser'):
    client = auth_with_password(session, api_id, api_hash, phone, password)

    dialogs = client(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=200,
        hash=0
    ))

    for dialog in dialogs.chats:
        if isinstance(dialog, Channel) and dialog.title == target_title:
            print(f"Сбор участников канала '{dialog.title}' через iter_participants...")
            users = []
            for user in client.iter_participants(dialog, aggressive=True):
                users.append(TelegramUserInfo(
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    phone=user.phone
                ))

            client.disconnect()
            print(f"Загружено {len(users)} пользователей.")
            return users

    client.disconnect()
    raise ValueError(f"Канал с названием '{target_title}' не найден среди доступных.")


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


load_dotenv()

API_ID = int(getenv("api_id"))
API_HASH = getenv("api_hash")
SESSION = 'session'

PHONE = getenv("phone")
PASSWORD = getenv("password")
target_channel = getenv("target_channel")

users = parse_private_channel_users_iter(
    api_id=API_ID,
    api_hash=API_HASH,
    phone=PHONE,
    password=PASSWORD,
    target_title=target_channel
)
save_users_to_csv(users)
print(f"✅ Сохранено {len(users)} пользователей.")
