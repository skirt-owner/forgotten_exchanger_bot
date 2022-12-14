from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

from bot.keyboards.callback import user_menu_callback, currency_menu_symbol_callback, currency_menu_page_callback
from bot.config import SYMBOLS

UserMenu = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [InlineKeyboardButton(text="Current currency rates", callback_data=user_menu_callback.new(option="1"))],
    [InlineKeyboardButton(text="Historical currency rates", callback_data=user_menu_callback.new(option="2"))],
    [InlineKeyboardButton(text="Currency statistics", callback_data=user_menu_callback.new(option="3"))],
    [InlineKeyboardButton(text="Calculate currency", callback_data=user_menu_callback.new(option="4"))],
    [InlineKeyboardButton(text="All currencies", callback_data=user_menu_callback.new(option="5"))]
])

BackMenu = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [InlineKeyboardButton(text="Cancel", callback_data="cancel")]
])


def generate_currencies_menu(symbols=SYMBOLS, page=0, to_remove="") -> InlineKeyboardMarkup:
    if page < 0:
        page = len(symbols) // 9 - 1
    if page * 9 >= len(symbols):
        page = 0

    keyboard = InlineKeyboardMarkup(row_width=3)
    for symbol in list(symbols.keys())[page * 9:page * 9 + 9]:
        if symbol == to_remove:
            continue
        else:
            keyboard.insert(
                InlineKeyboardButton(text=symbol, callback_data=currency_menu_symbol_callback.new(symbol=symbol)))
    keyboard.add(InlineKeyboardButton(text="<-", callback_data=currency_menu_page_callback.new(page=str(page - 1))))
    keyboard.insert(InlineKeyboardButton(text="->", callback_data=currency_menu_page_callback.new(page=str(page + 1))))
    keyboard.add(InlineKeyboardButton(text="Cancel", callback_data="cancel"))

    return keyboard
