import telebot
import os
from config import *
import logging
import psycopg2
from flask import Flask, request

#db_connection = psycopg2.connection(DB_URI, sslmode="require")
#db_object = db_connection.cursor()


bot = telebot.TeleBot(BOT_TOKEN)
logger = telebot.logger
logger.setLevel(logging.DEBUG)
server = Flask(__name__)


@server.route(f"/{BOT_TOKEN}", methods=['POST'])
def redirect_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@bot.message_handler(commands=['start'])
def _start(message):
    user_name = message.from_user.username
    bot.reply_to(message, f'Hello, {user_name}')


@bot.message_handler(commands=['add'])
def _add(message):
    user_id = message.from_user.id
    text = message.text
 #   db_object.execute("INSERT INTO places(address, user_id) VALUES (%s, %s)", (text, user_id))
 #   db_connection.commit()


@bot.message_handler(commands=['list'])
def _list(message):
    user_id = message.from_user.id
    # Выведем все записи от user_id
    #db_object.execute(f"SELECT address, comment FROM places WHERE user_id={user_id} ORDER BY place_id LIMIT 10")
    #result = db_object.fetchall()
    #if not result:
    #    bot.send_message(message.chat.id, "Вы пока не добавили сохраненных мест")
    #else:
    #    reply = "Ваши сохраненные места:\n"
    #    for i, item in enumerate(result):
    #        reply += f"[{i+1}] Адрес: {item[0]}. Комментарий: {item[1]}"
    #    bot.send_message(message.chat.id, str(result))


@bot.message_handler(commands=['reset'])
def _reset(message):
    user_id = message.from_user.id
    #db_object.execute(f"DELETE FROM places WHERE user_id = {user_id}")
    #db_connection.commit()


if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
