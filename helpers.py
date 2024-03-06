from typing import List
import config
import content
import presenters

from requests import get, post, put

telegram_base_url = f'https://api.telegram.org/bot{config.TOKEN}'

def telegram_request(method_name, params):
    r = get(f'{telegram_base_url}/{method_name}', params)
    return r

def send_message(message, user_id):
    message_params = {
        'chat_id': str(user_id),
        'text': message
    }
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

def get_lunches(user_id):
    response = get(f'{config.API_BASE_URL}/lunch', params={ 'user_id': user_id })
    if response.ok:
        return response.json()
    else:
        return []

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
