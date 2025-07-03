import asyncio
import os

from typing import Optional
from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, Channel, ChannelParticipantAdmin, ChannelParticipantCreator, InputUser
from telethon.errors import SessionPasswordNeededError, PasswordHashInvalidError

from app.schemas import TelegramUserInfo


async def get_admin_channels(client):
    me = await client.get_me()
    admin_channels = []

    async for dialog in client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            try:
                participant = await client(GetParticipantRequest(
                    channel=entity,
                    participant=InputUser(user_id=me.id, access_hash=me.access_hash)
                ))

                if isinstance(participant.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
                    admin_channels.append(entity.title)
            except Exception:
                continue

    return admin_channels


async def get_users_from_channel(client, title: str):
    dialogs = await client(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=100,
        hash=0
    ))
    for dialog in dialogs.chats:
        if isinstance(dialog, Channel) and dialog.title == title:
            users = []
            async for user in client.iter_participants(dialog, aggressive=True):
                users.append(TelegramUserInfo(
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    phone=user.phone
                ))

            return users

    raise ValueError(f"Канал '{title}' не найден.")


def get_session_path():
    session_dir = os.path.join(os.path.expanduser("~"), ".telegram_parser")
    os.makedirs(session_dir, exist_ok=True)

    if os.name == 'nt':
        os.system(f'attrib +h "{session_dir}"')

    return os.path.join(session_dir, "channel_parser")


async def auth_with_password(session_name, api_id, api_hash, phone, password, get_code_func, get_password_func):
    session_path = get_session_path()
    client = TelegramClient(session_path, api_id, api_hash)

    await client.connect()
    if not await client.is_user_authorized():
        print("🔐 Вход по номеру телефона...")
        await client.send_code_request(phone)
        code = get_code_func()

        try:
            await client.sign_in(phone, code)
        except SessionPasswordNeededError:
            if password is None:
                password = get_password_func()
            await client.sign_in(password=password)

    return client


async def parse_private_channel_users_iter(api_id, api_hash, phone, password, target_title: str, session='channel_parser'):
    client = await auth_with_password(session, api_id, api_hash, phone, password)

    dialogs = await client(GetDialogsRequest(
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
            async for user in client.iter_participants(dialog, aggressive=True):
                users.append(TelegramUserInfo(
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    phone=user.phone
                ))

            await client.disconnect()
            print(f"Загружено {len(users)} пользователей.")
            return users

    await client.disconnect()
    raise ValueError(f"Канал с названием '{target_title}' не найден среди доступных.")
