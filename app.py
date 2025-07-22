from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Разрешаем все CORS-запросы

# Замените эти значения на свои реальные данные
TOKEN = '8026007613:AAFIinG8q-Met5hapLcOmSV0loR57nuiBXc'
CHAT_ID = '7953774150'  # Можно использовать как строку

def send_telegram_message(text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': text,
        'parse_mode': 'HTML'  # Добавляем поддержку HTML-разметки
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp_data = resp.json()
        if not resp.ok or not resp_data.get('ok'):
            error_msg = resp_data.get('description', 'Unknown Telegram API error')
            print(f"Telegram API error: {error_msg}")
            return False, error_msg
        return True, None
    except Exception as e:
        error_msg = f"Request to Telegram failed: {str(e)}"
        print(error_msg)
        return False, error_msg

@app.route('/send', methods=['POST', 'OPTIONS'])
def receive_data():
    if request.method == 'OPTIONS':
        # Обработка предварительного CORS-запроса
        return jsonify({'status': 'success'}), 200
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'fail', 'error': 'No data provided'}), 400
        
        text = f"Новые координаты:\n{data}"
        success, error = send_telegram_message(text)
        
        if success:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'fail', 'error': error}), 500
            
    except Exception as e:
        return jsonify({'status': 'fail', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6899, debug=True)  # Включим debug для диагностики