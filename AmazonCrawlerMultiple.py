import requests
from bs4 import BeautifulSoup
import datetime
import argparse
import AmazonCrawler
import texter
import pandafy

# test url single
# https://www.amazon.de/ROCKSTAR-GAMES-no-Redemption-PlayStation/dp/B01M6Y1Y4A/ref=sr_1_1_sspa?keywords=red+dead+redemption+2&qid=1554210224&s=gateway&sr=8-1-spons&psc=1

# test url multiple
# https://www.amazon.de/s?k=red+dead+redemption+2&__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=V0OHKJ0GMJN5&sprefix=red%2Caps%2C163&ref=nb_sb_ss_i_1_3

def amazon_multiple_url_grabber(url, max_pages):
    page = 1
    url_collection = []
    prices = []
    prices_crawled = 0

    while page <= max_pages:
        # add page number parameter to request
        url = url + '&page=' + str(page)

        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, features="html.parser")

        for link in soup.findAll('a', {'class' : 'a-link-normal a-text-normal'}):
            url_collection.append(link['href'])

        page += 1

    #save to file to later crawl the individual links
    texter.array_to_text_file(url_collection, 'links.txt')

    # crawl each link for prices
    for link in url_collection:
        prices.append(AmazonCrawler.amazon_single_spider(link))
        prices_crawled += 1
        print(f'found {prices_crawled} prices.')

    #put out prices as text file for review
    texter.array_to_text_file(prices, 'prices.txt')

    #concert to array of floats
    float_prices = pandafy.prices_to_floats(prices)
    float_prices.sort()
    print(f'The cheapest items is: {float_prices[0]}')


if __name__ == "__main__":
    #create argument parser
    parser = argparse.ArgumentParser(description='Provide search term for crawling / monitoring')
    parser.add_argument('SEARCH', metavar='SEARCH', type=str, help='provide a search term')
    parser.add_argument('--pages', '-p', dest='num_pages', default=3, help='define the maximum number of pages to be scanned by the crawler. Default: 3.')
    args = parser.parse_args()

    print(args)

    print('The execution can take a while. Depending on the amount of links to be crawled, this can take serveral minutes. Please be patient.')

    # execute script depending on flags provided
    amazon_multiple_url_grabber(args.SEARCH, int(args.num_pages))
