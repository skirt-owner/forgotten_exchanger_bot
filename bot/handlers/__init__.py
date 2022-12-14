from aiogram import Dispatcher

from bot.handlers.start import start_admin, start_user
from bot.handlers.user import cancel, option1, change_page, choose_symbol, option2, get_start_date, option3, \
                                get_end_date, option4, get_amount, option5, get_full_name
from bot.keyboards.callback import cancel_callback, user_menu_callback, admin_menu_callback, \
                                    currency_menu_page_callback, currency_menu_symbol_callback
from bot.misc.states import Option1, Option2, Option3, Option4, Option5


async def register_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(callback=start_admin, is_admin=True, commands=["start"])
    dp.register_message_handler(callback=start_user, commands=["start"])

    dp.register_message_handler(callback=cancel, commands=["cancel"], state="*")
    dp.register_callback_query_handler(cancel, cancel_callback.filter(), state="*")

    dp.register_callback_query_handler(change_page, currency_menu_page_callback.filter(), state="*")

    dp.register_callback_query_handler(option1, user_menu_callback.filter(option=str(1)))
    dp.register_callback_query_handler(choose_symbol, currency_menu_symbol_callback.filter(),
                                       state=Option1.from_currency)
    dp.register_callback_query_handler(choose_symbol, currency_menu_symbol_callback.filter(),
                                       state=Option1.to_currency)

    dp.register_callback_query_handler(option2, user_menu_callback.filter(option=str(2)))
    dp.register_callback_query_handler(choose_symbol, currency_menu_symbol_callback.filter(),
                                       state=Option2.from_currency)
    dp.register_callback_query_handler(choose_symbol, currency_menu_symbol_callback.filter(),
                                       state=Option2.to_currency)
    dp.register_message_handler(callback=get_start_date, state=Option2.date)

    dp.register_callback_query_handler(option3, user_menu_callback.filter(option=str(3)))
    dp.register_callback_query_handler(choose_symbol, currency_menu_symbol_callback.filter(),
                                       state=Option3.from_currency)
    dp.register_callback_query_handler(choose_symbol, currency_menu_symbol_callback.filter(),
                                       state=Option3.to_currency)
    dp.register_message_handler(callback=get_start_date, state=Option3.start_date)
    dp.register_message_handler(callback=get_end_date, state=Option3.end_date)

    dp.register_callback_query_handler(option4, user_menu_callback.filter(option=str(4)))
    dp.register_callback_query_handler(choose_symbol, currency_menu_symbol_callback.filter(),
                                       state=Option4.from_currency)
    dp.register_callback_query_handler(choose_symbol, currency_menu_symbol_callback.filter(),
                                       state=Option4.to_currency)
    dp.register_message_handler(callback=get_amount, state=Option4.amount)

    dp.register_callback_query_handler(option5, user_menu_callback.filter(option=str(5)))
    dp.register_callback_query_handler(get_full_name, currency_menu_symbol_callback.filter(), state=Option5.currency)