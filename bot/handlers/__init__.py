from aiogram import Dispatcher

from bot.config import PREFIXES
from bot.handlers.start import start_admin, start_user


async def register_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(callback=start_admin, is_admin_id=True, commands=["start"], prefixes=PREFIXES)
    dp.register_message_handler(callback=start_user,  commands=["start"], prefixes=PREFIXES)

