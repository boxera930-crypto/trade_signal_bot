from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()  # loads .env

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8247606729:AAE5Pbh5lxKy53q7g2usDBPO9CzBEriYU3k")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "-1003239600800")

app = Flask(__name__)

def send_telegram_message(text: str):
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    try:
        r = requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", data=payload, timeout=10)
        r.raise_for_status()
        return True, r.text
    except Exception as e:
        return False, str(e)

@app.route("/tradingview", methods=["POST"])
def tradingview_webhook():
    # Expecting JSON from TradingView (example in README)
    data = request.get_json(silent=True) or {}

    # Try to extract common fields. TradingView variables are configured in the alert message.
    symbol = data.get("symbol") or data.get("ticker") or "N/A"
    side = data.get("side") or data.get("action") or data.get("type") or "N/A"
    price = data.get("price") or data.get("close") or "N/A"
    comment = data.get("comment") or data.get("message") or data.get("note") or ""

    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    # Format message with emojis and HTML (user requested emojis)
    text = (
        "📣 <b>Трейд сигнал</b>\n"
        "📈 <b>{symbol}</b>\n"
        "➡️ <b>Посока:</b> <b>{side}</b>\n"
        "💸 <b>Цена:</b> {price}\n"
        "🕒 <b>Време:</b> {ts}\n"
    ).format(symbol=symbol, side=side, price=price, ts=ts)

    if comment:
        text += "💬 <b>Коментар:</b> {comment}".format(comment=comment)

    ok, resp = send_telegram_message(text)
    if not ok:
        return jsonify({"status":"error","reason":resp}), 500
    return jsonify({"status":"ok","sent":True}), 200

@app.route("/", methods=["GET"])
def index():
    return "TradingView → Telegram webhook is running. POST JSON to /tradingview", 200

if __name__ == "__main__":
    # For local testing; in production use a proper WSGI server.
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
