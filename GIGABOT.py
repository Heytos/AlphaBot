import telebot
import time

import users

from telebot import types
from datetime import datetime
from dateutil.relativedelta import relativedelta

bot = telebot.TeleBot('TG_BOT_API')

def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    button1 = types.KeyboardButton('Вывести текущий рейтинг')
    button2 = types.KeyboardButton('Вернуться в главное меню')
    markup.add(button1, button2)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    markup = get_main_keyboard()
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

    bot.register_next_step_handler(message, on_click)
@bot.message_handler(func=lambda message: True)
def on_click(message):
    user_id = message.from_user.id
    user = users.get_user_by_id(user_id)

    if not user:
        users.add_new_user(user_id)

    users.sum_alpha_amount(user_id)

    if message.text == 'Вывести текущий рейтинг':
        pass
        
    elif message.text == 'Вернуться в главное меню':
        markup = get_main_keyboard()
        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

def collect_monthly_info():
    conn = users.connect_to_db()
    members = users.get_all_users(conn)
    conn.close()

    message = 'Месячный отчет:\n\n'
    for user in members:
        tg_id, username, alpha_amount = user
        message += f"ID: {tg_id}, Имя: {username}, Счет: {alpha_amount}\n"

    bot.send_message(YOUR_CHAT_ID, message)

def clean_old_data():
    month_ago = datetime.now() - relativedelta(months=1)
    conn = users.connect_to_db()
    c = conn.cursor()
    c.execute("DELETE FROM your_table WHERE your_date_column < ?", (month_ago,))
    conn.commit()
    conn.close()

bot.polling(none_stop=True)