from bs4 import BeautifulSoup
import urllib.request


def scrape_coin_data(url):
    """ Fetch html served by url, and return as string.

    :param url: url of page to scrape
    :return: string of raw html containing page's contents
    """
    with urllib.request.urlopen(url) as response:
        return response.read()


def parse_coin_data(html):
    """ Extract data from raw html string.

    :param html: string of raw html source
    :return: list of daily coin pricing data lists
    """
    soup = BeautifulSoup(html, 'html.parser')

    results = []

    for row in soup.table.tbody.find_all('tr'):
        data = str(row.get_text(''))
        data = data.strip().split('\n')

        record_date = data[0]
        open_price = float(data[1])
        high_price = float(data[2])
        low_price = float(data[3])
        close_price = float(data[4])
        trade_volume = int(data[5].replace(',', ''))
        market_cap = int(data[6].replace(',', ''))

        results.append([record_date, open_price, high_price, low_price, close_price, trade_volume, market_cap])

    return results


def main():
    url = 'https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20161019&end=20171019'

    html = scrape_coin_data(url)
    data = parse_coin_data(html)

    print(data)


if __name__ == "__main__":
    main()
