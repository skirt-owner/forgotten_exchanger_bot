from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

from bot.keyboards.callback import user_menu_callback, symbol_pair_callback, page_callback
from bot.config import SYMBOLS

UserMenu = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [InlineKeyboardButton(text="Currency pair rates", callback_data=user_menu_callback.new(option="1"))],
    [InlineKeyboardButton(text="Calculate currency", callback_data=user_menu_callback.new(option="2"))]
])

BackMenu = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [InlineKeyboardButton(text="Cancel", callback_data="cancel")]
])


def get_symbols_menu(symbols=SYMBOLS, page=0, to_symbol="") -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=3)
    if (page < 0) or (page*9 >= len(symbols)):
        page = 0
    for symbol in list(symbols.keys())[page*9:page*9+9]:
        button = InlineKeyboardButton(text=symbol, callback_data=symbol_pair_callback.new(pair=symbol+to_symbol))
        keyboard.insert(button)
    keyboard.insert(InlineKeyboardButton(text="<-", callback_data=page_callback.new(page=str(page-1))))
    keyboard.insert(InlineKeyboardButton(text="->", callback_data=page_callback.new(page=str(page+1))))
    keyboard.add(InlineKeyboardButton(text="Cancel", callback_data="cancel"))
    return keyboard
