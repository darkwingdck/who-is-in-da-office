import keyboards
import service
import presenters
import content

from constants import Button, Command

# MESSAGES
def handle_start_message(message):
    # I use telegram's chat_id as user id for queries simplicity
    user_id = message['chat']['id']
    user = service.get_user(user_id)
    if user:
        presenters.show_main_menu(user_id)
    else:
        service.send_message(content.hello_message, user_id)

def get_user_name(message):
    first_name = message['from']['first_name']
    last_name = message['from']['last_name'] if 'last_name' in message['from'] else ''

    nickname = message['from']['username'] if 'username' in message['from'] else ''
    return f'{first_name} {last_name}', nickname

def handle_new_user(message):
    user_id = message['chat']['id']
    user_name, user_nickname = get_user_name(message)
    user = service.get_user(user_id)
    if user:
        service.send_message(content.company_change, user_id, keyboards.MAIN_MENU)
        return
    text = message['text']
    text_parsed = text.split(' ')
    if len(text_parsed) != 2:
        service.send_message(content.company_code_incorrect, user_id)
        return
    company_id = text_parsed[1]
    user_params = {
        'id': str(user_id),
        'company_id': company_id,
        'name': user_name
    }
    if user_nickname:
        user_params['nickname'] = user_nickname
    company = service.add_user(user_params)
    if company:
        service.send_message(content.company_welcome.format(company['name']), user_id, keyboards.MAIN_MENU)
    else:
        service.send_message(content.company_404, user_id)

def handle_new_lunch(message):
    user_id = message['chat']['id']
    text = message['text']
    text_parsed = text.split(' ')
    if len(text_parsed) == 1:
        service.send_message(content.lunch_incorrect, user_id)
        return

    lunch_name = ' '.join(text_parsed[1:])

    user = service.get_user(user_id)

    if not user['lunch_id'] is None:
        service.change_lunch_votes_count(user['lunch_id'], -1)
    new_lunch_id = service.add_lunch(lunch_name, user['company_id'])
    change_user_lunch_response = service.update_user_lunch_id(user['id'], new_lunch_id)

    message_text = ''
    if change_user_lunch_response.ok:
        message_text =  content.lunch_success
    else:
        message_text = content.error_common
    service.send_message(message_text, user_id, keyboards.BACK_MENU)

def handle_unknown_command(message):
    user_id = message['chat']['id']
    service.send_message(content.error_unknown_command, user_id)

# CALLBACKS
def handle_show_main_menu(user_id, message_id):
    presenters.show_main_menu(user_id, message_id)

def handle_show_office_menu(user_id, message_id):
    presenters.show_office_menu(user_id, message_id)

def handle_show_lunch_menu(user_id, message_id):
    presenters.show_lunch_menu(user_id, message_id)

def handle_presence_toggle(user_id, message_id, new_presence):
    response = service.toggle_user_presence(user_id, new_presence)

    if response.ok:
        presenters.show_presence_menu(user_id, message_id, new_presence)
    else:
        service.edit_message(content.error_common, user_id, message_id, keyboards.BACK_MENU)

def handle_lunch_vote(user_id, message_id, button):
    button_parsed = button.split('_')

    if len(button_parsed) != 3:
        service.send_message(content.error_common, user_id, keyboards.BACK_MENU)
        return

    new_lunch_id = int(button_parsed[2])
    user = service.get_user(user_id)

    if user['lunch_id'] == new_lunch_id:
        service.edit_message(content.vote_double, user_id, message_id, keyboards.BACK_MENU)
        return

    user_update_response = service.update_user_lunch_id(user_id, new_lunch_id)
    if not user['lunch_id'] is None:
        service.change_lunch_votes_count(user['lunch_id'], -1)
    new_lunch_update_response = service.change_lunch_votes_count(new_lunch_id, 1)

    message_text = ''
    if user_update_response.ok and new_lunch_update_response.ok:
        message_text = content.vote_success
    else:
        message_text = content.error_common
    service.edit_message(message_text, user_id, message_id, keyboards.BACK_MENU)

def handle_callback(callback_query):
    user_id = str(callback_query['message']['chat']['id'])
    message_id = str(callback_query['message']['message_id'])
    button = callback_query['data']

    if button == Button.BACK.value:
        handle_show_main_menu(user_id, message_id)

    elif button == Button.OFFICE.value:
        handle_show_office_menu(user_id, message_id)

    elif button == Button.LUNCH_SHOW.value:
        handle_show_lunch_menu(user_id, message_id)

    elif button == Button.PRESENCE_FALSE.value:
        handle_presence_toggle(user_id, message_id, False)

    elif button == Button.PRESENCE_TRUE.value:
        handle_presence_toggle(user_id, message_id, True)

    elif Button.LUNCH_VOTE.value in button:
        handle_lunch_vote(user_id, message_id, button)

def handle_message(message):
    text = message['text']

    if Command.START.value in text:
        handle_start_message(message)

    elif Command.SIGN.value in text:
        handle_new_user(message)

    elif Command.LUNCH.value in text:
        handle_new_lunch(message)

    else:
        handle_unknown_command(message)
