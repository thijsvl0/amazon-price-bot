from classes import browser
import requests

_browser:browser = None

def getname(url):
    try: 
        name = str(_browser.get_tree(url).xpath('//*[@id="productTitle"]/text()')[0]).replace('\n', '').strip()
    except (IndexError, AttributeError):
        return None
    return name

def getPrice(url):
    try: 
        price = str(_browser.get_tree(url).xpath('//*[@id="price_inside_buybox"]/text()')[0]).replace('\n', '').replace(u'\xa0€', u'').replace('€','').replace('£', '').replace(',','.').strip()
    except (IndexError, AttributeError):
        return None
    return price

def main():
    global _browser
    _browser = browser()

if __name__ ==  "scraper":
    main()