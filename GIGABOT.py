import telebot
import datetime
import users

from users import is_user_admin

TOKEN = "API"
bot = telebot.TeleBot(TOKEN)
TARGET_CHAT_ID = -1001550460619


@bot.message_handler(commands=['rating'])
def send_rating(message):
    try:
        conn = users.connect_to_db()
        all_users = users.get_all_users(conn)
        formatted_users = users.format_users_as_text(all_users)
        bot.send_message(message.chat.id, formatted_users)
        conn.close()
    except Exception as e:
        print("Error:", e)
        bot.send_message(message.chat.id, "Произошла ошибка. Пожалуйста, попробуйте позже.")

@bot.message_handler(commands=['clean_db'])
def clear_database(message):
    if message.chat.id == TARGET_CHAT_ID and is_user_admin(bot, message.from_user.id, message.chat.id):
        conn = users.connect_to_db()
        users.clear_users_table(conn)
        conn.close()
        bot.send_message(message.chat.id, "База данных очищена!")
    else:
        bot.send_message(message.chat.id, "У вас нет прав на выполнение этой команды.")

@bot.message_handler(content_types=['text', 'photo'])
def on_click(message):
    if message.chat.id != TARGET_CHAT_ID:
        return

    user_id = message.from_user.id
    username = message.from_user.username

    conn = users.connect_to_db()

    user = users.get_user_by_id(conn, user_id)
    if not user:
        users.add_new_user(conn, user_id, username)

    users.sum_alpha_amount(conn, user_id)
    conn.close()


if __name__ == "__main__":
    bot.polling(none_stop=True)








