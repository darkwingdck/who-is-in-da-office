import config
from requests import get

telegram_base_url = f'https://api.telegram.org/bot{config.TOKEN}'

def telegram_request(method_name, params = {}):
    get(f'{telegram_base_url}/{method_name}', params)

def send_message(message, chat_id):
    message_params = {
        'chat_id': str(chat_id),
        'text': message,
        'parse_mode': 'MARKDOWN'
    }
    telegram_request('sendMessage', message_params)

def delete_message(chat_id, message_id):
    params = {
      'chat_id': chat_id,
      'message_id': message_id
    }
    telegram_request('deleteMessage', params)
