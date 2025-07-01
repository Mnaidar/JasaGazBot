import telebot
from telebot import types
import os

TOKEN = os.getenv("BOT_TOKEN")  # Переменная из Render
ADMIN_ID = 1168360870  # Твой Telegram ID

bot = telebot.TeleBot(TOKEN)

user_data = {}

# Главное меню
def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📄 Отправить данные объекта", "📷 Прикрепить фото")
    markup.add("📝 Задать вопрос", "🌐 Сменить язык")
    if message.from_user.id == ADMIN_ID:
        markup.add("🛠 Админ-панель")
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

# /start
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "👋 Привет! Это JASA GAZ бот. Отправь данные объекта, и мы поможем с расчётом.")
    main_menu(message)

# Получить Telegram ID
@bot.message_handler(commands=["getid"])
def get_id(message):
    bot.reply_to(message, f"🆔 Ваш Telegram ID: `{message.from_user.id}`", parse_mode="Markdown")

# Обработка текста
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "📄 Отправить данные объекта":
        user_data[message.chat.id] = {}
        bot.send_message(message.chat.id, "Введите адрес объекта:")
        bot.register_next_step_handler(message, get_address)
    elif message.text == "📷 Прикрепить фото":
        bot.send_message(message.chat.id, "📷 Отправьте фото или файл:")
    elif message.text == "📝 Задать вопрос":
        bot.send_message(message.chat.id, "🗣 Задайте ваш вопрос:")
        bot.register_next_step_handler(message, get_question)
    elif message.text == "🌐 Сменить язык":
        bot.send_message(message.chat.id, "🌐 Язык переключён. (функция в разработке)")
    elif message.text == "🛠 Админ-панель" and message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "🛠 Добро пожаловать в админ-панель.\nЗдесь будет доступ к заявкам и настройкам.")
    else:
        bot.send_message(message.chat.id, "🤖 Не понял. Выберите действие с кнопки ниже.")
        main_menu(message)

# Анкета: адрес
def get_address(message):
    user_data[message.chat.id]["address"] = message.text
    bot.send_message(message.chat.id, "Введите площадь объекта в м²:")
    bot.register_next_step_handler(message, get_area)

# Анкета: площадь
def get_area(message):
    user_data[message.chat.id]["area"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Газовое", "Электрическое", "Другое")
    bot.send_message(message.chat.id, "Выберите тип отопления:", reply_markup=markup)
    bot.register_next_step_handler(message, get_heating)

# Анкета: тип отопления
def get_heating(message):
    user_data[message.chat.id]["heating"] = message.text
    data = user_data[message.chat.id]
    text = f"📬 Новая заявка:\n\n🏠 Адрес: {data['address']}\n📐 Площадь: {data['area']} м²\n🔥 Тип отопления: {data['heating']}\n\n👤 От: @{message.from_user.username or 'Без ника'}"
    bot.send_message(ADMIN_ID, text)
    bot.send_message(message.chat.id, "✅ Заявка отправлена! Мы скоро свяжемся с вами.")
    main_menu(message)

# Вопрос от клиента
def get_question(message):
    text = f"❓ Вопрос от пользователя @{message.from_user.username or 'Без ника'}:\n\n{message.text}"
    bot.send_message(ADMIN_ID, text)
    bot.send_message(message.chat.id, "✅ Вопрос отправлен. Мы свяжемся с вами.")
    main_menu(message)

# Обработка фото и файлов
@bot.message_handler(content_types=["photo", "document"])
def handle_files(message):
    file_type = "Фото" if message.content_type == "photo" else "Файл"
    bot.send_message(message.chat.id, f"✅ {file_type} получено. Спасибо!")
    if message.content_type == "photo":
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    elif message.content_type == "document":
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)

# Запуск
bot.polling(none_stop=True)
