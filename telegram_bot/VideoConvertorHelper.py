import telebot, logging
from telebot.types import *
import json
import requests
from download_yotube_video import download_youtube

logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot("6922410100:AAFTsqJ3c6qTCmxl8mXY1NDCBpi27vYXrlI")
global callback_data


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, с помощью которого ты можешь "
                                      "сохранять видео и прочие материалы с разных платформ\n\n"
                                      "Доступные платформы: Youtube, Instagram, VK, TikTok")

    create_choice_message(message)


def create_choice_message(message):
    button = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("Скачать видео с Youtube", callback_data="download_youtube")
    btn2 = InlineKeyboardButton("Скачать видео из Instagram", callback_data="download_instagram")
    btn3 = InlineKeyboardButton("Скачать видео из VK", callback_data="download_vk")
    btn4 = InlineKeyboardButton("Скачать видео из TikTok", callback_data="download_tiktok")

    button.row(btn1)
    button.row(btn2)
    button.row(btn3)
    button.row(btn4)

    bot.send_photo(message.chat.id, InputFile("choice_window.jpg"), caption="Выбери платформу:", reply_markup=button)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    global callback_data
    if callback.data == "start":
        start(callback.message)

    else:
        callback_data = callback.data
        bot.send_message(callback.message.chat.id, "Хорошо, а теперь вставь ссылку")

        print_message(callback.message)


def print_message(callback):
    pass
    # print(callback)

# def get_youtube_vid(message):


@bot.message_handler(content_types=['text', "audio"])
def how_many(message):
    global callback_data
    if callback_data == 'download_youtube':
        bot.send_message(message.chat.id, f"Скачиваем видео: {message.text}")
        download_youtube(url=message.text, quality='1080')
        # bot.send_message(message.chat.id, message.from_user)  # Суда функцию по скачиванию ютуб
        bot.send_message(message.chat.id, "Готово")  # Суда файл, или че там
        create_choice_message(message)

        callback_data = ''

    elif callback_data == 'download_instagram':
        bot.send_message(message.chat.id, f"Скачиваем видео: {message.text}")
        bot.send_message(message.chat.id, message.from_user)  # Суда функцию по скачиванию ютуб
        bot.send_message(message.chat.id, "Готово")  # Суда файл, или че там
        create_choice_message(message)

        callback_data = ''

    elif callback_data == 'download_vk':
        bot.send_message(message.chat.id, f"Скачиваем видео: {message.text}")
        bot.send_message(message.chat.id, message.from_user)  # Суда функцию по скачиванию ютуб
        bot.send_message(message.chat.id, "Готово")  # Суда файл, или че там
        create_choice_message(message)

        callback_data = ''

    elif callback_data == 'download_tiktok':
        bot.send_message(message.chat.id, f"Скачиваем видео: {message.text}")
        bot.send_message(message.chat.id, message.from_user)  # Суда функцию по скачиванию ютуб
        bot.send_message(message.chat.id, "Готово")  # Суда файл, или че там
        create_choice_message(message)

        callback_data = ''

    else:
        bot.send_message(message.chat.id, text='Выберите платформу, бот работает через интерфейс.')

        create_choice_message(message)

    # bot.delete_message(message.chat.id, message.message_id - 1)
    # bot.delete_message(message.chat.id, message.message_id)
    # global how, from_coin, to_coin
    # how = message.text
    # if from_coin != '':
    #     data = requests.get(f"https://www.cbr-xml-daily.ru/daily_json.js")
    #     data = json.loads(data.text)
    #     try:
    #         how = float(how)
    #     except:
    #         button = InlineKeyboardMarkup()
    #         btn = InlineKeyboardButton("В начало", callback_data='start')
    #         button.add(btn)
    #         bot.send_photo(message.chat.id, InputFile("Screenshot_4.png"),caption="Введите целочисленные значния валют", reply_markup=button)
    #         return
    #     if from_coin == to_coin:
    #         button = InlineKeyboardMarkup()
    #         btn = InlineKeyboardButton("В начало", callback_data='start')
    #         button.add(btn)
    #         bot.send_photo(message.chat.id, InputFile("Screenshot_4.png"),caption="Введите разные валюты", reply_markup=button)
    #         return
    #     elif from_coin == "RUB":
    #         kurs = data['Valute'][f"{to_coin}"]['Value']
    #         res = float(how) / kurs
    #     elif to_coin != "RUB":
    #         kurs = data['Valute'][f"{from_coin}"]['Value']
    #         res = float(how) * kurs
    #         res = res / (data['Valute'][f"{to_coin}"]['Value'] / data['Valute'][to_coin]["Nominal"])
    #     else:
    #         kurs = data['Valute'][f"{from_coin}"]['Value'] / data['Valute'][from_coin]["Nominal"]
    #         res = float(how) * kurs
    #
    #
    #     button = InlineKeyboardMarkup()
    #     btn1 = InlineKeyboardButton("Начать Сначала", callback_data='start')
    #     button.add(btn1)
    #     bot.send_photo(message.chat.id,InputFile("Screenshot_4.png"), caption=f"{how} <b>{from_coin}</b> в <b>{to_coin}</b> будет равно: \n"
    #                                                                           f"➡️ {res} {to_coin}", parse_mode="html", reply_markup=button)
    #     from_coin = ''
    #     to_coin = ''
    #
    # else:
    #     bot.delete_message(message.chat.id, message.message_id)
    #     bot.send_message(message.chat.id, "Введите команду /start, чтобы начать")



def result(message):
    global from_coin, to_coin
    button = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("Назад", callback_data="to_coin_foo")
    btn2 = InlineKeyboardButton("Вернуться в начало", callback_data='start')
    button.row(btn1)
    button.row(btn2)
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_photo(message.chat.id,InputFile("Screenshot_4.png"), caption=f"Введи количество валюты, которую хочешь конвертировать: \nТекущие валюты: {from_coin} -> {to_coin}", reply_markup=button)
bot.polling(none_stop=True)