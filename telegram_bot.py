import requests

TOKEN = "<TOKEN>"
CHAT_ID = "<USER_CHAT_ID_OR_CHANNEL_CHAT_ID>"


URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def send_image(image_name):
    """Send image file through Telegram bot"""
    url = URL + "sendPhoto"
    files = {'photo': open(image_name, 'rb')}
    data = {'chat_id' : CHAT_ID}
    requests.post(url, files=files, data=data)


def send_text(message):
    """Send text message through Telegram bot"""
    url = URL + "sendMessage"
    data = {'chat_id' : CHAT_ID, 'text' : message}
    requests.post(url,  data=data)
