from aiogram.dispatcher.filters.state import State, StatesGroup


class Option1(StatesGroup):
    from_currency = State()
    to_currency = State()


class Option2(StatesGroup):
    from_currency = State()
    to_currency = State()
    date = State()


class Option3(StatesGroup):
    from_currency = State()
    to_currency = State()
    start_date = State()
    end_date = State()


class Option4(StatesGroup):
    from_currency = State()
    to_currency = State()
    amount = State()


class Option5(StatesGroup):
    currency = State()