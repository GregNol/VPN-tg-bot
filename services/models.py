"""ORM-модели и функции маппинга в доменные сущности.

Содержит классы SQLAlchemy и методы:
- from_domain: создание ORM-модели из доменной сущности
- to_domain: преобразование ORM-модели в доменную запись (Record)
"""
from datetime import datetime
from typing import cast

from sqlalchemy import Boolean, Column, BigInteger, DateTime, String, Text, Enum, Integer

from base import Base
from core import domain


class BaseModel(Base):
    """Базовая ORM‑модель.

    Добавляет стандартные временные поля:
    - created_on: дата/время создания записи
    - updated_on: дата/время последнего обновления записи
    """
    __abstract__ = True

    created_on = Column(DateTime, default=datetime.now)
    updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class User(BaseModel):
    """ORM‑модель пользователя (таблица `users`).

    Поля:
    - tgid: Telegram ID пользователя
    - parent_id: реферальный/родительский ID (может отсутствовать)
    - username: Telegram username
    - name: отображаемое имя пользователя
    - balance: баланс в минимальных единицах (целое число)
    - trial: признак наличия пробного периода
    - expiry_time: срок окончания подписки/тарифа
    - cnt_friend: количество приглашённых друзей
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)

    tgid = Column(Integer, nullable=False)
    parent_id = Column(Integer, nullable=True, default=817866082)
    username = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    balance = Column(BigInteger, default=0)
    trial = Column(Boolean, default=False)
    expiry_time = Column(DateTime, nullable=True)
    cnt_friend = Column(Integer, default=0)

    @classmethod
    def from_domain(cls, user: "domain.User") -> "User":
        """Создать ORM‑модель пользователя из доменной сущности.

        Аргументы:
        - user: domain.User — пользователь без БД‑специфичных полей

        Возвращает:
        - User — ORM‑модель для сохранения в БД
        """
        return User(
            tgid=user.tgid,
            parent_id=user.parent_id,
            username=user.username,
            name=user.name,
            balance=user.balance,
            trial=user.trial,
            expiry_time=user.expiry_time,
            cnt_friend=user.cnt_friend,
        )

    def to_domain(self) -> "domain.UserRecord":
        """Преобразовать ORM‑модель в доменную запись пользователя.

        Возвращает:
        - domain.UserRecord — полная запись пользователя, как хранится/возвращается из БД
        """
        return domain.UserRecord(
            id=cast(int, self.id),
            tgid=cast(int, self.tgid),
            parent_id=cast(int | None, self.parent_id),
            username=cast(str, self.username),
            name=cast(str, self.name),
            balance=cast(int, self.balance),
            trial=cast(bool, self.trial),
            expiry_time=cast(datetime | None, self.expiry_time),
            cnt_friend=cast(int, self.cnt_friend),
            opened_at=cast(datetime | None, self.created_on),
            updated_on=cast(datetime | None, self.updated_on),
        )


class Payment(BaseModel):
    """ORM‑модель платежа (таблица `payments`).

    Поля:
    - user_id: идентификатор пользователя (FK на users.id)
    - amount: сумма платежа в минимальных единицах (целое число)
    - months: период подписки, enum domain.Months
    """
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    amount = Column(BigInteger, nullable=False)
    months = Enum(domain.Months)

    @classmethod
    def from_domain(cls, payment: "domain.Payment") -> "Payment":
        """Создать ORM‑модель платежа из доменной сущности.

        Аргументы:
        - payment: domain.Payment — платёж без БД‑специфичных полей

        Возвращает:
        - Payment — ORM‑модель для сохранения в БД
        """
        return Payment(
            user_id=payment.user_id,
            amount=payment.amount,
            months=payment.months,
        )

    def to_domain(self) -> "domain.PaymentRecord":
        """Преобразовать ORM‑модель в доменную запись платежа.

        Возвращает:
        - domain.PaymentRecord — полная запись платежа, как хранится/возвращается из БД
        """
        return domain.PaymentRecord(
            id=cast(int, self.id),
            user_id=cast(int, self.user_id),
            amount=cast(int, self.amount),
            months=cast(domain.Months, self.months),
            opened_at=cast(datetime | None, self.created_on),
            updated_on=cast(datetime | None, self.updated_on),
        )
