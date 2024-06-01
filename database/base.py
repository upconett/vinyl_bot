from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .models import Base, User, Subscription
from .models.Subscription import SubType


engine = create_engine("sqlite:///:memory:", echo=True)

