# coding: utf8
import telegram
import logging
from telegram.ext import Updater

bot = telegram.Bot(token='502243941:AAFbHlkv_7TBAWhhoi1v4Nu0e7q0RRfb6lA')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',\
                    level=logging.INFO)



def send_feedback(tuid, cashierName, rating):
    bot.sendMessage(tuid, 'Продавец %s только что получил оценку: %s' % (cashierName, rating))

