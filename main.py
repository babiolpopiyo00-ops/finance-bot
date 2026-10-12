import asyncio
import os
from threading import Thread
from aiogram import Bot, Dispatcher
from flask import Flask

# Render taym-autga tushmasligi uchun soxta veb-server
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


# ----------------------------------------------------
# Telegram Bot kodingiz (Main)
# ----------------------------------------------------


async def main():
    # Veb-serverni fonda ishga tushiramiz
    keep_alive()

    # Bot tokenini atrof-muhit o'zgaruvchisidan (Environment Variable) olamiz
    bot_token = os.environ.get("BOT_TOKEN")
    if not bot_token:
        raise ValueError("BOT_TOKEN topilmadi!")

    bot = Bot(token=bot_token)
    dp = Dispatcher()

    # Bu yerda sizning handler laringiz ulangan bo'lishi kerak
    # Masalan: dp.include_router(...)

    print("Bot muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
