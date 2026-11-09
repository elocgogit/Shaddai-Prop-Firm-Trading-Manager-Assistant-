from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Telegram error: {e}")

@app.route('/alert', methods=['POST'])
def alert():
    # TradingView sends the alert message as plain text in the body
    body = request.get_data(as_text=True)
    if not body:
        body = str(request.json)
    
    # Format it nicely
    message = f"🚨 <b>NAIRATRADER ALERT</b> 🚨\n\n{body}\n\n⏰ Time: WAT confirmed"
    send_telegram(message)
    return jsonify({"status": "ok"}), 200

@app.route('/', methods=['GET'])
def home():
    return "NairaTrader Alert Server — Active", 200

@app.route('/ping', methods=['GET'])
def ping():
    return "pong", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
