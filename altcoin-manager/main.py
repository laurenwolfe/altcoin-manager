import psycopg2
import configparser


def enter_transaction():
    symbol = ''
    purchase_date = ''
    shares = ''
    unit_price = ''

    print("Enter X to finish inputting data and exit.")

    while symbol == '':
        symbol = input('Enter currency symbol:')
        if check_for_exit(symbol):
            return
        if symbol == '':
            print("Blank entries are not valid, please try again.")
            continue

    while purchase_date == '':
        purchase_date = input('Enter purchase date:')
        if check_for_exit(purchase_date):
            return
        if purchase_date == '':
            print("Please enter the purchase date, or X to exit.")
            continue

    while shares == '':
        shares = input('Enter number of coins purchased:')
        if check_for_exit(shares):
            return
        if shares == '':
            print("Please enter the number of coins purchased, or X to exit.")
            continue

    while unit_price == '':
        unit_price = input('Enter coin unit price:')
        if check_for_exit(unit_price):
            return
        if unit_price == '':
            print("Please enter the per-coin price, or X to exit.")
            continue

    data = [symbol, purchase_date, shares, unit_price]
    query = "INSERT INTO transactions (symbol, purchase_date, num_units, unit_price) VALUES (%s, %s, %s, %s)"
    insert_data_into_db(data, query)


def insert_data_into_db(data, query):
    db_creds = configparser.ConfigParser()
    db_creds.read('data-scraper/database.ini')

    conn = psycopg2.connect(dbname=db_creds['postgres']['db_name'],
                            user=db_creds['postgres']['user'],
                            password=db_creds['postgres']['password'])

    cur = conn.cursor()

    cur.execute(query, data)

    conn.commit()
    cur.close()
    conn.close()


def check_for_exit(line):
    line = line.strip()

    if line == 'X' or line == 'x':
        return True
    else:
        return False


def main():
    enter_transaction()


if __name__ == "__main__":
    main()
