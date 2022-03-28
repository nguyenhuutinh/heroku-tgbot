import telebot
import os
from config import *
import logging
import psycopg2
from flask import Flask, request
import user_states

db_connection = psycopg2.connect(DB_URI, sslmode="require")
db_object = db_connection.cursor()


bot = telebot.TeleBot(BOT_TOKEN)
logger = telebot.logger
logger.setLevel(logging.DEBUG)
server = Flask(__name__)


@server.route("/{}".format(BOT_TOKEN), methods=['POST'])
def redirect_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@bot.message_handler(commands=['start', 'help'])
def _start(message):
    user_name = message.from_user.username
    start_message = f'Hello, {user_name}! You can add your places with /add command.\n' \
                    f'Type /list to show 10 last places you added' \
                    f'You can delete all your places with /reset command.' \
                    f'Try typing /add <wanted address> to add your first place'
    bot.reply_to(message, start_message)


# When user types /add we send him to state 2 - ADD_ADDRESS and ask him to write address
@bot.message_handler(commands=['add'])
def _add_start(message):
    # clear address global variable
    user_states.ADDRESS = ''
    bot.send_message(message.chat.id, "Write address that you want to save")
    user_states.update_state(message, user_states.ADD_ADDRESS)


# When user has written address we send him to state 3 - ADD_COMMENT, where we ask him to write comment
@bot.message_handler(func=lambda message: user_states.get_state(message) == user_states.ADD_ADDRESS)
def _add_address(message):
    user_states.ADDRESS = message.text
    bot.send_message(message.chat.id, "Write comment (optional)")
    user_states.update_state(message, user_states.ADD_COMMENT)


# When comment has been written, we save data into our db and send user to starting state 1 - START
@bot.message_handler(func=lambda message: user_states.get_state(message) == user_states.ADD_COMMENT)
def _add_comment(message):
    user_id = message.from_user.id
    comment = message.text
    db_object.execute("INSERT INTO places(address, comment, user_id) VALUES (%s, %s, %s)",
                      (user_states.ADDRESS, comment, user_id))
    db_connection.commit()
    bot.send_message(message.chat.id, "Successfully added!")
    user_states.update_state(message, user_states.START)


@bot.message_handler(commands=['list'])
def _list(message):
    user_id = message.from_user.id
    db_object.execute("SELECT address, comment FROM places WHERE user_id={} ORDER BY place_id LIMIT 10".format(user_id))
    result = db_object.fetchall()
    if not result:
        bot.send_message(message.chat.id, "You didn't add any saved places")
    else:
        reply = "Your added places:\n"
        for i, item in enumerate(result):
            reply += "[{}] Address: {}. Comment: {}\n".format(i+1, item[0], item[1])
        bot.send_message(message.chat.id, reply)


@bot.message_handler(commands=['reset'])
def _reset(message):
    user_id = message.from_user.id
    db_object.execute("DELETE FROM places WHERE user_id = {}".format(user_id))
    db_connection.commit()
    bot.send_message(message.chat.id, "All your saved addresses have been deleted")


if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
