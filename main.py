import os
import json
import logging
import asyncio

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.message import ParseMode

from bot.config import TELEGRAM_TOKEN
from bot.handlers import register_handlers
from bot.filters import bind_filters

log = logging.getLogger(__name__)
log.setLevel(os.environ.get('LOGGING_LEVEL', 'INFO').upper())


async def process_event(event, dp: Dispatcher):
    update = json.loads(event['body'])
    log.debug('Update: ' + str(update))
    Bot.set_current(dp.bot)
    update = types.Update.to_object(update)
    await dp.process_update(update)


async def handler(event, context):
    if event['httpMethod'] == 'POST':
        bot = Bot(TELEGRAM_TOKEN)
        storage = MemoryStorage()
        dp = Dispatcher(bot, storage=storage)
        await register_handlers(dp)
        await bind_filters(dp)
        await process_event(event, dp)

        return {'statusCode': 200, 'body': 'ok'}
    return {'statusCode': 405}