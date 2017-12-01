# coding: utf8
import telegram

bot = telegram.Bot(token='502243941:AAFbHlkv_7TBAWhhoi1v4Nu0e7q0RRfb6lA')


def send_feedback(tuid, cashierName, rating):
    bot.sendMessage(tuid, 'Продавец %s только что получил оценку: %s' % (cashierName, rating))

