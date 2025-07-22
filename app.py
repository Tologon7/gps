from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
import logging

app = Flask(__name__)
CORS(app)  # Разрешаем CORS

# Настройки почты — поставь свои реальные
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'your_email@gmail.com'
SMTP_PASS = 'your_app_password'  # Используй App Password или пароль приложения

TO_EMAIL = 'kubandykovtologon@gmail.com'  # Куда шлём

# Настройка логов
logging.basicConfig(level=logging.INFO)

def send_email(subject, body):
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = TO_EMAIL

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, [TO_EMAIL], msg.as_string())
        server.quit()
        app.logger.info("Email sent successfully")
    except Exception as e:
        app.logger.error(f"Failed to send email: {e}")
        raise

@app.route('/send', methods=['POST'])
def receive_data():
    data = request.get_json()
    app.logger.info(f"Received data: {data}")
    try:
        send_email('Новые координаты брата', str(data))
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'fail', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
