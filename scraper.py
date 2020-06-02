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

if __name__ == "__main__":
    _browser = browser()
    print(getPrice("https://www.amazon.com/Nintendo-Switch-Neon-Blue-Joy%E2%80%91/dp/B07VGRJDFY/ref=sr_1_1?dchild=1&fst=as%3Aoff&pf_rd_i=16225016011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=03b28c2c-71e9-4947-aa06-f8b5dc8bf880&pf_rd_r=WHTFPFNG9STV3JK4CVNG&pf_rd_s=merchandised-search-3&pf_rd_t=101&qid=1591017399&refinements=p_89%3ANintendo&rnid=2528832011&s=videogames-intl-ship&sr=1-1"))
