# coding: utf8
import telegram
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler

bot = telegram.Bot(token='502243941:AAFbHlkv_7TBAWhhoi1v4Nu0e7q0RRfb6lA')

updater = Updater(token='502243941:AAFbHlkv_7TBAWhhoi1v4Nu0e7q0RRfb6lA')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',\
                    level=logging.INFO)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Hello! send /code <code> to subscribe for statistics')

def register(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

def send_feedback(tuid, cashierName, rating):
    bot.sendMessage(tuid, 'Продавец %s только что получил оценку: %s' % (cashierName, rating))

start_handler = CommandHandler('start', start)
register_handler = CommandHandler('code', register)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(register_handler)

updater.start_polling()

