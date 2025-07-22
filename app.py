from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

TOKEN = '8026007613:AAFIinG8q-Met5hapLcOmSV0loR57nuiBXc'  # Твой токен Telegram-бота
CHAT_ID = 7953774150  # Твой chat_id из Telegram

def send_telegram_message(text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {'chat_id': CHAT_ID, 'text': text}
    resp = requests.post(url, data=payload)
    return resp

@app.route('/send', methods=['POST'])
def receive_data():
    data = request.get_json()
    text = f"Новые координаты брата:\n{data}"
    try:
        resp = send_telegram_message(text)
        if resp.status_code == 200:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'fail', 'error': 'Telegram API error'}), 500
    except Exception as e:
        return jsonify({'status': 'fail', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6899)
