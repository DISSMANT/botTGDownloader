import telebot
from telebot.types import *
from download_yotube_video import download_youtube, YRLException

logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot("6922410100:AAFTsqJ3c6qTCmxl8mXY1NDCBpi27vYXrlI")
callback_data = ''


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
    if callback.data == 'choice_message':
        create_choice_message(callback.message)
    else:
        callback_data = callback.data
        bot.send_message(callback.message.chat.id, "Хорошо, а теперь вставь ссылку")

        print_message(callback.message)


def print_message(callback):
    pass
    # print(callback)


@bot.message_handler(content_types=['text'])
def how_many(message):
    global callback_data
    if callback_data:
        if callback_data == 'download_youtube':
            try:
                button = InlineKeyboardMarkup()
                btn = InlineKeyboardButton("Скачать еще", callback_data='choice_message')
                button.row(btn)

                bot.send_message(message.chat.id, f"Скачиваем видео: {message.text}")
                download_youtube(url=message.text, quality='1080')
                bot.send_video(message.chat.id,
                               video=InputFile(os.getcwd() + "\\final.mp4"),
                               caption='Готово',
                               reply_markup=button)

                callback_data = ''
            except YRLException:
                bot.send_message(message.chat.id, f"Ошибка. Некорректная ссылка - {message.text}\n"
                                                  f"Введите корректную ссылку:")

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


bot.polling(none_stop=True)