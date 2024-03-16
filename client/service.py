import config
import constants

from json import dumps
from requests import get, post, put

class TelegramBotAPI():
    def __init__(self, user_id) -> None:
        self.base_url = f'{constants.TELEGRAM_BASE_URL}'
        self.user_id = user_id

    def send_request(self, method_name, params) -> None:
        get(f'{self.base_url}/{method_name}', params)

    def send_message(self, message, keyboard=None) -> None:
        message_params = {
            'chat_id': self.user_id,
            'text': message,
            'parse_mode': 'MARKDOWN',
            'link_preview_options': dumps({
                'is_disabled': True
            })
        }
        if keyboard is not None:
            message_params['reply_markup'] = dumps(keyboard)
        self.send_request('sendMessage', message_params)

    def edit_message(self, message, message_id, keyboard=None) -> None:
        message_params = {
            'text': message,
            'chat_id': self.user_id,
            'message_id': message_id,
            'parse_mode': 'MARKDOWN',
            'link_preview_options': dumps({
                'is_disabled': True
            })
        }
        if keyboard is not None:
            message_params['reply_markup'] = dumps(keyboard)
        self.send_request('editMessageText', message_params)

    def delete_message(self, message_id) -> None:
        params = {
            'chat_id': self.user_id,
            'message_id': message_id
        }
        self.send_request('deleteMessage', params)

class UserAPI:
    def add_user(self, user_params):
        response = post(f'{config.API_BASE_URL}/users', json=user_params)
        if response.ok:
            company_name = response.json()
            return company_name
        else:
            return ''

    def get_user(self, user_id):
        response = get(f'{config.API_BASE_URL}/users/{user_id}')
        if response.ok:
            return response.json()
        else:
            return {}

    def get_users(self, user_id):
        response = get(f'{config.API_BASE_URL}/users', params={ 'user_id': user_id })
        if response.ok:
            return response.json()
        else:
            return {}

    def toggle_user_presence(self, user_id, new_presence):
        user_params = {
            'id': user_id,
            'presence': new_presence,
        }
        return put(f'{config.API_BASE_URL}/users', json=user_params)

    def update_user_lunch_id(self, user_id, new_lunch_id):
        user_params = {
            'id': user_id,
            'lunch_id': new_lunch_id,
        }
        return put(f'{config.API_BASE_URL}/users', json=user_params)

class LunchAPI:
    def get_lunches(self, user_id):
        response = get(f'{config.API_BASE_URL}/lunches', params={ 'user_id': user_id })
        if response.ok:
            return response.json()
        else:
            return []

    def change_lunch_votes_count(self, lunch_id, change_direction=1):
        lunch_params = {
            'id': lunch_id,
        }
        return put(f'{config.API_BASE_URL}/lunches', json=lunch_params, params={ 'change_direction': change_direction })

    def add_lunch(self, lunch_name, company_id):
        lunch_params = {
            'name': lunch_name,
            'company_id': company_id
        }
        response = post(f'{config.API_BASE_URL}/lunches', json=lunch_params)
        return response.json()
