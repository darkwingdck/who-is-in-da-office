import helpers
import requests
import config

from fastapi import FastAPI
from uvicorn import run

app = FastAPI()

def handle_new_user(message):
    chat_id = message['chat']['id']
    text = message['text']
    company_code = text.split(' ')[1]
    params = {
        'chat_id': chat_id,
        'company_code': company_code,
        'name': 'Даня' # TODO: брать имя из message
    }
    data = requests.post(f'{config.API_BASE_URL}/add_user', params = params)
    if data.status_code == 404:
        helpers.send_message('Ошибка! Такой компании не существует', chat_id = chat_id)
        return
    company_name = data.json()[0][0]
    helpers.send_message(f'Добро пожаловать в компанию {company_name}!', chat_id = chat_id)

def handle_message(message):
    text = message['text']
    chat_id = message['chat']['id']
    if text == '/start':
        helpers.send_message('Привет! Это бот WIIDO. Чтобы зарегистрироваться, введите /sign\_up <код своей компании>', chat_id = chat_id)
    elif '/sign_up' in text:
        handle_new_user(message)

@app.post('/bot')
def root(update: dict):
    if not 'message' in update or not 'text' in update['message']:
        return 404
    if 'message' in update and 'text' in update['message']:
        handle_message(update['message'])


def main():
    run(app, host="localhost", port=8000)

if __name__ == "__main__":
    main()

