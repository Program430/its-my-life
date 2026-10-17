from contextlib import asynccontextmanager

from aiogram import Bot
from aiogram.types import Update
from fastapi import FastAPI, Header, HTTPException, Request

from src.core.database.engine import engine
from src.core.logger import get_logger, setup_logger
from src.core.settings import settings
from src.presentation.routers import main_router
from src.presentation.telegram_rounters import dp

setup_logger()


logger = get_logger()

bot = Bot(settings.telegram_token.get_secret_value())


@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook(
        settings.webhook_url,
        secret_token=settings.request_from_telegram_secret.get_secret_value(),
    )
    await bot.send_message(chat_id=settings.telegram_user_id, text="Бот запущен!")

    yield

    await bot.session.close()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(main_router)


@app.post("/webhook")
async def webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(
        default=None, alias="X-Telegram-Bot-API-Secret-Token"
    ),
):
    if (
        x_telegram_bot_api_secret_token
        != settings.request_from_telegram_secret.get_secret_value()
    ):
        raise HTTPException(status_code=403, detail="Invalid secret token")

    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)

    return {"ok": True}
