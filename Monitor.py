import requests
from bs4 import BeautifulSoup
import os
import re

URL = os.getenv("PRODUCT_URL")  
SELECTOR = os.getenv("PRICE_SELECTOR")  
UMBRAL = float(os.getenv("TARGET_PRICE"))

TELEGRAM_TOKEN = os.getenv("TG_TOKEN")
TELEGRAM_CHAT = os.getenv("TG_CHAT_ID")

def obtener_precio():
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    elem = soup.select_one(SELECTOR)
    if not elem:
        raise Exception("No se encontró el selector del precio.")
    txt = elem.get_text()
    num = re.sub(r"[^\d,\.]", "", txt).replace(",", ".")
    return float(num)

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT, "text": msg}
    requests.post(url, data=data)

def main():
    try:
        precio = obtener_precio()
    except Exception as e:
        enviar_telegram(f"Error revisando precio: {e}")
        return
    if precio <= UMBRAL:
        enviar_telegram(f"🔥 BAJÓ EL PRECIO! Ahora vale {precio}\n{URL}")

if __name__ == "__main__":
    main()
