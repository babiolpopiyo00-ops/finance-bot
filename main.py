import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN
from database import init_db
from handlers import start, transactions, quick, reports, history, settings, export
from scheduler import setup_scheduler

async def main():
    # Logging sozlash
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        stream=sys.stdout
    )
    
    # Ma'lumotlar bazasini ishga tushirish
    await init_db()
    logging.info("Ma'lumotlar bazasi muvaffaqiyatli ulandi.")

    # Bot va Dispatcher yaratish
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # Routerni ulash (Handlerlar)
    dp.include_router(start.router)
    dp.include_router(transactions.router)
    dp.include_router(quick.router)
    dp.include_router(reports.router)
    dp.include_router(history.router)
    dp.include_router(settings.router)
    dp.include_router(export.router)

    # Rejalashtiruvchini (scheduler) ishga tushirish
    setup_scheduler(bot)

    # Eski xabarlarni oʻchirib, yangi ulanishni boshlash
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("Bot ishga tushdi...")
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot to'xtatildi!")
      
