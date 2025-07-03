from dataclasses import dataclass
from typing import Optional


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
