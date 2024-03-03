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

def show_office_menu(user_id):
    users = helpers.get_users(user_id)
    message_text = ''
    user_presence = False
    if users:
        message_text += 'Вот список людей, которые идут в офис:\n\n'
        user_presence = user_id in list(users.keys())
        for i, key in enumerate(users):
            message_text += f'{i + 1}. {users[key]}\n'
    else:
        message_text += 'Похоже, пока в офис никто не собирается. Будь первым!'
    keyboard = keyboards.OFFICE_MENU_PRESENCE_FALSE if user_presence else keyboards.OFFICE_MENU_PRESENCE_TRUE
    message_params = {
        'parse_mode': 'MARKDOWN',
        'chat_id': user_id,
        'text': message_text,
        'reply_markup': dumps(keyboard)
    }
    helpers.telegram_request('sendMessage', message_params)
