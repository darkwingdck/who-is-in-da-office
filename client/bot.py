import logging

from config import ENV, SSL_CERTFILE_PATH, SSL_KEYFILE_PATH
from handlers import Message, Callback
from fastapi import FastAPI
from uvicorn import run

app = FastAPI()

logging.basicConfig(
    filename='logs/bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.post('/wiido')
def root(update: dict):
    try:
        if 'message' in update and 'text' in update['message']:
            Message(update['message'])
        elif 'callback_query' in update:
            Callback(update['callback_query'])
    except Exception as e:
        logging.error(str(e))

def main():
    if ENV == 'DEV':
        run(app, host="0.0.0.0", port=8000)
    elif ENV == 'PROD':
        run(app, host="0.0.0.0", port=8443, ssl_keyfile=SSL_KEYFILE_PATH, ssl_certfile=SSL_CERTFILE_PATH)

if __name__ == "__main__":
    main()
