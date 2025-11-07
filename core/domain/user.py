from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class User:
    """
    Модель пользователя для создания/изменения (без id и временных полей)
    """
    tgid: int
    parent_id: Optional[int]
    username: str
    name: str
    balance: int
    trial: bool
    expiry_time: Optional[datetime]
    cnt_friend: int


@dataclass(slots=True)
class UserRecord:
    """
    Полная запись пользователя, как хранится/возвращается из БД
    """
    id: int
    tgid: int
    parent_id: Optional[int]
    username: str
    name: str
    balance: int
    trial: bool
    expiry_time: Optional[datetime]
    cnt_friend: int
    opened_at: Optional[datetime]
    updated_on: Optional[datetime]
