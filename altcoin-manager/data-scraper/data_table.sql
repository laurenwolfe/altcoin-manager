CREATE TABLE coin_value_history (symbol varchar(10), price_date date,
  open_price money, high_price money, low_price money, close_price money,
  volume bigint, market_cap bigint, add_timestamp timestamp DEFAULT now());

CREATE TABLE currencies (symbol VARCHAR(10), coin_name VARCHAR(50),
  min_confirmations INT, txn_fee FLOAT);

CREATE TABLE markets (base_currency VARCHAR(10), market_currency VARCHAR(10),
  market_name VARCHAR(50), minimum_trade FLOAT, is_active BOOLEAN, date_created date);

CREATE TABLE tickers (market_name VARCHAR(50), bid_price FLOAT,
  ask_price FLOAT, last_price FLOAT, curr_timestamp TIMESTAMP DEFAULT now());

CREATE TABLE daily_market_summary (market_name VARCHAR(50), high_val FLOAT, low_val FLOAT, sale_volume FLOAT,
  last_val FLOAT, base_volume FLOAT, previous_day_price FLOAT, open_buys INT, open_sells INT, data_timestamp TIMESTAMP);