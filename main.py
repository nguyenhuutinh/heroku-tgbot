import telebot
import os
from config import *
import logging

bot = telebot.TeleBot(BOT_TOKEN)
logger = telebot.logger
logger.setLevel(logging.DEBUG)

@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.username
    bot.reply_to(message, 'Hello, {user_name}')