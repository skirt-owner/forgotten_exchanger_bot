from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from bot.config import ADMINS_IDS
from bot.misc.types import ID


class AdminIdFilter(BoundFilter):
    key = "is_admin"

    def __init__(self, is_admin: bool):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        if ID(message.from_user.id) in ADMINS_IDS:
            return self.is_admin is True
        return self.is_admin is False
