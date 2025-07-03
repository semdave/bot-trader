import requests
import pandas as pd
from datetime import datetime, timedelta

# Configurazione API Solana
SOLANA_FM_API = "https://api.solana.fm/v0"
BIRDEYE_API = "https://public-api.birdeye.so/public"

def get_top_traders(days=7):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Ottieni transazioni di memecoin (esempio con Solana FM)
    response = requests.get(
        f"{SOLANA_FM_API}/transactions",
        params={
            "symbol": "MEME",  # Filtra per memecoin
            "from": start_date.strftime("%Y-%m-%d"),
            "to": end_date.strftime("%Y-%m-%d"),
            "limit": 1000
        }
    )
    
    transactions = response.json().get("data", [])
    
    # Filtra i trader
    traders = {}
    for tx in transactions:
        wallet = tx["wallet"]
        amount = tx["amount_usd"]
        
        if wallet not in traders:
            traders[wallet] = {
                "total_tx": 0,
                "total_profit": 0,
                "max_amount": 0,
                "daily_tx": {}
            }
        
        date = tx["timestamp"][:10]
        if date not in traders[wallet]["daily_tx"]:
            traders[wallet]["daily_tx"][date] = 0
        
        traders[wallet]["daily_tx"][date] += 1
        traders[wallet]["total_tx"] += 1
        traders[wallet]["max_amount"] = max(traders[wallet]["max_amount"], amount)
        traders[wallet]["total_profit"] += tx.get("profit", 0)
    
    # Filtra per criteri (max 15 tx/giorno, max $3.000/tx)
    filtered_traders = []
    for wallet, data in traders.items():
        valid = True
        for date, count in data["daily_tx"].items():
            if count > 15:
                valid = False
                break
        if valid and data["max_amount"] <= 3000:
            filtered_traders.append({
                "wallet": wallet,
                "total_profit": data["total_profit"],
                "avg_profit": data["total_profit"] / data["total_tx"]
            })
    
    # Ordina per profitto
    top_traders = sorted(filtered_traders, key=lambda x: x["total_profit"], reverse=True)[:50]
    return pd.DataFrame(top_traders)

# Esegui e salva i risultati
weekly_traders = get_top_traders(7)
monthly_traders = get_top_traders(30)

weekly_traders.to_csv("top_traders_7d.csv", index=False)
monthly_traders.to_csv("top_traders_30d.csv", index=False)
