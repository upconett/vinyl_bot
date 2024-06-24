from aiogram.types import Message

from create_bot import admins


class AllowedUsers():
    """Проверяет есть ли пользователь в списке admins в config.yaml"""
    def __call__(self, message: Message) -> bool:
        if message.from_user.id in admins:
            return True
        return False
