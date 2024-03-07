from json import dumps
from typing import List
import config
import content
import presenters
import keyboards

from requests import get, post, put

telegram_base_url = f'https://api.telegram.org/bot{config.TOKEN}'

def telegram_request(method_name, params):
    r = get(f'{telegram_base_url}/{method_name}', params)
    return r

def send_message(message, user_id, keyboard=None):
    message_params = {
        'chat_id': str(user_id),
        'text': message
    }
    if not keyboard is None:
        message_params['reply_markup'] = dumps(keyboard)
    telegram_request('sendMessage', message_params)

def delete_message(user_id, message_id):
    params = {
        'chat_id': str(user_id),
        'message_id': message_id
    }
    telegram_request('deleteMessage', params)

def add_user(user_params):
    user_id = user_params['id']
    response = post(f'{config.API_BASE_URL}/users', json=user_params)
    if response.ok:
        company_name = response.json()
        send_message(f'Добро пожаловать в компанию {company_name}!', user_id)
        presenters.show_main_menu(user_id)
    else:
        send_message(response.content, user_id)

def get_users(user_id):
    response = get(f'{config.API_BASE_URL}/users', params={ 'user_id': user_id })
    if response.ok:
        return response.json()
    else:
        return {}

def get_user(user_id):
    response = get(f'{config.API_BASE_URL}/users/{user_id}')
    if response.ok:
        return response.json()
    else:
        return {}

def toggle_user_presence(user_id, new_presence):
    user_params = {
        'id': user_id,
        'presence': new_presence,
    }
    response = put(f'{config.API_BASE_URL}/users', json=user_params)
    if response.ok:
        message = content.presence_true_hint if new_presence else content.presence_false_hint
        send_message(message, user_id)
    else:
        send_message(response.content, user_id)

def get_lunches(user_id):
    response = get(f'{config.API_BASE_URL}/lunches', params={ 'user_id': user_id })
    if response.ok:
        return response.json()
    else:
        return []


def update_user_lunch_id(user_id, new_lunch_id):
    user_params = {
        'id': user_id,
        'lunch_id': new_lunch_id,
    }
    response = put(f'{config.API_BASE_URL}/users', json=user_params)
    if response.ok:
        message = 'Спасибо! Ваш голос очень важен для нас!'
        send_message(message, user_id, keyboards.BACK_MENU)
    else:
        send_message(response.content, user_id)

def change_lunch_votes_count(user_id, lunch_id, change_direction=1):
    lunch_params = {
        'id': lunch_id,
    }
    response = put(f'{config.API_BASE_URL}/lunches', json=lunch_params, params={ 'change_direction': change_direction })
    if response.ok:
        message = 'Спасибо! Ваш голос очень важен для нас!'
        send_message(message, user_id)
    else:
        send_message(response.content, user_id)
