from aiogram import Dispatcher

from bot.config import PREFIXES
from bot.handlers.start import start_admin, start_user
from bot.handlers.user import menu_option_1

from bot.keyboards.callback import user_menu_callback


async def register_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(callback=start_admin, is_admin_id=True, commands=["start"], prefixes=PREFIXES)
    dp.register_message_handler(callback=start_user, commands=["start"], prefixes=PREFIXES)
    dp.register_callback_query_handler(user_menu_callback.filter(option=1))
