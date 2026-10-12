import os
from dotenv import load_dotenv

load_dotenv()

# BotFather bergan Telegram bot tokeni
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Ma'lumotlar bazasi nomi
DB_NAME = "finance.db"

# Xarajat va Daromad kategoriyalari
CATEGORIES = {
    "expense": ["Ovqat", "Transport", "Kiyim", "O'yin-kulgi", "Boshqa"],
    "income": ["Oylik", "Otkazma", "Keshbek", "Boshqa"]
}

# Tezkor kiritish so'zlari (avto-kategoriya)
QUICK_KEYWORDS = {
    "ovqat": "Ovqat",
    "taksi": "Transport",
    "metro": "Transport",
    "bozor": "Kiyim",
    "kino": "O'yin-kulgi"
}
