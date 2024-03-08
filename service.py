import config
import constants

from json import dumps
from requests import get, post, put

def telegram_request(method_name, params):
    return get(f'{constants.TELEGRAM_BASE_URL}/{method_name}', params)

def send_message(message, user_id, keyboard=None):
    message_params = {
        'chat_id': str(user_id),
        'text': message
    }
    if not keyboard is None:
        message_params['reply_markup'] = dumps(keyboard)
    telegram_request('sendMessage', message_params)

def edit_message(message, user_id, message_id, keyboard=None):
    message_params = {
        'text': message,
        'chat_id': str(user_id),
        'message_id': message_id
    }
    if not keyboard is None:
        message_params['reply_markup'] = dumps(keyboard)
    telegram_request('editMessageText', message_params)

def delete_message(user_id, message_id):
    params = {
        'chat_id': str(user_id),
        'message_id': message_id
    }
    telegram_request('deleteMessage', params)

def add_user(user_params):
    response = post(f'{config.API_BASE_URL}/users', json=user_params)
    if response.ok:
        company_name = response.json()
        return company_name
    else:
        return ''

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
    return put(f'{config.API_BASE_URL}/users', json=user_params)

def update_user_lunch_id(user_id, new_lunch_id):
    user_params = {
        'id': user_id,
        'lunch_id': new_lunch_id,
    }
    return put(f'{config.API_BASE_URL}/users', json=user_params)

def get_lunches(user_id):
    response = get(f'{config.API_BASE_URL}/lunches', params={ 'user_id': user_id })
    if response.ok:
        return response.json()
    else:
        return []

def change_lunch_votes_count(lunch_id, change_direction=1):
    lunch_params = {
        'id': lunch_id,
    }
    return put(f'{config.API_BASE_URL}/lunches', json=lunch_params, params={ 'change_direction': change_direction })

def add_lunch(lunch_name, company_id):
    lunch_params = {
        'name': lunch_name,
        'company_id': company_id
    }
    response = post(f'{config.API_BASE_URL}/lunches', json=lunch_params)
    return response.json()
