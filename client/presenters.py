import keyboards
import content

from service import TelegramBotAPI, UserAPI, LunchAPI
from constants import Button
from copy import deepcopy

class Menu:
    def __init__(self) -> None:
        self.telegramBotAPI = TelegramBotAPI()
        self.userAPI = UserAPI()
        self.lunchAPI = LunchAPI()

class MainMenu(Menu):
    def __init__(self) -> None:
        super().__init__()

    def show(self, user_id, message_id=None):   
        message_text = content.choose_option
        if message_id is not None:
            self.telegramBotAPI.edit_message(message_text, user_id, message_id, keyboards.MAIN_MENU)
        else:
            self.telegramBotAPI.send_message(message_text, user_id, keyboards.MAIN_MENU)

class LunchMenu(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.lunches = []

    def create_keyboard(self):
        result = deepcopy(keyboards.BACK_MENU)
        for i in range(len(self.lunches)):
            lunch = self.lunches[i]
            lunch_item = {
                'text': f'{i + 1}',
                'callback_data': f'{Button.LUNCH_VOTE.value}_{lunch["id"]}'
            }
            if i == 3:
                result['inline_keyboard'].append([])
            row = i // 3 if i != 6 else 1
            result['inline_keyboard'][row].append(lunch_item)
        return result
        
    def create_message(self):
        result = '\n\n'
        for i in range(len(self.lunches)):
            lunch = self.lunches[i]
            lunch_item = f'{i + 1}. {lunch["name"]} - {lunch["votes_count"]} голосов\n'
            result += lunch_item
        return result
    
    def show(self, user_id, message_id):
        self.lunches = self.lunchAPI.get_lunches(user_id)
        message_text = ''
        keyboard = []
        if self.lunches:
            message_text += content.lunch_variants
            message_text += self.create_message()
            keyboard = self.create_keyboard()
        else:
            keyboard = keyboards.BACK_MENU
            message_text += content.lunch_empty
        self.telegramBotAPI.edit_message(message_text, user_id, message_id, keyboard)

class OfficeMenu(Menu):
    def __init__(self) -> None:
        super().__init__()

    def show(self, user_id, message_id=None):
        users = self.userAPI.get_users(user_id)
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
        if message_id is not None:
            self.telegramBotAPI.edit_message(message_text, user_id, message_id, keyboard)
        else:
            self.telegramBotAPI.send_message(message_text, user_id, keyboard)

class PresenceMenu(Menu):
    def __init__(self) -> None:
        super().__init__()

    def show(self, user_id, message_id, new_presence):
        message_text = content.presence_true_response if new_presence else content.presence_false_response
        self.telegramBotAPI.edit_message(message_text, user_id, message_id, keyboards.BACK_MENU)
