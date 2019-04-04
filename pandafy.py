import pandas
import texter

def prices_to_floats(prices):
    clean_prices = []

    for price in prices:
        if price == 'price':
            pass
        elif price[0] == 'E':
            if '-' in price:
                position = price.index('-')
                clean_price = price[4:position]
                clean_price = clean_price.replace(',', '.')
                clean_price = float(clean_price)
                clean_prices.append(clean_price)
            else:
                clean_price = price[4:]
                clean_price = clean_price.replace(',', '.')
                clean_price = float(clean_price)
                clean_prices.append(clean_price)

    return clean_prices
