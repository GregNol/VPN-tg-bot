from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .month import Months


@dataclass(slots=True)
class Payment:
    """
    Модель платежа для создания (без id и временных полей)
    """
    user_id: int
    amount: int
    months: Months


@dataclass(slots=True)
class PaymentRecord:
    """
    Полная запись о платеже из БД
    """
    id: int
    user_id: int
    amount: int
    months: Months
    opened_at: Optional[datetime]
    updated_on: Optional[datetime]
