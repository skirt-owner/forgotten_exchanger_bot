import os

from bot.misc.types import ID

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMINS_IDS = list(map(lambda admin_id: ID(int(admin_id)), os.getenv("ADMINS_IDS").strip("[]").split(",")))
PREFIXES = "/!"
