CREATE TABLE altcoin.coin_value_history (symbol varchar(10), price_date date,
  open_price money, high_price money, low_price money, close_price money,
  volume bigint, market_cap bigint, add_timestamp timestamp DEFAULT now())