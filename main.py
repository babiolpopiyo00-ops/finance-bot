import asyncio
import os
from threading import Thread
from aiogram import Bot, Dispatcher
from flask import Flask

# Handlers papkasidagi barcha routerlarni import qilamiz
from handlers import (
    export,
    history,
    quick,
    reports,
    settings,
    start,
    transactions,
)

# Render o'chib qolmasligi uchun soxta veb-server
app = Flask("")


@app.route("/")
def home():
    return "Bot status: Active"


def run_http_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


def keep_alive():
    t = Thread(target=run_http_server)
    t.daemon = True
    t.start()


async def main():
    # Veb-serverni fonda ishga tushiramiz
    keep_alive()

    bot_token = os.environ.get("BOT_TOKEN")
    if not bot_token:
        raise ValueError("BOT_TOKEN topilmadi!")

    bot = Bot(token=bot_token)
    dp = Dispatcher()

    # Barcha routerlarni dispetcherga ulaymiz
    dp.include_router(start.router)
    dp.include_router(transactions.router)
    dp.include_router(history.router)
    dp.include_router(reports.router)
    dp.include_router(quick.router)
    dp.include_router(settings.router)
    dp.include_router(export.router)

    print("Bot muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
  
