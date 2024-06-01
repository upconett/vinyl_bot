import enum
from datetime import datetime, timedelta
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from .BaseModel import BaseModel


class SubType(enum.Enum):
    MONTH_1 = 'MONTH 1'
    MONTH_3 = 'MONTH 3'
    UNLIMITED = 'UNLIMITED'


class Subscription(BaseModel):
    __tablename__ = 'subscriptions'

    type: Mapped[SubType]
    expires_at: Mapped[datetime | None]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))

    def __init__(self, type: SubType):
        match type:
            case SubType.MONTH_1:
                expires_at = datetime.now() + timedelta(days=30)
                print('expires_at', expires_at.date())
            case SubType.MONTH_3:
                expires_at = datetime.now() + timedelta(days=90)
                print('expires_at', expires_at.date())
            case SubType.UNLIMITED:
                expires_at = None
                print('Never expires')

        self.type = type
        self.expires_at = expires_at
        
    def __repr__(self) -> str:
        return f'Subscription(id={self.id!r}, type={self.type.value}, expires={self.expires_at!r})'
