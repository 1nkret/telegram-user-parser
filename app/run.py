import asyncio
from app.save_csv import save_users_to_csv
from app.telegram import parse_private_channel_users_iter


def run_parser(api_id, api_hash, phone, password, target_channel):
    users = asyncio.run(parse_private_channel_users_iter(
        api_id=api_id,
        api_hash=api_hash,
        phone=phone,
        password=password,
        target_title=target_channel
    ))
    save_users_to_csv(users)
    print(f"✅ Сохранено {len(users)} пользователей.")
