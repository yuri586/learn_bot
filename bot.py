# import telebot

# # Replace 'YOUR_API_TOKEN' with your actual Telegram bot API token
# API_TOKEN = 'YOUR_API_TOKEN'

# bot = telebot.TeleBot(API_TOKEN)

# @bot.message_handler(func=lambda message: True)
# def echo_message(message):
#     bot.reply_to(message, message.text)

# if __name__ == '__main__':
#     print("Bot is running...")
#     bot.polling(none_stop=True)


# Импортируем Updater, компонент овечающий за коммуникацию с Telegram.
# Импортируем обработчик команд
# Импортируем обработчик текстовых сообщений
import logging
import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def greet_user(update, context):
    print("Вызван /старт")
    update.message.reply_text("Здравствуй, пользователь")
    print(context)


def talk_to_me(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)


def main():  # Тело бота. Функция main() - это точка входа в программу.  Содержит в себе всю логику бота.
    # print("Бот запускается...")  # Проверяем запускается ли бот
    mybot = Updater(
        settings.API_KEY, use_context=True
    )  # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Бот стартовал")
    mybot.start_polling()  # Командуем боту начать (несколько раз в секунду) ходить в Telegram за сообщениями
    mybot.idle()  # Запускаем бота, он будет работать, пока мы его не остановим вручную (например, по нажатию Ctrl+C в терминале)


main()  # Запускаем бота
