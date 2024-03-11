import keyboards
import service
import content

from constants import Button
from copy import deepcopy

def show_main_menu(user_id, message_id=None):
    message_text = content.choose_option
    if not message_id is None:
        service.edit_message(message_text, user_id, message_id, keyboards.MAIN_MENU)
    else:
        service.send_message(message_text, user_id, keyboards.MAIN_MENU)

def create_lunches_keyboard(lunches):
    result = deepcopy(keyboards.BACK_MENU)
    for i in range(len(lunches)):
        lunch = lunches[i]
        lunch_id = lunch[0]
        lunchItem = {
            'text': f'{i + 1}',
            'callback_data': f'{Button.LUNCH_VOTE.value}_{lunch_id}',
        }
        if i == 3:
            result['inline_keyboard'].append([])
        row = i // 3 if i != 6 else 1
        result['inline_keyboard'][row].append(lunchItem)
    return result

def create_lunches_message(lunches):
    result = '\n\n'
    for i in range(len(lunches)):
        lunch = lunches[i]
        _, lunch_name, lunch_votes_count = lunch
        lunch_line = f'{i + 1}. {lunch_name} - {lunch_votes_count} голосов\n'
        result += lunch_line
    return result

def show_lunch_menu(user_id, message_id):
    lunches = service.get_lunches(user_id)
    message_text = ''
    keyboard = []
    if lunches:
        message_text += content.lunch_variants
        message_text += create_lunches_message(lunches)
        keyboard = create_lunches_keyboard(lunches)
    else:
        keyboard = keyboards.BACK_MENU
        message_text += content.lunch_empty
    service.edit_message(message_text, user_id, message_id, keyboard)

def show_office_menu(user_id, message_id=None):
    users = service.get_users(user_id)
    message_text = ''
    user_presence = False
    if users:
        message_text += content.users_list
        user_presence = user_id in list(users.keys())
        for i, key in enumerate(users):
            user = users[key]
            message_text += f'{i + 1}. '
            if 'nickname' in user:
                message_text += f'[{user["name"]}](https://t.me/{user["nickname"]})'
            else:
                message_text += user['name']
            message_text += '\n'
    else:
        message_text += content.office_empty
    keyboard = keyboards.OFFICE_MENU_PRESENCE_FALSE if user_presence else keyboards.OFFICE_MENU_PRESENCE_TRUE
    if not message_id is None:
        service.edit_message(message_text, user_id, message_id, keyboard)
    else:
        service.send_message(message_text, user_id, keyboard)

def show_presence_menu(user_id, message_id, new_presence):
    message_text = content.presence_true_response if new_presence else content.presence_false_response
    service.edit_message(message_text, user_id, message_id, keyboards.BACK_MENU)
