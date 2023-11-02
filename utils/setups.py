import ngrok
import requests

from config import TELEGRAM_TOKEN

def start_ngrok():
    listener = ngrok.connect(5000)
    ngrok_url = listener.url()
    print(ngrok_url)
    return ngrok_url


def set_webhook(url):
    r = requests.post(
        f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook', 
        headers={"Content-Type" : "application/json"},
        json={'url': url}
    )
    print(r.text)
    

def setup_tg():
    set_webhook(start_ngrok())    