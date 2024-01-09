import uuid
import os
import logging
import asyncio
from aiogram.types import InlineKeyboardMarkup, FSInputFile

from download_yotube_video import download_youtube, YRLException, DownloadException
from telegram_bot.get_qualities import get_qualities
from telegram_bot.parse_url import parse_url
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.types.inline_keyboard_button import InlineKeyboardButton


logging.basicConfig(level=logging.INFO)

# apihelper.API_URL = "http://188.234.213.32:8081/bot{0}/{1}"
bot = Bot(token="6922410100:AAFTsqJ3c6qTCmxl8mXY1NDCBpi27vYXrlI")
dp = Dispatcher()
CALLBACK_DATA = ''
CURRENT_URL = ''


async def download_video(chat_id, quality, url):
    try:
        video_id = uuid.uuid4()

        await download_youtube(url=url, quality=quality, video_id=video_id)
        await bot.send_video(chat_id,
                             video=FSInputFile(f"./{video_id}_final.mp4"),
                             caption='Готово')

        os.remove(f"./{video_id}_final.mp4")

    except YRLException:
        await bot.send_message(chat_id, f"Ошибка. Некорректная ссылка - {url}\n"
                                        f"Введите корректную ссылку:")

    except DownloadException:
        await bot.send_message(chat_id, f"Ошибка при скачивании видео - {url}\n"
                                        f"Попробуйте повторить попытку, или попытайтесь скачать позже")


@dp.callback_query()
async def callback_message(callback):
    global CALLBACK_DATA
    global CURRENT_URL
    if 'download_video' in callback.data:
        quality = callback.data.split(" | ")[1]
        await download_video(callback.message.chat.id, quality, CURRENT_URL)
        CURRENT_URL = ''


@dp.message()
async def main_handler(message):
    global CALLBACK_DATA
    global CURRENT_URL
    CALLBACK_DATA = parse_url(message.text)
    if CALLBACK_DATA == 'download_youtube':
        try:
            qualities = await get_qualities(message.text)

            CURRENT_URL = message.text

            buttons = []

            for quality in qualities:
                btn = InlineKeyboardButton(text=quality, callback_data=f"download_video | {quality}")
                buttons.append([btn])

            button = InlineKeyboardMarkup(inline_keyboard=buttons)

            await bot.send_message(message.chat.id, 'Выбери качество', reply_markup=button)

        except YRLException:
            await bot.send_message(message.chat.id, f"Ошибка. Некорректная ссылка - {message.text}\n"
                                                    f"Введите корректную ссылку:")

    elif CALLBACK_DATA == 'download_instagram':
        await bot.send_message(message.chat.id, f"Скачиваем видео: {message.text}")
        await bot.send_message(message.chat.id, message.from_user)  # Суда функцию по скачиванию ютуб
        await bot.send_message(message.chat.id, "Готово")  # Суда файл, или че там

    elif CALLBACK_DATA == 'download_vk':
        await bot.send_message(message.chat.id, f"Скачиваем видео: {message.text}")
        await bot.send_message(message.chat.id, message.from_user)  # Суда функцию по скачиванию ютуб
        await bot.send_message(message.chat.id, "Готово")  # Суда файл, или че там

    elif CALLBACK_DATA == 'download_tiktok':
        await bot.send_message(message.chat.id, f"Скачиваем видео: {message.text}")
        await bot.send_message(message.chat.id, message.from_user)  # Суда функцию по скачиванию ютуб
        await bot.send_message(message.chat.id, "Готово")  # Суда файл, или че там
    else:
        await bot.send_message(message.chat.id, f"Не удается найти видео по ссылке: {message.text}\nПопробуйте еще раз")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
