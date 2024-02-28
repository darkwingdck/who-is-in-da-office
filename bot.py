import handlers

from fastapi import FastAPI
from uvicorn import run

app = FastAPI()

@app.post('/bot')
def root(update: dict):
    if 'message' in update and 'text' in update['message']:
        handlers.handle_message(update['message'])
    elif 'callback_query' in update:
        handlers.handle_callback(update['callback_query'])
    else:
        return 404

def main():
    run(app, host="localhost", port=8000)

if __name__ == "__main__":
    main()

