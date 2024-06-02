from dataclasses import dataclass
from datetime import datetime

from database.models.Subscription import SubType
from database.models import Subscription


@dataclass
class ProfileData:
    subscribed: bool
    subscription_type: SubType
    expires_at: datetime
    free_vinyl: int
    free_albums: int

    def __init__(self, subscription: Subscription, free_vinyl: int, free_albums: int):
        self.subscribed = True if subscription else False
        self.subscription_type = None if not subscription else subscription.type
        self.expires_at = None if not subscription else subscription.expires_at.strftime('%d.%m.%Y')
        self.free_vinyl = free_vinyl
        self.free_albums = free_albums
