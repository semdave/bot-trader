from http.server import BaseHTTPRequestHandler
from datetime import datetime
import json
import os
from bot.solana_trader_bot import get_top_traders

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            days = int(self.path.split("days=")[1]) if "days=" in self.path else 7
            top_traders = get_top_traders(days)
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(top_traders).encode())
        
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
