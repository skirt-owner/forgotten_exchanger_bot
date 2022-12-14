import re

from typing import Union
from aiogram import types
from datetime import datetime

from aiogram.dispatcher import FSMContext

from bot.keyboards.user import BackMenu, UserMenu, generate_currencies_menu
from bot.misc.states import Option1, Option2, Option3, Option4, Option5
from bot.misc.api import get_currency, get_historical_currency, get_stat_image, calculate_currency, get_symbol_full_name


async def cancel(obj: Union[types.Message, types.CallbackQuery], state: FSMContext) -> None:
    state_status = await state.get_state()
    if state_status is not None:
        await state.finish()

    if isinstance(obj, types.CallbackQuery):
        await obj.answer()
        obj = obj.message
    text = "Hello, {}!".format(obj.from_user.username or "Anonymous")
    try:
        await obj.edit_text(text=text, reply_markup=UserMenu)
    except:
        await obj.answer(text, reply_markup=UserMenu)
        await obj.edit_reply_markup()


async def option1(query: types.CallbackQuery, callback_data: dict) -> None:
    await query.answer()

    keyboard = generate_currencies_menu()
    await query.message.edit_text(text="Choose _from_ currency:", reply_markup=keyboard)
    await Option1.from_currency.set()


async def change_page(query: types.CallbackQuery, callback_data: dict, state: FSMContext) -> None:
    await query.answer()

    page = int(callback_data["page"])
    state_data = await state.get_data()

    await state.update_data(page=page)

    if "to_remove" in list(state_data.keys()):
        to_remove = state_data["to_remove"]
    else:
        to_remove = ""

    keyboard = generate_currencies_menu(page=page, to_remove=to_remove)
    await query.message.edit_reply_markup(reply_markup=keyboard)


async def choose_symbol(query: types.CallbackQuery, callback_data: dict, state: FSMContext) -> None:
    await query.answer()

    state_data = await state.get_data(default=str)
    state_name = (await state.get_state(default=str)).split(":")

    if "_from_" not in list(state_data.keys()):
        await state.update_data(_from_=callback_data["symbol"])
        await state.update_data(to_remove=callback_data["symbol"])
        if "page" not in list(state_data.keys()):
            page = 0
        else:
            page = state_data["page"]

        keyboard = generate_currencies_menu(page=page, to_remove=callback_data["symbol"])
        await query.message.edit_reply_markup(reply_markup=keyboard)

        await query.message.edit_text("Choose _to_ currency:", reply_markup=keyboard)
        if state_name[0] == "Option1":
            await Option1.to_currency.set()
        elif state_name[0] == "Option2":
            await Option2.to_currency.set()
        elif state_name[0] == "Option3":
            await Option3.to_currency.set()
        elif state_name[0] == "Option4":
            await Option4.to_currency.set()
    else:
        _from_ = state_data["_from_"]
        _to_ = callback_data["symbol"]
        if state_name[0] == "Option1":
            date, rate = await get_currency(_from_, _to_)
            await query.message.edit_text(text=f"Date: {date}\nPair: {_from_}{_to_}\nRate: {rate}",
                                          reply_markup=BackMenu)
            await state.finish()
        elif state_name[0] == "Option2":
            await state.update_data(_to_=_to_)
            await state.update_data(message_to_remove=query.message)

            await query.message.edit_text(text=f"Send me the date (YYYY-MM-DD), no earlier than 2000, for the pair "
                                               f"{_from_}{_to_}.", reply_markup=BackMenu)
            await Option2.date.set()
        elif state_name[0] == "Option3":
            await state.update_data(_to_=_to_)
            await state.update_data(message_to_remove=query.message)

            await query.message.edit_text(text=f"Send me start-date (YYYY-MM-DD), no earlier than 2000, for the pair "
                                               f"{_from_}{_to_}.", reply_markup=BackMenu)
            await Option3.start_date.set()
        elif state_name[0] == "Option4":
            await state.update_data(_to_=_to_)
            await state.update_data(message_to_remove=query.message)

            await query.message.edit_text(text=f"Send me amount of {_from_}.", reply_markup=BackMenu)
            await Option4.amount.set()


async def option2(query: types.CallbackQuery, callback_data: dict) -> None:
    await query.answer()
    keyboard = generate_currencies_menu()
    await query.message.edit_text(text="Choose _from_ currency:", reply_markup=keyboard)
    await Option2.from_currency.set()


async def get_start_date(message: types.Message, state: FSMContext) -> None:
    state_data = await state.get_data(default=str)

    message_to_remove = state_data["message_to_remove"]
    if message_to_remove != "":
        await message_to_remove.edit_reply_markup()
        await state.update_data(message_to_remove="")

    _from_, _to_ = state_data["_from_"], state_data["_to_"]
    start_date = message.text

    state_name = (await state.get_state(default=str)).split(":")
    if state_name[0] == "Option2":
        check_date = re.match(r"^(20\d\d)-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])$", start_date)
        if check_date is not None:
            rate = await get_historical_currency(_from_, _to_, start_date)
            await message.answer(text=f"Date: {start_date}\nPair: {_from_}{_to_}\nRate: {rate}", reply_markup=BackMenu)
            await state.finish()
        else:
            await state.update_data(message_to_remove=message)
            message_to_remove = await message.reply("Send me correct date (YYYY-MM-DD), no earlier than 1999!",
                                                    reply_markup=BackMenu)
            await state.update_data(message_to_remove=message_to_remove)
    elif state_name[0] == "Option3":
        check_date = re.match(r"^(20\d\d)-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])$", start_date)
        if check_date is not None:
            await state.update_data(start_date=start_date)

            message_to_remove = await message.answer(text=f"Send me end-date (YYYY-MM-DD), no earlier than 2000, "
                                                          f"for the pair {_from_}{_to_}.", reply_markup=BackMenu)
            await state.update_data(message_to_remove=message_to_remove)
            await Option3.end_date.set()
        else:
            await state.update_data(message_to_remove=message)
            message_to_remove = await message.reply("Send me correct start-date (YYYY-MM-DD), no earlier than 1999!",
                                                    reply_markup=BackMenu)
            await state.update_data(message_to_remove=message_to_remove)


async def option3(query: types.CallbackQuery, callback_data: dict) -> None:
    await query.answer()
    keyboard = generate_currencies_menu()
    await query.message.edit_text(text="Choose _from_ currency:", reply_markup=keyboard)
    await Option3.from_currency.set()


async def get_end_date(message: types.Message, state: FSMContext) -> None:
    state_data = await state.get_data(default=str)

    message_to_remove = state_data["message_to_remove"]
    if message_to_remove != "":
        await message_to_remove.edit_reply_markup()
        await state.update_data(message_to_remove="")

    _from_, _to_, start_date = state_data["_from_"], state_data["_to_"], state_data["start_date"]
    end_date = message.text

    state_name = (await state.get_state(default=str)).split(":")
    if state_name[0] == "Option3":
        check_date = re.match(r"^(20\d\d)-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])$", end_date)
        d1 = datetime.strptime(start_date, "%Y-%m-%d")
        d2 = datetime.strptime(end_date, "%Y-%m-%d")
        if (check_date is not None) and (d2 > d1):
            stat_image = await get_stat_image(_from_, _to_, start_date, end_date)
            stat_image.seek(0)
            stat_image = types.InputFile(stat_image)
            await message.answer_photo(photo=stat_image, reply_markup=BackMenu)
            await state.finish()
        else:
            await state.update_data(message_to_remove=message)
            message_to_remove = await message.reply("Send me correct end-date (YYYY-MM-DD), no earlier than 2000 and "
                                                    "bigger than start-date!!",
                                                    reply_markup=BackMenu)
            await state.update_data(message_to_remove=message_to_remove)


async def option4(query: types.CallbackQuery, callback_data: dict) -> None:
    await query.answer()
    keyboard = generate_currencies_menu()
    await query.message.edit_text(text="Choose _from_ currency:", reply_markup=keyboard)
    await Option4.from_currency.set()


def is_float(s: str):
    try:
        float(s)
        return True
    except:
        return False


async def get_amount(message: types.Message, state: FSMContext) -> None:
    state_data = await state.get_data(default=str)

    message_to_remove = state_data["message_to_remove"]
    if message_to_remove != "":
        await message_to_remove.edit_reply_markup()
        await state.update_data(message_to_remove="")

    _from_, _to_ = state_data["_from_"], state_data["_to_"]
    amount = message.text
    if is_float(amount):
        date, result = await calculate_currency(_from_, _to_, amount)
        await message.answer(text=f"{amount} of {_from_} = {result} of {_to_} by date of {date}.",
                             reply_markup=BackMenu)
    else:
        message_to_remove = await message.reply(text=f"Send me correct amount of {_from_}!", reply_markup=BackMenu)
        await state.update_data(message_to_remove=message_to_remove)


async def option5(query: types.CallbackQuery, callback_data: dict) -> None:
    await query.answer()
    keyboard = generate_currencies_menu()
    await query.message.edit_text(text="Choose currency:", reply_markup=keyboard)
    await Option5.currency.set()


async def get_full_name(query: types.CallbackQuery, callback_data: dict, state: FSMContext) -> None:
    await query.answer()
    symbol = callback_data["symbol"]
    symbol_full_name = get_symbol_full_name(symbol)
    await query.message.edit_text(text=f"{symbol} - {symbol_full_name}", reply_markup=BackMenu)
    await state.finish()
