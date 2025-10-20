import yfinance as yf
import pandas as pd
from datetime import datetime
import os

# Ticker PNAS sur Euronext Paris
TICKER = "PNAS.PA"
CSV_FILE = "pnas_prices.csv"

def get_price():
    ticker = yf.Ticker(TICKER)
    data = ticker.history(period="1d", interval="15m")
    
    if data.empty:
        print("⚠️ Pas de données récupérées")
        return None
    
    # On prend la dernière ligne (le point le plus récent)
    last_row = data.tail(1)
    price = last_row["Close"].iloc[0]
    timestamp = last_row.index[-1].to_pydatetime()
    
    return {"datetime": timestamp, "ticker": TICKER, "price": price}

def save_price(record):
    # Charger l'existant si le fichier existe
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
    else:
        df = pd.DataFrame(columns=["datetime", "ticker", "price"])
    
    # Ajouter la nouvelle ligne
    df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    
    # Sauvegarder
    df.to_csv(CSV_FILE, index=False)
    print(f"✅ Ajouté : {record}")

if __name__ == "__main__":
    record = get_price()
    if record:
        save_price(record)