from classes import database
from datetime import datetime
import os
db = None

def main():
    global db
    db = database(os.path.abspath('main.db'))
    make_users_table()
    make_products_table()
    make_prices_table()

def make_users_table():
    db.execute('CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY, name text, chat_id integer)')

def make_products_table():
    db.execute('CREATE TABLE IF NOT EXISTS products (id integer PRIMARY KEY, name text, url text, user_id integer, FOREIGN KEY(user_id) REFERENCES users(id))')

def make_prices_table():
    db.execute('CREATE TABLE IF NOT EXISTS prices (id integer PRIMARY KEY, date datetime, price integer, product_id integer, FOREIGN KEY(product_id) REFERENCES users(id))')

def add_user(name, chat_id):
    if(get_user(chat_id) == None):
        db.execute('INSERT INTO users(name, chat_id) values(?,?)', (name, chat_id,) )
    db.conn.commit()

def get_user(chat_id):
    db.execute('SELECT * FROM users WHERE chat_id = ?', (chat_id, ))
    return db.cursor.fetchone()

def get_users():
    db.execute('SELECT * FROM users')
    return db.cursor.fetchall()

def del_user(chat_id):
    db.execute('DELETE FROM users WHERE chat_id = ?', (chat_id, ))
    db.conn.commit()

def add_product(chat_id, name, url):
    user_id = get_user(chat_id)[0]
    db.execute('INSERT INTO products(name, url, user_id) values(?,?,?)', (name, url, user_id,))
    db.conn.commit()

def get_products(chat_id):
    user_id = get_user(chat_id)[0]
    db.execute('SELECT * FROM products WHERE user_id = ?', (user_id, ))
    return db.cursor.fetchall()

def get_product(product_id):
    db.execute('SELECT * FROM products WHERE id = ?', (product_id, ))
    return db.cursor.fetchone()

def del_product(product_id):
    db.execute('DELETE FROM products WHERE id = ?', (product_id, ))
    db.conn.commit()

def add_price(product_id, price):
    db.execute('INSERT INTO prices(date, price, product_id) values(?,?,?)', (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), price, product_id,))
    db.conn.commit()

def get_prices(product_id):
    db.execute('SELECT * FROM prices WHERE product_id = ?', (product_id, ))
    return db.cursor.fetchall()

def del_price(price_id):
    db.execute('DELETE FROM prices WHERE id = ?', (price_id, ))
    db.conn.commit()

if __name__ == 'db':
    main()




