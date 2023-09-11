import sqlite3

def connect_to_db(db_name='gigausers.db'):
    return sqlite3.connect(db_name)

def setup_database(conn):
    c = conn.cursor()
    c.execute('''
    CREATE TABLE users (
        tg_id INTEGER PRIMARY KEY,
        username TEXT,
        alpha_amount INTEGER
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
    return c.fetchone

def format_users_as_text(users):
    text = 'Рейтинг пользователей:\n\n'
    for idx, user in enumerate(users,1):
        text += f"{idx}. {user[1]} (ID: {user[0]}) - {user[2]} сообщений\n"
    return text
def add_new_user(conn, tg_id):
    c = conn.cursor()
    c.execute('INSERT INTO users(tg_id, alpha_amount) VALUES (?, ?)', (tg_id, 0))
    conn.commit()

def sum_alpha_amount(conn, tg_id):
    c = conn.cursor()
    c.execute('UPDATE users SET alpha_amount = alpha_amount + 1 WHERE tg_id=?', (tg_id,))
    conn.commit()


conn = connect_to_db()
setup_database(conn)

tg_id = update.message.from_user.id

user = get_user_by_id(conn, tg_id)
if not user:
    add_new_user(conn, tg_id)

sum_alpha_amount(conn, tg_id)

conn.close()