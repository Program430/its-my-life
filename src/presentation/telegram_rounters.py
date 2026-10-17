from aiogram import Dispatcher
from aiogram.types import Message

from src.core.logger import get_logger

dp = Dispatcher()

logger = get_logger()


@dp.message()
async def echo(message: Message):
    await message.answer(f"Вы написали: {message.text}")
