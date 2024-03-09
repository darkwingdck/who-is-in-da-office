import logging
import handlers

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
            handlers.handle_message(update['message'])
        elif 'callback_query' in update:
            handlers.handle_callback(update['callback_query'])
    except Exception as e:
        logging.error(str(e))

def main():
    run(app, host="localhost", port=8000)

if __name__ == "__main__":
    main()
