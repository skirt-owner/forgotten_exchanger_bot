from aiogram import types

from bot.keyboards.admin import AdminMenu
from bot.keyboards.user import UserMenu


async def start_admin(message: types.Message) -> None:
    text = "Hello, {}!".format(message.from_user.username or "Admin")
    await message.reply(text=text, reply_markup=AdminMenu())


async def start_user(message: types.Message) -> None:
    text = "Hello, {}!".format(message.from_user.username or "Anonymous")
    await message.reply(text=text, reply_markup=UserMenu())
