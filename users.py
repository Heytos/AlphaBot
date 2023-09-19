import sqlite3
import datetime

def connect_to_db(db_name='gigausers.db'):
    return sqlite3.connect(db_name)

def check_connection(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT sqlite_version();")
        version = cursor.fetchone()
        print("SQLite version:", version[0])
        return True
    except sqlite3.Error as e:
        print("Error:", e)
        return False

def setup_database(conn):
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (  
        tg_id INTEGER PRIMARY KEY,
        username TEXT,
        alpha_amount INTEGER,
        last_update_date DATE
    )
    ''')
    conn.commit()

def get_user_by_id(conn, tg_id):
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE tg_id=?', (tg_id,))
    return c.fetchone()

def get_all_users(conn):
    c = conn.cursor()
    c.execute('SELECT tg_id, username, alpha_amount FROM users ORDER BY alpha_amount DESC')
    return c.fetchall()

def format_users_as_text(users):
    text = 'Рейтинг пользователей:\n\n'
    for idx, user in enumerate(users, 1):
        text += f"{idx}. {user[1]} (ID: {user[0]}) - {user[2]} сообщений\n"
    return text

def add_new_user(conn, tg_id, username):
    c = conn.cursor()
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    c.execute('INSERT INTO users(tg_id, username, alpha_amount, last_update_date) VALUES (?, ?, ?, ?)',
              (tg_id, username, 0, today))
    conn.commit()


def sum_alpha_amount(conn, tg_id):
    c = conn.cursor()
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    c.execute('UPDATE users SET alpha_amount = alpha_amount + 1, last_update_date = ? WHERE tg_id=?', (today, tg_id))
    conn.commit()

def clear_users_table(conn):
    c = conn.cursor()
    c.execute('DELETE FROM users')
    conn.commit()

def is_user_admin(bot, user_id, chat_id):
    admins = bot.get_chat_administrators(chat_id)
    for admin in admins:
        if admin.user.id == user_id:
            return True
    return False







