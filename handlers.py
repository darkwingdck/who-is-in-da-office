import helpers
import presenters
import content
import requests
import config

from constants import Button, Command

def handle_lunch_vote(message):
    pass

def handle_unknown_command(message):
    chat_id = message['chat']['id']
    helpers.send_message('Не понимаю тебя', chat_id)

def handle_presence_toggle(status):
    pass

def handle_new_user(message):
    chat_id = message['chat']['id']
    text = message['text']
    company_code = text.split(' ')[1]
    params = {
        'chat_id': chat_id,
        'company_code': company_code,
        'name': 'Даня'
    }
    data = requests.post(f'{config.API_BASE_URL}/add_user', params = params)
    if data.status_code == 404:
        helpers.send_message('Ошибка! Такой компании не существует', chat_id)
        return
    company_name = data.json()[0][0]
    helpers.send_message(f'Добро пожаловать в компанию {company_name}!', chat_id)
    presenters.show_main_menu(chat_id)


def handle_callback(callback_query):
    chat_id = str(callback_query['message']['chat']['id'])
    callback_message_id = callback_query['message']['message_id']
    button = callback_query['data']

    if button == Button.BACK.value:
        presenters.show_main_menu(chat_id)
    
    elif button == Button.OFFICE.value:
        presenters.show_office_menu(chat_id)
    
    elif button == Button.LUNCH.value:
        presenters.show_lunch_menu(chat_id)
    
    elif button == Button.PRESENCE_FALSE.value:
        handle_presence_toggle(False)
    
    elif button == Button.PRESENCE_TRUE.value:
        handle_presence_toggle(True)
    
    helpers.delete_message(chat_id, callback_message_id)


def handle_message(message):
    text = message['text']
    chat_id = message['chat']['id']

    if Command.START.value in text:
        helpers.send_message(content.hello_message, chat_id = chat_id)

    elif Command.SIGN_UP.value in text:
        handle_new_user(message)

    elif Command.LUNCH.value in text:
        handle_lunch_vote(message)
 
    else:
        handle_unknown_command(message)

