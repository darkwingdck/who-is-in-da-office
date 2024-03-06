import keyboards
import helpers

from copy import deepcopy
from json import dumps

def show_main_menu(chat_id):
    message_params = {
        'parse_mode': 'MARKDOWN',
        'chat_id': chat_id,
        'text': 'Выбери одну из опций!',
        'reply_markup': dumps(keyboards.MAIN_MENU)
    }
    helpers.telegram_request('sendMessage', message_params)

def create_lunches_keyboard(lunches):
    result = deepcopy(keyboards.EMPTY_LUNCH_MENU)
    for i in range(len(lunches)):
        lunch = lunches[i]
        lunch_id = lunch[0]
        lunchItem = {
            'text': f'{i + 1}',
            'callback_data': f'lunch_{lunch_id}',
        }
        result['inline_keyboard'][0].append(lunchItem)
    return result

def create_lunches_message(lunches):
    result = '\n\n'
    for i in range(len(lunches)):
        lunch = lunches[i]
        _, lunch_name, lunch_votes_count = lunch
        lunch_line = f'{i + 1}. {lunch_name} - {lunch_votes_count} голосов\n'
        result += lunch_line
    return result

def show_lunch_menu(user_id):
    lunches = helpers.get_lunches(user_id)
    message_text = ''
    keyboard = []
    if lunches:
        message_text += 'Вот варианты, куда сходить на обед. Ты можешь проголосовать, либо добавить свой вариант, набрав команду /lynch <название варианта>'
        message_text += create_lunches_message(lunches)
        keyboard = create_lunches_keyboard(lunches)
    else:
        keyboard = keyboards.EMPTY_LUNCH_MENU
        message_text += 'Похоже, пока никто не предложил, куда сходить на обед.\nЧтобы добавить варинт, набери команду /lunch <название варианта>'
    
    message_params = {
        'chat_id': user_id,
        'text': message_text,
        'parse_mode': 'MARKDOWN',
        'reply_markup': dumps(keyboard)
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
