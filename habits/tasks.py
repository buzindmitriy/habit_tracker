# habits/tasks.py

from celery import shared_task
import requests
import os


@shared_task
def send_telegram_notification(chat_id, message):
    """
    Отправляет уведомление в Telegram.
    """
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    response = requests.post(url, data=data)
    return response.json()
