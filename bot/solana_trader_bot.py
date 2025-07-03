import requests
import pandas as pd
from datetime import datetime, timedelta

SOLANA_FM_API = "https://api.solana.fm/v0"
BIRDEYE_API = "https://public-api.birdeye.so/public"

def get_top_traders(days=7):
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Simulazione dati (usa API reali in produzione)
        mock_data = [
            {"wallet": "A1", "amount_usd": 1500, "profit": 300, "timestamp": "2024-01-01"},
            {"wallet": "A2", "amount_usd": 2500, "profit": 500, "timestamp": "2024-01-02"},
        ]
        
        df = pd.DataFrame(mock_data)
        df = df[df["amount_usd"] <= 3000]  # Filtra transazioni <= $3000
        
        # Simula il limite di 15 transazioni/giorno
        df = df.groupby("wallet").filter(lambda x: len(x) <= 15)
        
        # Classifica per profitto
        top_traders = df.sort_values("profit", ascending=False).head(50)
        return top_traders.to_dict("records")
    
    except Exception as e:
        print(f"Errore: {e}")
        return []

if __name__ == "__main__":
    top_traders = get_top_traders(7)
    print(pd.DataFrame(top_traders))
