import requests
import os
from dotenv import load_dotenv


def send_telegram_message(text: str):
    load_dotenv()
    token = os.environ.get('crazypythonbot')
    channel_id = os.environ.get('channel_id')

    url = "https://api.telegram.org/bot"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
        "chat_id": channel_id,
        "text": f"Сообщение с локальной машины\n {text}"
    })

    if r.status_code != 200:
        raise Exception("post_text error")





class SendTelegramMessage:
    def __init__(self, message_text, bot_name='crazypythonbot'):
        self.message_text = message_text
        self.bot_name = bot_name

    def credentials(self):
        load_dotenv()
        token = os.environ.get(self.bot_name)
        channel_id = os.environ.get('channel_id')
        return token, channel_id

    def send_message(self):
        url = "https://api.telegram.org/bot"
        token, channel_id = self.credentials()
        url += token
        method = url + "/sendMessage"

        data = {
            "chat_id": channel_id,
            "text": f"Message from Macbook\n {self.message_text}"
        }

        r = requests.post(method, data=data)

        if r.status_code != 200:
            raise Exception("post_text error")


if __name__ == '__main__':
    SendTelegramMessage('Fucking OOP').send_message()
