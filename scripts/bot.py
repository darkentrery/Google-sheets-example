from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from django.conf import settings


bot = Bot(token=settings.TELEGRAM_TOKEN)
dp = Dispatcher(bot)


def send_notification(message: str) -> None:
    executor.start(dp, bot.send_message(settings.TELEGRAM_ID, text=message))
