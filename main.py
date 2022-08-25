from datetime import datetime, timedelta
import telebot
import os
# from config import *
import logging
import psycopg2
from flask import Flask, request
import user_states
from telebot import types,util

db_connection = psycopg2.connect("postgres://imufmulnjjiqnt:829b20d89a1c04269a2acce443e9171042f4e40455fe99496be08fe54d2a2fee@ec2-54-160-109-68.compute-1.amazonaws.com:5432/dbp2nedqcukgic", sslmode="require")
db_object = db_connection.cursor()

BOT_TOKEN = "5697634365:AAEUgF96qD1wcXtxF5x1tXJSH5CjU18KAYM"
APP_URL = "https://telegram-bot-check-name.herokuapp.com"

bot = telebot.TeleBot(BOT_TOKEN)
logger = telebot.logger

logger.setLevel(logging.DEBUG)
server = Flask(__name__)

class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
    # Class will check whether the user is admin or creator in group or not
    key='is_admin'
    @staticmethod
    def check(message: telebot.types.Message):
        return bot.get_chat_member(message.chat.id,message.from_user.id).status in ['administrator','creator']
bot.add_custom_filter(IsAdmin())


@server.route("/", methods=['POST'])
def redirect_message():
    json_string = request.get_data().decode('utf-8')
    print("json_string", json_string)
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


# @bot.message_handler(commands=['start', 'help'])
# def _start(message):
    # print(message)
    # user_name = message.from_user.username
    # start_message = f'Hello, {user_name}! You can add your places with /add command.\n' \
    #                 f'Type /list to show 10 last places you added' \
    #                 f'You can delete all your places with /reset command.' \
    #                 f'Try typing /add <wanted address> to add your first place'
#     bot.reply_to(message, start_message)


# When user types /add we send him to state 2 - ADD_ADDRESS and ask him to write address
@bot.message_handler(commands=['add'])
def _add_start(message):
    print( "add_start")
    # clear address global variable
#     user_states.ADDRESS = ''
#     bot.send_message(message.chat.id, "Write address that you want to save")
#     user_states.update_state(message, user_states.ADD_ADDRESS)

@bot.chat_member_handler()
def chat_m(message: types.ChatMemberUpdated):
    # print("chat_mem", message)
    old = message.old_chat_member
    new = message.new_chat_member
    # print(old)
    # print(new)
#     if new.status == "member":
#         bot.send_message(message.chat.id,"Hello {name}!".format(name=new.user.first_name)) # Welcome message


# When user has written address we send him to state 3 - ADD_COMMENT, where we ask him to write comment
@bot.message_handler(func=lambda message: user_states.get_state(message) == user_states.ADD_ADDRESS)
def _add_address(message):
    print("add_address")
#     user_states.ADDRESS = message.text
#     bot.send_message(message.chat.id, "Write comment (optional)")
#     user_states.update_state(message, user_states.ADD_COMMENT)


# When comment has been written, we save data into our db and send user to starting state 1 - START
@bot.message_handler(func=lambda message: user_states.get_state(message) == user_states.ADD_COMMENT)
def _add_comment(message):
    print("add_comment")


#     user_id = message.from_user.id
#     comment = message.text
#     db_object.execute("INSERT INTO places(address, comment, user_id) VALUES (%s, %s, %s)",
#                       (user_states.ADDRESS, comment, user_id))
#     db_connection.commit()
#     bot.send_message(message.chat.id, "Successfully added!")
#     user_states.update_state(message, user_states.START)

@bot.message_handler(commands=['report'])
def report(message):
    print ('reported', message)
    if message.reply_to_message:
        firstname = message.reply_to_message.from_user.first_name
        last_name = message.reply_to_message.from_user.last_name
        name =  f" {firstname} {last_name}"
        reportName = message.from_user.first_name
        bot.send_message("-643525876", f"{reportName} reported {name}" )

@bot.message_handler(content_types=['photo'])
def photo(message):
    print("photo",message)
    userId = message.from_user.id
    chatId = message.chat.id
    firstName = message.from_user.first_name
    lastName = message.from_user.last_name
    username = message.from_user.username
    print(userId, chatId, firstName, lastName, username, message.caption)
    if (message.text != None and "follow us".lower() in message.text) or ( message.caption != None and "follow us".lower() in message.caption ):
        bot.reply_to(message, "👮‍♀️ ‼️ User: " + firstName + " sử dụng message bị cấm. Mời ra đảo du lịch 1 ngày ‼️ 👮‍♀️")
        bot.delete_message(chatId,message_id=message.id)
        bot.ban_chat_member(chatId, userId, datetime.now() + timedelta(days=1))
        bot.send_message("-643525876", "Reported user id: " + str(userId) + " - firstName: "+ f"{firstName}" + " - lastname: "+ f"{lastName}")
        return
    if (message.text != None and "futt + spot".lower() in message.text) or ( message.caption != None and "futt + spot".lower() in message.caption ):
        bot.reply_to(message, "👮‍♀️ ‼️ User: " + firstName + " sử dụng message bị cấm. Mời ra đảo du lịch 1 ngày ‼️ 👮‍♀️")
        bot.delete_message(chatId,message_id=message.id)
        bot.ban_chat_member(chatId, userId, datetime.now() + timedelta(days=1))
        bot.send_message("-643525876", "Reported user id: " + str(userId) + " - firstName: "+ f"{firstName}" + " - lastname: "+ f"{lastName}")
        return
    if (message.text != None and "anh em chưa vào nhóm".lower() in message.text) or ( message.caption != None and "anh em chưa vào nhóm".lower() in message.caption ):
        bot.reply_to(message, "👮‍♀️ ‼️ User: " + firstName + " sử dụng message bị cấm. Mời ra đảo du lịch 1 ngày ‼️ 👮‍♀️")
        bot.delete_message(chatId,message_id=message.id)
        bot.ban_chat_member(chatId, userId, datetime.now() + timedelta(days=1))
        bot.send_message("-643525876", "Reported user id: " + str(userId) + " - firstName: "+ firstName + " - lastname:" + lastName)
        return    
    if "TCCL Community".lower() in firstName.lower() or (lastName != None and "TCCL Community".lower() in lastName.lower()) :
        bot.reply_to(message, "👮‍♀️ ‼️ User: " + firstName + " sử dụng tên bị cấm. Mời ra đảo du lịch 1 ngày ‼️ 👮‍♀️")
        # bot.reply_to(message, "/report")
        bot.ban_chat_member(chatId, userId, datetime.now() + timedelta(days=1))
        bot.delete_message(chatId,message_id=message.id)
        bot.send_message("-643525876", "Reported user id: " + str(userId) + " - firstName: "+ f"{firstName}" + " - lastname: "+ f"{lastName}")

        return
    if "TCCL".lower()  in firstName.lower()  or (lastName != None and  "TCCL".lower()  in lastName.lower()  ):
        bot.reply_to(message, "👮‍♀️ ‼️ User: " + firstName + " sử dụng tên bị cấm. Mời ra đảo du lịch 1 ngày ‼️")
        # bot.reply_to(message, "/report")
        bot.delete_message(chatId,message_id=message.id)
        bot.ban_chat_member(chatId, userId, datetime.now() + timedelta(days=1))
        # bot.reply_to(message, "/report")
        bot.send_message("-643525876", "Reported user id: " + str(userId) + " - firstName: "+ f"{firstName}" + " - lastname: "+ f"{lastName}")

        return
    if username != None and "tccl" in username or message.from_user.id == 5547260085:
        bot.reply_to(message, "👮‍♀️ ‼️ User: " + username + " sử dụng tên bị cấm. Mời ra đảo du lịch 1 ngày ‼️ 👮‍♀️")
        # bot.reply_to(message, "/report")
        bot.delete_message(chatId,message_id=message.id)
        bot.ban_chat_member(chatId, userId, datetime.now() + timedelta(days=1))
        # bot.reply_to(message, "/report")
        bot.send_message("-643525876", "Reported user id: " + str(userId) + " - username: "+ username)

        return

    if "Đỗ Bảo".lower() == firstName.lower() or (lastName != None and "Đỗ Bảo".lower() == lastName.lower()) :
        bot.reply_to(message, "👮‍♀️ ‼️ User: " + firstName + " sử dụng tên bị cấm. Mời ra đảo du lịch 1 ngày ‼️ 👮‍♀️")
        # bot.reply_to(message, "/report")
        bot.ban_chat_member(chatId, userId, datetime.now() + timedelta(days=1))
        bot.delete_message(chatId,message_id=message.id)

        # bot.reply_to(message, "/report")
        bot.send_message("-643525876", "Reported user id: " + str(userId) + " - firstName: "+ f"{firstName}" + " - lastname: "+ f"{lastName}")

        return
    if "Trade Coin Chiến Lược".lower() in firstName.lower() or (lastName != None and "Trade Coin Chiến Lược".lower() in lastName.lower()) :
        bot.reply_to(message, "👮‍♀️ ‼️ User: " + firstName + " sử dụng tên bị cấm. Mời ra đảo du lịch 1 ngày ‼️  👮‍♀️")
        # bot.reply_to(message, "/report")
        bot.ban_chat_member(chatId, userId, datetime.now() + timedelta(days=1))
        bot.delete_message(chatId,message_id=message.id)

        # bot.reply_to(message, "/report")
        bot.send_message("-643525876", "Reported user id: " + str(userId) + " - firstName: "+ f"{firstName}" + " - lastname: "+ f"{lastName}")

    fullname = f"{firstName} {lastName}"
    if "Trade Coin Chiến Lược".lower() in fullname.lower():
        bot.reply_to(message, "👮‍♀️ ‼️ User: " + firstName + " sử dụng tên bị cấm. Mời ra đảo du lịch 1 ngày ‼️  👮‍♀️")
        # bot.reply_to(message, "/report")
        bot.ban_chat_member(chatId, userId, datetime.now() + timedelta(days=1))
        bot.delete_message(chatId,message_id=message.id)

        # bot.reply_to(message, "/report")
        bot.send_message("-643525876", "Reported user id: " + str(userId) + " - firstName: "+ f"{firstName}" + " - lastname: "+ f"{lastName}")
        return
@bot.message_handler(is_admin=False, func=lambda message: user_states.get_state(message) == user_states.START)
def _all(message):
    # print("other", message)
    
    userId = message.from_user.id
    chatId = message.chat.id
    firstName = message.from_user.first_name
    lastName = message.from_user.last_name
    username = message.from_user.username
    print(userId, chatId, firstName, lastName, username, message.caption)
    
    if (message.text != None and "Land of Conquest".lower() in message.text) or ( message.caption != None and "Land of Conquest".lower() in message.caption ):
        bot.reply_to(message, "👮‍♀️ ‼️ User: " + firstName + " sử dụng message bị cấm. Mời ra đảo du lịch 1 ngày ‼️ 👮‍♀️")
        bot.delete_message(chatId,message_id=message.id)
        bot.ban_chat_member(chatId, userId, datetime.now() + timedelta(days=1))
        bot.send_message("-643525876", "Reported user id: " + str(userId) + " - firstName: "+ f"{firstName}" + " - lastname: "+ f"{lastName}")
        return
    if (message.text != None and "follow us".lower() in message.text) or ( message.caption != None and "follow us".lower() in message.caption ):
        bot.reply_to(message, "👮‍♀️ ‼️ User: " + firstName + " sử dụng message bị cấm. Mời ra đảo du lịch 1 ngày ‼️ 👮‍♀️")
        bot.delete_message(chatId,message_id=message.id)
        bot.ban_chat_member(chatId, userId, datetime.now() + timedelta(days=1))
        bot.send_message("-643525876", "Reported user id: " + str(userId) + " - firstName: "+ f"{firstName}" + " - lastname: "+ f"{lastName}")
        return
    if (message.text != None and "futt + spot".lower() in message.text) or ( message.caption != None and "futt + spot".lower() in message.caption ):
        bot.reply_to(message, "👮‍♀️ ‼️ User: " + firstName + " sử dụng message bị cấm. Mời ra đảo du lịch 1 ngày ‼️ 👮‍♀️")
        bot.delete_message(chatId,message_id=message.id)
        bot.ban_chat_member(chatId, userId, datetime.now() + timedelta(days=1))
        bot.send_message("-643525876", "Reported user id: " + str(userId) + " - firstName: "+ f"{firstName}" + " - lastname: "+ f"{lastName}")
        return
    if (message.text != None and "anh em chưa vào nhóm".lower() in message.text) or ( message.caption != None and "anh em chưa vào nhóm".lower() in message.caption ):
        bot.reply_to(message, "👮‍♀️ ‼️ User: " + firstName + " sử dụng message bị cấm. Mời ra đảo du lịch 1 ngày ‼️ 👮‍♀️")
        bot.delete_message(chatId,message_id=message.id)
        bot.ban_chat_member(chatId, userId, datetime.now() + timedelta(days=1))
        bot.send_message("-643525876", "Reported user id: " + str(userId) + " - firstName: "+ f"{firstName}" + " - lastname: "+ f"{lastName}")
        return
    if "TCCL Community".lower() in firstName.lower() or (lastName != None and "TCCL Community".lower() in lastName.lower()):
        bot.reply_to(message, "👮‍♀️ ‼️ User: " + firstName + " sử dụng tên bị cấm. Mời ra đảo du lịch 1 ngày ‼️ 👮‍♀️")
        bot.delete_message(chatId,message_id=message.id)

        bot.ban_chat_member(chatId, userId, datetime.now() + timedelta(days=1))
        # bot.reply_to(message, "/report")
        bot.send_message("-643525876", "Reported user id: " + str(userId) + " - firstName: "+ f"{firstName}" + " - lastname: "+ f"{lastName}")
        return
    if "TCCL".lower()  in firstName.lower()  or (lastName != None and  "TCCL".lower()  in lastName.lower()  ):
        bot.reply_to(message, "👮‍♀️ ‼️ User: " + firstName + " sử dụng tên bị cấm. Mời ra đảo du lịch 1 ngày ‼️ 👮‍♀️")
        bot.delete_message(chatId,message_id=message.id)

        bot.ban_chat_member(chatId, userId, datetime.now() + timedelta(days=1))
        # bot.reply_to(message, "/report")
        bot.send_message("-643525876", "Reported user id: " + str(userId) + " - firstName: "+ f"{firstName}" + " - lastname: "+ f"{lastName}")
        return
    if username != None and "tccl" in username or message.from_user.id == 5547260085:
        bot.reply_to(message, "👮‍♀️ ‼️ User: " + username + " sử dụng tên bị cấm. Mời ra đảo du lịch 1 ngày ‼️ 👮‍♀️")
        bot.delete_message(chatId,message_id=message.id)
        bot.ban_chat_member(chatId, userId, datetime.now() + timedelta(days=1))
        # bot.reply_to(message, "/report")
        bot.send_message("-643525876", "Reported user id: " + str(userId) + " - username: "+ username)
        return
    if "Đỗ Bảo".lower() == firstName.lower() or (lastName != None and "Đỗ Bảo".lower() == lastName.lower()) :
        bot.reply_to(message, "👮‍♀️ ‼️ User: " + firstName + " sử dụng tên bị cấm. Mời ra đảo du lịch 1 ngày ‼️ 👮‍♀️")
        bot.delete_message(chatId,message_id=message.id)
        bot.ban_chat_member(chatId, userId, datetime.now() + timedelta(days=1))
        # bot.reply_to(message, "/report")
        bot.send_message("-643525876", "Reported user id: " + str(userId) + " - firstName: "+ f"{firstName}" + " - lastname: "+ f"{lastName}")
        return
    if "Trade Coin Chiến Lược".lower() in firstName.lower() or (lastName != None and "Trade Coin Chiến Lược".lower() in lastName.lower()) :
        bot.reply_to(message, "👮‍♀️ ‼️ User: " + firstName + " sử dụng tên bị cấm. Mời ra đảo du lịch 1 ngày ‼️ 👮‍♀️")
        bot.delete_message(chatId,message_id=message.id)
        bot.ban_chat_member(chatId, userId, datetime.now() + timedelta(days=1))
        # bot.reply_to(message, "/report")
        bot.send_message("-643525876", "Reported user id: " + str(userId) + " - firstName: "+ f"{firstName}" + " - lastname: "+ f"{lastName}")


        return

    fullname = f"{firstName} {lastName}"
    if "Trade Coin Chiến Lược".lower() in fullname.lower():
        bot.reply_to(message, "👮‍♀️ ‼️ User: " + firstName + " sử dụng tên bị cấm. Mời ra đảo du lịch 1 ngày ‼️  👮‍♀️")
        # bot.reply_to(message, "/report")
        bot.ban_chat_member(chatId, userId, datetime.now() + timedelta(days=1))
        bot.delete_message(chatId,message_id=message.id)

        # bot.reply_to(message, "/report")
        bot.send_message("-643525876", "Reported user id: " + str(userId) + " - firstName: "+ f"{firstName}" + " - lastname: "+ f"{lastName}")
        return
@bot.message_handler(commands=['list'])
def _list(message):
    print("_list")  
@bot.message_handler(commands=['ban_bao'])
def banuser(message):
    print(message)
    bot.ban_chat_member(-1001724937734, 5547260085)
    bot.ban_chat_member(-1001724937734, 5640136487)
    bot.ban_chat_member(-1001724937734, 5761077402)
    bot.send_message("-643525876", "Đã ban user id: " + str(5547260085) + f" {message.text}")
#     user_id = message.from_user.id
#     db_object.execute("SELECT address, comment FROM places WHERE user_id={} ORDER BY place_id LIMIT 10".format(user_id))
#     result = db_object.fetchall()
#     if not result:
#         bot.send_message(message.chat.id, "You didn't add any saved places")
#     else:
#         reply = "Your added places:\n"
#         for i, item in enumerate(result):
#             reply += "[{}] Address: {}. Comment: {}\n".format(i+1, item[0], item[1])
#         bot.send_message(message.chat.id, reply)
@bot.message_handler(commands=['ban_bot'])
def ban_bot(message):
    print(message)
    bot.ban_chat_member(-1001724937734, 136817688)
    bot.send_message("-643525876", "Đã ban bot id: " + str(136817688) + f" {message.text}")

@bot.message_handler( content_types=[
    "new_chat_members"
])
def new_chat_members(message):
    # bot.reply_to(message, "welcome")
    userId = message.from_user.id
    chatId = message.chat.id

    firstName = message.from_user.first_name
    lastName = message.from_user.last_name
    username = message.from_user.username
    print("WELCOME", userId, chatId, firstName, lastName, username)
    if "Trung Kim Son".lower() in firstName.lower() or (lastName != None and "Trung Kim Son".lower() in lastName.lower()):
        bot.delete_message(chatId,message_id=message.id)
        bot.ban_chat_member(chatId, userId, datetime.now() + timedelta(days=1))
        bot.send_message("-643525876", "Reported user id: " + str(userId) + " - firstName: "+ f"{firstName}" + " - lastname: "+ f"{lastName}")
    if "TCCL Community".lower() in firstName.lower() or (lastName != None and "TCCL Community".lower() in lastName.lower()):
        # bot.reply_to(message, "👮‍♀️ ‼️ " + username + " sử dụng tên bị cấm. Mời ra đảo du lịch 1 ngày ‼️ 👮‍♀️")
        # bot.reply_to(message, "/report")
        bot.delete_message(chatId,message_id=message.id)
        bot.ban_chat_member(chatId, userId, datetime.now() + timedelta(days=1))
        bot.send_message("-643525876", "Reported user id: " + str(userId) + " - firstName: "+ f"{firstName}" + " - lastname: "+ f"{lastName}")

        return
    if "TCCL".lower()  in firstName.lower()  or (lastName != None and  "TCCL".lower()  in lastName.lower()  ):
        # bot.reply_to(message, "👮‍♀️ ‼️ " + username + " sử dụng tên bị cấm. Mời ra đảo du lịch 1 ngày ‼️ 👮‍♀️\n")
        # bot.reply_to(message, "/report")
        bot.delete_message(chatId,message_id=message.id)
        bot.ban_chat_member(chatId, userId, datetime.now() + timedelta(days=1))
        bot.send_message("-643525876", "Reported user id: " + str(userId) + " - firstName: "+ f"{firstName}" + " - lastname: "+ f"{lastName}")

        return
    if username != None and "tccl" in username :
        # bot.reply_to(message, "👮‍♀️ ‼️ " + username + " sử dụng tên bị cấm. Mời ra đảo du lịch 1 ngày ‼️ 👮‍♀️\n")
        # bot.reply_to(message, "/report")
        bot.delete_message(chatId,message_id=message.id)
        bot.ban_chat_member(chatId, userId, datetime.now() + timedelta(days=1))
        bot.send_message("-643525876", "Reported user id: " + str(userId) + " - username: "+ username)
        return

# @bot.message_handler(content_types=[
#     "left_chat_member"
# ])
# def foo(message):
#     bot.reply_to(message, "bye bye")

@bot.message_handler(commands=['reset'])
def _reset(message):
    print("_reset")
#     user_id = message.from_user.id
#     db_object.execute("DELETE FROM places WHERE user_id = {}".format(user_id))
#     db_connection.commit()
#     bot.send_message(message.chat.id, "All your saved addresses have been deleted")


if __name__ == "__main__":
    print("start main")
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    
    

