import requests

from aiogram import types

from bot.keyboards.user import get_symbols_menu, BackMenu


async def menu_option_1(query: types.CallbackQuery, callback_data: dict) -> None:
    await query.answer()
    await query.message.edit_text(text="Pick <FROM> currency:", reply_markup=get_symbols_menu())


async def change_page(query: types.CallbackQuery, callback_data: dict) -> None:
    await query.answer()
    new_page = int(callback_data["page"])
    await query.message.edit_reply_markup(reply_markup=get_symbols_menu(page=new_page))


async def pick_symbol(query: types.CallbackQuery, callback_data: dict) -> None:
    await query.answer()
    pair = callback_data["pair"]
    if len(pair) > 3:
        url = f"https://api.exchangerate.host/convert?from={pair[:3]}&to={pair[3:]}"
        response = requests.get(url)
        data = response.json()
        date = data["date"]
        rate = data["result"]
        await query.message.edit_text(text=f"Pair: {pair}\nDate: {date}\nRate: {rate}", reply_markup=BackMenu)
    else:
        await query.message.edit_text(text="Pick <TO> currency:", reply_markup=get_symbols_menu())
