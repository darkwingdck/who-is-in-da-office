import content
import keyboards
import helpers

from json import dumps

def show_main_menu(chat_id):
    message_params = {
        'parse_mode': 'MARKDOWN',
        'chat_id': chat_id,
        'text': 'Выбери одну из опций!',
        'reply_markup': dumps(keyboards.MAIN_MENU)
    }
    helpers.telegram_request('sendMessage', message_params)

def show_lunch_menu(chat_id):
    message_params = {
        'parse_mode': 'MARKDOWN',
        'chat_id': chat_id,
        'text': 'Вот обеды. Чтобы проголосовать за обед, набери /lunch <номер обеда>, а для того, чтобы предолжить свой вариант, набери /lunch <название обеда>',
        'reply_markup': dumps(keyboards.LUNCH_MENU)
    }
    helpers.telegram_request('sendMessage', message_params)

def show_office_menu(chat_id):
    message_params = {
        'parse_mode': 'MARKDOWN',
        'chat_id': chat_id,
        'text': 'Вот кто придет завтра в офис. А ты пойдешь?',
        'reply_markup': dumps(keyboards.OFFICE_MENU_PRESENCE_TRUE)
    }
    helpers.telegram_request('sendMessage', message_params)
