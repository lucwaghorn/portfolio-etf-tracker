import yfinance as yf
import psycopg2
from datetime import datetime

HOST = os.getenv("SUPABASE_HOST")
DB = os.getenv("SUPABASE_DB")
USER = os.getenv("SUPABASE_USER")
PASSWORD = os.getenv("SUPABASE_PASSWORD")

# Connexion à Supabase Postgres
conn = psycopg2.connect(
    host=HOST,
    database=DB,
    user=USER,
    password=PASSWORD,
    port="5432"
)

cursor = conn.cursor()

def log_price(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period="1d", interval="15m")
    if data.empty:
        return
    
    last = data.tail(1)
    price = last["Close"].iloc[0]
    ts = last.index[-1].to_pydatetime()

    cursor.execute(
        "insert into market_data (datetime, ticker, close) values (%s, %s, %s)",
        (ts, ticker_symbol, float(price))
    )
    conn.commit()
    print(f"✅ Ajouté {ticker_symbol} @ {price} à {ts}")

# Exemple avec PNAS et PUST
log_price("PNAS.PA")
log_price("PUST.PA")

cursor.close()
conn.close()
