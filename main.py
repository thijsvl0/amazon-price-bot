import bot
import db
import scraper
import threading
import sched, time
import os
from classes import ROOT_DIR
from dotenv import load_dotenv

sleep = 3600/2

def main():
    schedule = sched.scheduler(time.time, time.sleep)

    schedule.enter(1, 1, checkPrices, (schedule,))
    schedule.run()


def checkPrices(schedule):
    users = db.get_users()
    for user in users:
        products = db.get_products(user[2])
        for product in products:
            prices = db.get_prices(product[0])
            price = scraper.getPrice(product[2])
            db.add_price(product[0], price)
            try:
                if(float(price) != float(prices[-1][2])):
                    bot.send_message(user[2], "***Price Change***\nName: {} is now \nOld-Price:€{} \nPrice: €{}\nUrl: {}".format(product[1],prices[-1][2], price, product[2]))
            except (IndexError, TypeError):
                continue
    schedule.enter(sleep, 1, checkPrices, (schedule, ))
    

if __name__ == "__main__": 
    load_dotenv(os.path.join(ROOT_DIR, '.env'))
    telegram_bot = threading.Thread(name='Telegram_Bot', target=bot.main)
    main = threading.Thread(name='Main Thread', target=main)
    
    telegram_bot.start()
    main.start()