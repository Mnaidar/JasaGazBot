import os
import telebot

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Салам! Я бот JASA GAZ — готов принимать заявки 🤖")

bot.polling()
