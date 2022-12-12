from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from bot.config import ADMINS_IDS
from bot.misc.types import ID


class AdminIdFilter(BoundFilter):
    key = "is_admin_id"

    def __init__(self):
        if ADMINS_IDS is not None:
            self.admins_ids = ADMINS_IDS
        else:
            self.admins_ids = []

    def check(self, message: types.Message):
        if ID(message.from_user.id) in self.admins_ids:
            return True
        return False
