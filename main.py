import os
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Привет! Это JASA GAZ бот. Отправь данные объекта, и мы поможем с расчётом.")

@bot.message_handler(content_types=['text', 'photo', 'document'])
def handle_message(message):
    bot.reply_to(message, "📩 Заявка получена. Менеджер свяжется с вами.")

bot.polling()
