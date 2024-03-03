import helpers

import presenters
import content

from constants import Button, Command

# MESSAGES
def handle_start_message(message):
    # I use telegram's chat_id as user id for queries simplicity
    user_id = message['chat']['id']
    helpers.send_message(content.hello_message, user_id)

def handle_new_user(message):
    user_id = message['chat']['id']
    user_name = message['from']['username']
    text = message['text']
    text_parsed = text.split(' ')
    if len(text_parsed) == 1:
        helpers.send_message('Неверный код компании', user_id)
        return
    company_id = text_parsed[1]
    user_params = {
        'id': str(user_id),
        'company_id': company_id,
        'name': user_name
    }
    helpers.add_user(user_params)

def handle_lunch_vote(message):
    pass

def handle_unknown_command(message):
    user_id = message['chat']['id']
    helpers.send_message('Не понимаю тебя', user_id)

# CALLBACKS
def handle_show_main_menu(user_id):
    presenters.show_main_menu(user_id)

def handle_show_office_menu(user_id):
    presenters.show_office_menu(user_id)

def handle_show_lunch_menu(user_id):
    presenters.show_lunch_menu(user_id)

def handle_presence_toggle(user_id, new_presence):
    helpers.toggle_user_presence(user_id, new_presence)
    presenters.show_main_menu(user_id)

def handle_callback(callback_query):
    user_id = str(callback_query['message']['chat']['id'])
    callback_message_id = callback_query['message']['message_id']
    button = callback_query['data']
    helpers.delete_message(user_id, callback_message_id)

    if button == Button.BACK.value:
        handle_show_main_menu(user_id)

    elif button == Button.OFFICE.value:
        handle_show_office_menu(user_id)

    elif button == Button.LUNCH.value:
        handle_show_lunch_menu(user_id)

    elif button == Button.PRESENCE_FALSE.value:
        handle_presence_toggle(user_id, False)

    elif button == Button.PRESENCE_TRUE.value:
        handle_presence_toggle(user_id, True)

def handle_message(message):
    text = message['text']

    if Command.START.value in text:
        handle_start_message(message)

    elif Command.SIGN_UP.value in text:
        handle_new_user(message)

    elif Command.LUNCH.value in text:
        handle_lunch_vote(message)

    else:
        handle_unknown_command(message)
