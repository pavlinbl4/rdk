import requests
import os
from dotenv import load_dotenv


def send_telegram_message(text: str):
    load_dotenv()
    token = os.environ.get('crazypythonbot')
    channel_id = os.environ.get('channel_id')

    if not token or not channel_id:
        raise ValueError("Telegram bot token or channel_id is missing")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": channel_id,
        "text": f"Сообщение сервера macbook\n{text}"
    }

    r = requests.post(url, data=data)

    if r.status_code != 200:
        raise Exception(f"Post error: {r.status_code}, {r.text}")


class SendTelegramMessage:
    def __init__(self, message_text, bot_name='crazypythonbot'):
        self.message_text = message_text
        self.bot_name = bot_name

    def credentials(self):
        load_dotenv()
        token = os.environ.get(self.bot_name)
        channel_id = os.environ.get('channel_id')

        if not token or not channel_id:
            raise ValueError("Telegram bot token or channel_id is missing")

        return token, channel_id

    def send_message(self):
        token, channel_id = self.credentials()
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {
            "chat_id": channel_id,
            "text": f"Message from macbook\n{self.message_text}"
        }

        r = requests.post(url, data=data)

        if r.status_code != 200:
            raise Exception(f"Post error: {r.status_code}, {r.text}")

if __name__ == '__main__':
    # send_telegram_message("SSSS")
    SendTelegramMessage('Fucking OOP').send_message()