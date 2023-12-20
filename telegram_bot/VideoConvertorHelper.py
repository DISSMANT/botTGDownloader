import uuid

import telebot
from telebot.types import *
from download_yotube_video import download_youtube, YRLException, DownloadException
from telegram_bot.get_qualities import get_qualities
from telegram_bot.parse_url import parse_url

logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot("6922410100:AAFTsqJ3c6qTCmxl8mXY1NDCBpi27vYXrlI")
CALLBACK_DATA = ''
CURRENT_URL = ''


def download_video(chat_id, quality, url):
    try:
        video_id = uuid.uuid4()

        download_youtube(url=url, quality=quality, video_id=video_id)
        bot.send_video(chat_id,
                       video=InputFile(f"./{video_id}_final.mp4"),
                       caption='Готово')

        os.remove(f"./{video_id}_final.mp4")

    except YRLException:
        bot.send_message(chat_id, f"Ошибка. Некорректная ссылка - {url}\n"
                                          f"Введите корректную ссылку:")

    except DownloadException:
        bot.send_message(chat_id, f"Ошибка при скачивании видео - {url}\n"
                                  f"Попробуйте повторить попытку, или попытайтесь скачать позже")


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    global CALLBACK_DATA
    global CURRENT_URL
    if 'download_video' in callback.data:
        quality = callback.data.split(" | ")[1]
        download_video(callback.message.chat.id, quality, CURRENT_URL)
        CURRENT_URL = ''


@bot.message_handler(content_types=['text'])
def how_many(message):
    global CALLBACK_DATA
    global CURRENT_URL
    CALLBACK_DATA = parse_url(message.text)
    print(message.text)
    if CALLBACK_DATA == 'download_youtube':
        try:
            qualities = get_qualities(message.text)

            CURRENT_URL = message.text

            button = InlineKeyboardMarkup()

            for quality in qualities:
                btn = InlineKeyboardButton(quality, callback_data=f"download_video | {quality}")
                button.row(btn)
            bot.send_message(message.chat.id, 'Выбери качество', reply_markup=button)

        except YRLException:
            bot.send_message(message.chat.id, f"Ошибка. Некорректная ссылка - {message.text}\n"
                                              f"Введите корректную ссылку:")

    elif CALLBACK_DATA == 'download_instagram':
        bot.send_message(message.chat.id, f"Скачиваем видео: {message.text}")
        bot.send_message(message.chat.id, message.from_user)  # Суда функцию по скачиванию ютуб
        bot.send_message(message.chat.id, "Готово")  # Суда файл, или че там

    elif CALLBACK_DATA == 'download_vk':
        bot.send_message(message.chat.id, f"Скачиваем видео: {message.text}")
        bot.send_message(message.chat.id, message.from_user)  # Суда функцию по скачиванию ютуб
        bot.send_message(message.chat.id, "Готово")  # Суда файл, или че там

    elif CALLBACK_DATA == 'download_tiktok':
        bot.send_message(message.chat.id, f"Скачиваем видео: {message.text}")
        bot.send_message(message.chat.id, message.from_user)  # Суда функцию по скачиванию ютуб
        bot.send_message(message.chat.id, "Готово")  # Суда файл, или че там


bot.polling(none_stop=True)
