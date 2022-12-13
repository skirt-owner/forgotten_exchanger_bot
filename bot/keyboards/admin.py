from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

from bot.keyboards.callback import admin_menu_callback


AdminMenu = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [InlineKeyboardButton(text="Send notification", callback_data=admin_menu_callback.new(option="1"))],
    [InlineKeyboardButton(text="Block user", callback_data=admin_menu_callback.new(option="2"))]
])
