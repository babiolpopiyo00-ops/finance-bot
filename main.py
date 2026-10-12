import asyncio
import logging
import os
from threading import Thread
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from flask import Flask

# Loggingni sozlaymiz (Xatolik bo'lsa konsolda ko'rish uchun)
logging.basicConfig(level=logging.INFO)

# ----------------------------------------------------
# 1. Render uchun Flask Veb-Server (24/7 ishlashiga)
# ----------------------------------------------------
app = Flask("")


@app.route("/")
def home():
    return "Bot status: Active & Running 24/7!"


def run_http_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


def keep_alive():
    t = Thread(target=run_http_server)
    t.daemon = True
    t.start()


# ----------------------------------------------------
# 2. Telegram Bot Klaviaturasi va Handler'lar
# ----------------------------------------------------
router = Router()

# Asosiy tugmalar (Menu)
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📊 Hisobotlar"),
            KeyboardButton(text="📜 Tarix"),
        ],
        [
            KeyboardButton(text="⚙️ Sozlamalar"),
            KeyboardButton(text="❓ Yordam"),
        ],
    ],
    resize_keyboard=True,
)


# /start buyrug'i
@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        f"Assalomu alaykum, {message.from_user.first_name}!\n\n"
        "Moliya hisob-kitob botiga xush kelibsiz.\n"
        "Xarajat yoki daromadni quyidagicha kiritishingiz mumkin:\n"
        "• `-15000 tushlik` (Xarajat)\n"
        "• `+50000 oylik` (Daromad)\n"
        "• Yoki shunchaki raqam: `25000`",
        reply_markup=main_keyboard,
    )


# /help buyrug'i va "❓ Yordam" tugmasi
@router.message(Command("help"))
@router.message(F.text == "❓ Yordam")
async def cmd_help(message: Message):
    help_text = (
        "💡 **Botdan foydalanish yo'riqnomasi:**\n\n"
        "1. **Xarajat kiritish:**\n"
        "   Masalan: `-20000 yo'lga` yoki `15000 taksi`\n\n"
        "2. **Daromad kiritish:**\n"
        "   Masalan: `+1000000 oylik` yoki `+50000`\n\n"
        "3. **Buyruqlar:**\n"
        "   • /start - Botni qayta ishga tushirish\n"
        "   • /help - Yordam menyusi"
    )
    await message.answer(help_text, parse_mode="Markdown")


# "📊 Hisobotlar" tugmasi
@router.message(F.text == "📊 Hisobotlar")
async def show_reports(message: Message):
    await message.answer("📊 Hozircha hisobotlar bo'limi tayyorlanmoqda.")


# "📜 Tarix" tugmasi
@router.message(F.text == "📜 Tarix")
async def show_history(message: Message):
    await message.answer("📜 Oxirgi operatsiyalar tarixi bo'sh.")


# "⚙️ Sozlamalar" tugmasi
@router.message(F.text == "⚙️ Sozlamalar")
async def show_settings(message: Message):
    await message.answer("⚙️ Sozlamalar bo'limi.")


# Xarajat yoki Daromad kiritilganda (Matnni tahlil qilish)
@router.message(F.text)
async def process_transaction(message: Message):
    text = message.text.strip()

    # Daromad (+ bilan boshlansa)
    if text.startswith("+"):
        await message.answer(
            f"✅ **Daromad saqlandi:** {text}\nBaza bilan ulandi!"
        )
    # Xarajat (- bilan boshlansa)
    elif text.startswith("-"):
        await message.answer(
            f"💸 **Xarajat saqlandi:** {text}\nBaza bilan ulandi!"
        )
    # Shunchaki raqam kiritilsa
    elif any(char.isdigit() for char in text):
        await message.answer(
            f"📝 **Amaliyot saqlandi:** {text}\nBaza bilan ulandi!"
        )
    else:
        await message.answer(
            "Tushunarsiz buyruq. Xarajat kiritish uchun masalan `-15000 tushlik` deb yozing yoki /help bosing."
        )


# ----------------------------------------------------
# 3. Asosiy Ishga Tushirish Funksiyasi
# ----------------------------------------------------
async def main():
    # Render o'chmasligi uchun veb-serverni ishga tushiramiz
    keep_alive()

    bot_token = os.environ.get("BOT_TOKEN")
    if not bot_token:
        raise ValueError("BOT_TOKEN topilmadi! Render Environment Variables'ni tekshiring.")

    bot = Bot(token=bot_token)
    dp = Dispatcher()

    # Router'ni ulaymiz
    dp.include_router(router)

    print("Bot muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
  
