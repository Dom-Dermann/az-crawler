import requests
import argparse
import pandafy
import pandas as pd
import datetime
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

    # get crawling result and convert to a float
    result = []
    result.append(amazon_single_spider(args.URL))
    float_price_array = pandafy.prices_to_floats(result)
    float_price = float_price_array[0]

    # prepare new dataframe row with current date
    current_date = datetime.datetime.now()
    data = [ [current_date, float_price] ]
    df = pd.DataFrame(data, columns=['Time', 'Price'])

    try:
        # open CSV to append new row
        old_df = pd.read_csv("single-crawler-monitor.csv")
        # append to old dataframe and save back to csv
        new_csv = old_df.append(df)
        new_csv.to_csv("single-crawler-monitor.csv", index=False)
    except pd.errors.EmptyDataError:
        print('First time run. Starting new csv file.')
        df.to_csv("single-crawler-monitor.csv", index=False)
    