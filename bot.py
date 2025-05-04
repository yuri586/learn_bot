from glob import glob
import logging
from random import choice, randint
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


def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, ты выиграл!"
    elif user_number == bot_number:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, ничья!"
    else:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, я выиграл!"
    return message


def guess_number(update, context):
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите число"
    update.message.reply_text(message)


def send_cat_picture(update, context):
    cat_photos_list = glob("images/cat*.jp*g")  # Получаем сисок картинок
    cat_pic_filename = choice(cat_photos_list)  # Выбираем случайную
    chat_id = update.effective_chat.id  # Получаем чат id с текущим пользователем
    context.bot.send_photo(
        chat_id=chat_id, photo=open(cat_pic_filename, "rb")
    )  # Передаем информацию


def main():  # Тело бота. Функция main() - это точка входа в программу.  Содержит в себе всю логику бота.
    # print("Бот запускается...")  # Проверяем запускается ли бот
    mybot = Updater(
        settings.API_KEY, use_context=True
    )  # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("cat", send_cat_picture))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Бот стартовал")
    mybot.start_polling()  # Командуем боту начать (несколько раз в секунду) ходить в Telegram за сообщениями
    mybot.idle()  # Запускаем бота, он будет работать, пока мы его не остановим вручную (например, по нажатию Ctrl+C в терминале)


if __name__ == "__main__":  # Если файл вызывается как python bot.py
    main()  # Запускаем бота
