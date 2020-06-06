import sqlite3
from sqlite3 import Error
import requests
from lxml import html
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class database:
    def __init__(self, db_file):
        self.conn = self.create_connection(db_file)
        self.cursor = self.conn.cursor()

    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file, check_same_thread=False)
        except Error as e:
            print(e)
        finally:
            return conn

    def execute(self, query, placeholder = ""):
        try:
            self.cursor.execute(query, placeholder)
        except Error as e:
            print(e)

class browser:
    def __init__(self):
        self.requests = requests
    
    def goto(self, url):
        headers = {
            'authority': 'www.amazon.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        try:
            return self.requests.get(url, headers=headers)
        except (requests.exceptions.ConnectionError, requests.exceptions.MissingSchema):
            return None
    
    def get_text(self, url):
        return self.goto(url).text
    
    def get_tree(self, url):
        return html.fromstring(self.goto(url).content)