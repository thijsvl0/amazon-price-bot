import telegram
import db
import scraper
from telegram.error import NetworkError, Unauthorized
from time import sleep
import os

update_id = None 
bot = None

# Core Functions

def main():
    global bot
    global update_id
    print('Bot starting')
    bot = telegram.Bot(os.getenv("BOT_TOKEN"))

    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    while True:
        try:
            update_handler(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1

def update_handler(bot:telegram.Bot):
    global update_id

    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        
        if update.message:
            if update.message.text[0] == '/':
                command_handler(update.message)
            else:
                update.message.reply_text('Please send /start to begin!')

def command_handler(message:telegram.Message):
    _message = message.text.split(' ')
    command = _message[0].replace('/', '')
    subcommand = _message[1:]

    if command == 'start':
        command_start(message, subcommand)
    elif command == 'status':
        command_status(message, subcommand)
    elif command == 'subscribe':
        command_subscribe(message, subcommand)
    elif command == 'unsubscribe':
        command_unsubscribe(message, subcommand)
    elif command == 'products':
        command_products(message, subcommand)
    elif command == 'price':
        command_price(message, subcommand)

    message.delete()

def send_message(chat_id, message):
    global bot
    bot.send_message(chat_id, text=message)

# Custom Commands

def command_start(message:telegram.Message, subcommand):
    message.reply_text("/status To get the status of your account \n /subscribe To subscribe \n /unsubscribe To unsubscribe \n /products To get all products")

def command_status(message:telegram.Message, subcommand):
    chat_id = message.chat_id
    user = db.get_user(chat_id)
    if subcommand == []:
        if user == None:
            message.reply_text("You're Not Subscribed \n Use /subscribe to subscribe")
        else:
            message.reply_text("You're Subscribed \n Use /unsubscribe to unsubscribe")

def command_products(message:telegram.Message, subcommand):
    chat_id = message.chat_id
    user = db.get_user(chat_id)
    if user == None:
        message.reply_text("You're Not Subscribed \n Use /subscribe to subscribe")
        return

    if subcommand == []:
        products = db.get_products(message.chat_id)
        if (len(products) > 0):
            for i in products:
                price = db.get_prices(i[0])[-1][2] or 0
                message.reply_text("ID: {} \nName: {}\nPrice: €{}".format(i[0], i[1], price))
        else:
            message.reply_text("No Products Found\nAdd one with /products add <url>")
    elif subcommand[0] == "add":
        if len(subcommand) != 2:
            message.reply_text("Usage: /products add <url>")
        else:
            url = subcommand[1]
            name = scraper.getname(url)
            if name == None:
                message.reply_text('Not a correct url')
            else:
                db.add_product(message.chat_id, name, url)
                message.reply_text('{} Added'.format(name))
    elif subcommand[0] == "del":
        if len(subcommand) != 2:
            message.reply_text("Usage: /products del <id>")
        else:
            product_id = subcommand[1]
            db.del_product(product_id)
            message.reply_text('Deleted!')
    elif subcommand[0] == "help":
        message.reply_text("/products add <url>   Add Product\n/products del <id>    Delete a product")

def command_price(message:telegram.Message, subcommand):
    chat_id = message.chat_id
    user = db.get_user(chat_id)
    
    if user == None:
        message.reply_text("You're Not Subscribed \n Use /subscribe to subscribe")
        return
    
    if len(subcommand) != 1:
        message.reply_text("Usage: /price <product id>")
    else:
        product = db.get_product(subcommand[0])
        prices = db.get_prices(subcommand[0])
        if product:
            if len(prices) > 0:
                price = prices[-1]
                message.reply_text('Latest Price of {}\nPrice: {}\nDate: {}\nUrl: {}'.format(product[1], price[2], price[1], product[2]))
            else:
                message.reply_text('No Prices found, check back in a hour')
        else:
            message.reply_text('Product not found.\nAdd one using /products add <url>')
        

def command_subscribe(message:telegram.Message, subcommand):
    chat_id = message.chat_id
    user = db.get_user(chat_id)
    
    if subcommand == []:
        if user == None:
            db.add_user(message.from_user.first_name, chat_id)
            message.reply_text("You're now subscribed!")
        else:
            message.reply_text("You're already subscribed")

def command_unsubscribe(message:telegram.Message, subcommand):
    chat_id = message.chat_id
    user = db.get_user(chat_id)

    if subcommand == []:
        if user != None:
            db.del_user(message.chat_id)
            message.reply_text("You're now unsubscribed!")
        else:
            message.reply_text("You're already unsubscribed")