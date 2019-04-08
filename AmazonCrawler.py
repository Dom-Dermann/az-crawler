import requests
import argparse
from bs4 import BeautifulSoup

def amazon_single_spider(url):
    price = 'price'

    try:
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, features="html.parser")

        for our_price in soup.findAll('span', {'id': 'priceblock_ourprice'}):
            price = our_price.getText()
    except:
        pass

    return price

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Provide the URL of a product you want monitored.")
    parser.add_argument('URL', type=str, help='provide you URL of your product.')
    args = parser.parse_args()

    result = amazon_single_spider(args.URL)
    print(result)