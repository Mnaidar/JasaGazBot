import os
import telebot
from telebot import types

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📄 Отправить данные объекта")
    btn2 = types.KeyboardButton("📷 Прикрепить фото")
    btn3 = types.KeyboardButton("📝 Задать вопрос")
    btn4 = types.KeyboardButton("🌐 Сменить язык")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    
    bot.send_message(message.chat.id, "👋 Привет! Это JASA GAZ бот.\nВыбери действие ниже:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "📄 Отправить данные объекта":
        bot.send_message(message.chat.id, "Пожалуйста, опиши объект: площадь, адрес, тип отопления и т.д.")
    elif message.text == "📷 Прикрепить фото":
        bot.send_message(message.chat.id, "Отправь фото технического паспорта или помещения.")
    elif message.text == "📝 Задать вопрос":
        bot.send_message(message.chat.id, "Задай свой вопрос, мы ответим как можно скорее.")
    elif message.text == "🌐 Сменить язык":
        bot.send_message(message.chat.id, "Скоро будет доступен выбор языка (русский / казахский).")
    else:
        bot.send_message(message.chat.id, "Не понял тебя 🤖. Попробуй выбрать действие с кнопки ниже.")

bot.polling()
