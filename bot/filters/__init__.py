from aiogram import Dispatcher

from bot.filters.admin import AdminIdFilter


async def bind_filters(dp: Dispatcher):
    dp.filters_factory.bind(AdminIdFilter)
