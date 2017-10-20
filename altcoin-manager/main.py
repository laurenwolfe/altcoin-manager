import psycopg2
import configparser


def enter_transaction():
    print("Enter X to finish inputting data.")

    while True:
        while symbol is None:
            symbol = input('Enter currency symbol:')
            if check_for_exit(symbol):
                return
            if symbol is None:
                print("Blank entries are not valid, please try again.")

        while purchase_date is None:
            purchase_date = input('Enter purchase date:')
            if check_for_exit(purchase_date):
                return
            if purchase_date is None:
                print("Blank entries are not valid, please try again.")

        while shares is None:
            shares = input('Enter number of coins purchased:')
            if check_for_exit(shares):
                return
            if shares is None:
                print("Blank entries are not valid, please try again.")

        while unit_price is None:
            unit_price = input('Enter coin unit price:')
            if check_for_exit(unit_price):
                return
            if unit_price is None:
                print("Blank entries are not valid, please try again.")

        data = [symbol, purchase_date, shares, unit_price]
        query = "INSERT INTO user_txns (symbol, purchase_date, shares, unit_price) VALUES (%s, %s, %s, %s)"
        insert_data_into_db(data, query)


def insert_data_into_db(data, query):
    db_creds = configparser.ConfigParser()
    db_creds.read('database.ini')

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
