import requests
import argparse
import pandafy
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from bs4 import BeautifulSoup
import sqlite3

def amazon_single_spider(url):
    price = 'price'
    title = 'title'

    try:
        source_code = requests.get(url)
        print(source_code)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, features="html.parser")

        for our_price in soup.findAll('span', {'id': 'priceblock_ourprice'}):
            price = our_price.getText()

        for product_title in soup.findAll('span', {'id': 'productTitle'}):
            title = product_title.getText()
    except:
        pass

    return price, title

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Provide the URL of a product you want monitored.")
    parser.add_argument('--URL', type=str, help='provide your URL of your product.')
    args = parser.parse_args()

    # initialize variables
    urls = []
    prices = []
    title = 'title'

    # creating database for first time use
    sql_connection = sqlite3.connect("crawler.db")
    sql_cursor = sql_connection.cursor()
    sql_creation = """
    CREATE TABLE IF NOT EXISTS params (
        ind INTEGER PRIMARY KEY, 
        url VARCHAR(200),
        title VARCHAR(50)
    );
    """
    sql_cursor.execute(sql_creation)

    # saving parameters to database for periodic execution, if parameter provided
    if (args.URL):

        sql_command = f"""
        INSERT INTO params (ind, url, title)
            VALUES (NULL, "{args.URL}", "{title}");
        """
        sql_cursor.execute(sql_command)
        sql_connection.commit()

    # collect URLs to be scanned
    sql_command = """
        SELECT url FROM params
    """
    sql_cursor.execute(sql_command)
    rows = sql_cursor.fetchall()
    for row in rows:
        urls.append(row[0])

    # get crawling results from each url and convert to a float
    for url in urls:
        price, title = amazon_single_spider(url)
        title = title.replace("\r", "")
        title = title.strip()
        prices.append(price)
        print(prices)
        float_price_array = pandafy.prices_to_floats(prices)
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

        plot_date = pd.read_csv("single-crawler-monitor.csv", parse_dates=['Time'], index_col='Time')
        plt.plot(plot_date)
        plt.title(title + " price curve")
        plt.show()
    
    sql_connection.close()