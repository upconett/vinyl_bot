import enum
from datetime import datetime, timedelta
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from .BaseModel import BaseModel


class SubType(enum.Enum):
    MONTH_1 = 'MONTH 1'
    MONTH_6 = 'MONTH 6'
    MONTH_12 = 'MONTH 12'
    MONTH_6 = 'MONTH 6'
    MONTH_12 = 'MONTH 12'


class Subscription(BaseModel):
    __tablename__ = 'subscriptions'

    id: Mapped[int] = mapped_column(unique=True, primary_key=True, autoincrement=True)
    type: Mapped[SubType]
    expires_at: Mapped[datetime | None]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    def __init__(self, type: SubType):
        super().__init__()
        super().__init__()
        match type:
            case SubType.MONTH_1:
                expires_at = datetime.now() + timedelta(days=31)
            case SubType.MONTH_6:
                expires_at = datetime.now() + timedelta(days=183)
            case SubType.MONTH_12:
                expires_at = datetime.now() + timedelta(days=365)
                expires_at = datetime.now() + timedelta(days=31)
            case SubType.MONTH_6:
                expires_at = datetime.now() + timedelta(days=183)
            case SubType.MONTH_12:
                expires_at = datetime.now() + timedelta(days=365)

        self.type = type
        self.expires_at = expires_at
        
    def __repr__(self) -> str:
        return f'Subscription(id={self.id!r}, type={self.type.value}, expires={self.expires_at!r}, created_at={self.created_at})'
