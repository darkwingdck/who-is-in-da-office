import keyboards
import service
import presenters
import content

from constants import Button, Command

# MESSAGES
def handle_start_message(message):
    # I use telegram's chat_id as user id for queries simplicity
    user_id = message['chat']['id']
    service.send_message(content.hello_message, user_id)

def handle_new_user(message):
    user_id = message['chat']['id']
    user_name = message['from']['username']
    text = message['text']
    text_parsed = text.split(' ')
    if len(text_parsed) != 2:
        service.send_message('Неверный код компании', user_id)
        return
    company_id = text_parsed[1]
    user_params = {
        'id': str(user_id),
        'company_id': company_id,
        'name': user_name
    }
    company_name = service.add_user(user_params)
    if company_name:
        service.send_message(f'Добро пожаловать в компанию {company_name}!', user_id)
        presenters.show_main_menu(user_id)
    else:
        service.send_message('Ошибка!', user_id, keyboards.BACK_MENU)

def handle_new_lunch(message):
    user_id = message['chat']['id']
    text = message['text']
    text_parsed = text.split(' ')
    if len(text_parsed) == 1:
        service.send_message('Чтобы предложить вариант, набери /lunch <название варианта>', user_id)
        return
    
    lunch_name = ' '.join(text_parsed[1:])
    
    user = service.get_user(user_id)
    response = service.add_lunch(lunch_name, user['company_id'])
    message_text = ''
    if response.ok:
        message_text = 'Супер! Я записал твой вариант, можешь звать друзей голосовать'
    else:
        message_text = 'Что-то пошло не так!'
    service.send_message(message_text, user_id, keyboards.BACK_MENU)

def handle_unknown_command(message):
    user_id = message['chat']['id']
    service.send_message('Не понимаю тебя', user_id)

# CALLBACKS
def handle_show_main_menu(user_id):
    presenters.show_main_menu(user_id)

def handle_show_office_menu(user_id):
    presenters.show_office_menu(user_id)

def handle_show_lunch_menu(user_id):
    presenters.show_lunch_menu(user_id)

def handle_presence_toggle(user_id, new_presence):
    response = service.toggle_user_presence(user_id, new_presence)
    if response.ok:
        presenters.show_presence_menu(user_id, new_presence)
    else:
        service.send_message('Ошибка!', user_id, keyboards.BACK_MENU)

def handle_lunch_vote(user_id, button):
    button_parsed = button.split('_')
    if len(button_parsed) != 3:
        service.send_message('Ошибочка вышла! Попробуй проголосовать еще раз', user_id, keyboards.BACK_MENU)
        return

    new_lunch_id = int(button_parsed[2])
    user = service.get_user(user_id)

    if user['lunch_id'] == new_lunch_id:
        service.send_message('Второй раз проголосовать не получится((', user_id, keyboards.BACK_MENU)
        return

    user_update_response = service.update_user_lunch_id(user_id, new_lunch_id)
    lunch_update_response = service.change_lunch_votes_count(new_lunch_id, 1)
    message_text = ''
    if user_update_response.ok and lunch_update_response.ok:
        message_text = 'Ваш голос очень важен для нас!'
    else:
        message_text = 'Ошибка!'
    service.send_message(message_text, user_id, keyboards.BACK_MENU)

def handle_callback(callback_query):
    user_id = str(callback_query['message']['chat']['id'])
    callback_message_id = callback_query['message']['message_id']
    button = callback_query['data']
    service.delete_message(user_id, callback_message_id)

    if button == Button.BACK.value:
        handle_show_main_menu(user_id)

    elif button == Button.OFFICE.value:
        handle_show_office_menu(user_id)

    elif button == Button.LUNCH_SHOW.value:
        handle_show_lunch_menu(user_id)

    elif button == Button.PRESENCE_FALSE.value:
        handle_presence_toggle(user_id, False)

    elif button == Button.PRESENCE_TRUE.value:
        handle_presence_toggle(user_id, True)
    
    elif Button.LUNCH_VOTE.value in button:
        handle_lunch_vote(user_id, button)

def handle_message(message):
    text = message['text']

    if Command.START.value in text:
        handle_start_message(message)

    elif Command.SIGN_UP.value in text:
        handle_new_user(message)

    elif Command.LUNCH.value in text:
        handle_new_lunch(message)

    else:
        handle_unknown_command(message)
