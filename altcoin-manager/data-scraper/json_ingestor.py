# import json
import psycopg2
import requests
import configparser


def fetch_json(json_url):
    """ Fetch JSON served by url, and return as string.

    :param json_url: url of page to scrape
    :return: string of raw html containing page's contents
    with urllib.request.urlopen(url) as response:
        return response.read()
    """
    req = requests.get(url=json_url)
    return req.json()


def get_currency_list(json_currency_data):
    """ Get list of currencies supported by bittrex

    :param json_currency_data: basic data about currency (name, symbol, txn fee)
    :return: db-ready list of currency data
    """
    currency_rows = []
    json_str = fetch_json(json_currency_data)
    json_objects = json_str['result']

    for obj in json_objects:
        symbol = obj['Currency']
        name = obj['CurrencyLong']
        min_confirmations = obj['MinConfirmation']
        txn_fee = obj['TxFee']

        currency_rows.append([symbol, name, min_confirmations, txn_fee])

    return currency_rows


def get_market_list(json_market_data):
    """ Get list of markets supported by bittres

    :param json_market_data: two currencies exchanged in the market, minumum trade amount, date of market creation
    :return: db-ready list of markets
    """
    # Market data
    market_rows = []
    ticker_rows = []
    market_summary_rows = []

    market_str = fetch_json(json_market_data)
    market_objects = market_str['result']

    for market in market_objects:
        base_currency = market['BaseCurrency']
        market_currency = market['MarketCurrency']
        market_name = market['MarketName']
        min_trade_amt = market['MinTradeSize']
        is_active = market['IsActive']
        created_date = market['Created']

        market_rows.append([base_currency, market_currency, market_name,
                            min_trade_amt, is_active, created_date])

        # Use market name to get associated ticker and market summary data
        ticker_rows.append(get_ticker_data(market_name))
        market_summary_rows.append(get_market_summary(market_name))

    return market_rows, ticker_rows, market_summary_rows


def get_ticker_data(market_name):
    """ Real-time price data for a given market (bid, ask, last price)

    :param market_name: the two-symbol combination describing the market's currencies
    :return: db-ready list of ticker data
    """
    # Ticker data
    json_ticker_data = 'https://bittrex.com/api/v1.1/public/getticker?market=' + market_name
    ticker_str = fetch_json(json_ticker_data)
    if ticker_str is not None:
        ticker = ticker_str['result']

        if ticker is not None:
            bid_price = ticker['Bid']
            ask_price = ticker['Ask']
            last_price = ticker['Last']

            return [market_name, bid_price, ask_price, last_price]


def get_market_summary(market_name):
    """ Get detailed summary of market's 24 hour financial performance.

    :param market_name: name of market whose data is retrieved.
    :return: db-ready market summary list
    """
    json_24hr_market_summary = 'https://bittrex.com/api/v1.1/public/getmarketsummary?market=' + market_name
    market_summary_str = fetch_json(json_24hr_market_summary)
    if market_summary_str is not None:
        summary = market_summary_str['result'][0]

        if summary is not None:

            high = summary['High']
            low = summary['Low']
            volume = summary['Volume']
            last = summary['Last']
            base_volume = summary['BaseVolume']
            previous = summary['PrevDay']
            pending_buy = summary['OpenBuyOrders']
            pending_sell = summary['OpenSellOrders']
            time = summary['TimeStamp']

            return [market_name, high, low, volume, last, base_volume, previous, pending_buy, pending_sell, time]


def insert_into_db(list, query):
    """ Insert ingested data into postgres db.

    :param lists: rows to be inserted into db table
    :param table_name: name of table for insertion
    """
    db_creds = configparser.ConfigParser()
    db_creds.read('database.ini')

    conn = psycopg2.connect(dbname=db_creds['postgres']['db_name'],
                            user=db_creds['postgres']['user'],
                            password=db_creds['postgres']['password'])
    cur = conn.cursor()

    for row in list:
        cur.execute(query, row)

    conn.commit()
    cur.close()
    conn.close()


def main():
    json_currency_data = 'https://bittrex.com/api/v1.1/public/getcurrencies'
    json_market_data = 'https://bittrex.com/api/v1.1/public/getmarkets'

    currency_rows = get_currency_list(json_currency_data)
    market_rows, ticker_rows, market_summary_rows = get_market_list(json_market_data)

    insert_into_db(currency_rows, "INSERT INTO currencies VALUES (%s, %s, %s, %s)")
    insert_into_db(market_rows, "INSERT INTO markets VALUES (%s, %s, %s, %s, %s, %s)")
    #insert_into_db(ticker_rows, "INSERT INTO tickers VALUES (%s, %s, %s, %s)")
    insert_into_db(market_summary_rows, "INSERT INTO daily_market_summary VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")


if __name__ == "__main__":
    main()
