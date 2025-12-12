import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message, Update
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not BOT_TOKEN:
    raise ValueError("TELEGRAM_TOKEN не установлен в переменных окружения")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.update.middleware()
async def logging_middleware(handler, event: Update, data):
    logging.info(f"Incoming update: {event.model_dump_json(indent=2)}")
    return await handler(event, data)


@dp.message()
async def echo_handler(message: Message):
    if message.text:
        await message.answer(message.text)
    elif message.photo:
        photo = message.photo[-1]
        await message.answer_photo(photo.file_id)
    elif message.sticker:
        await message.answer_sticker(message.sticker.file_id)
    elif message.video:
        await message.answer_video(message.video.file_id)
    elif message.document:
        await message.answer_document(message.document.file_id)


async def main():
    print("✅ Echo bot запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())