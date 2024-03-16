import keyboards
import content

from service import TelegramBotAPI, UserAPI, LunchAPI
from constants import Button
from copy import deepcopy

class Menu:
    def __init__(self, user_id, message_id=None) -> None:
        self.user_id = user_id
        self.message_id = message_id

        self.telegramBotAPI = TelegramBotAPI(self.user_id)
        self.userAPI = UserAPI()
        self.lunchAPI = LunchAPI()

class MainMenu(Menu):
    def __init__(self, user_id, message_id=None) -> None:
        super().__init__(user_id, message_id)

    def show(self):   
        message_text = content.choose_option
        if self.message_id is not None:
            self.telegramBotAPI.edit_message(message_text, self.message_id, keyboards.MAIN_MENU)
        else:
            self.telegramBotAPI.send_message(message_text, keyboards.MAIN_MENU)

class LunchMenu(Menu):
    def __init__(self, user_id, message_id) -> None:
        super().__init__(user_id, message_id)
        self.lunches = []

    def __create_keyboard(self):
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
        
    def __create_message(self):
        result = '\n\n'
        for i in range(len(self.lunches)):
            lunch = self.lunches[i]
            lunch_item = f'{i + 1}. {lunch["name"]} - {lunch["votes_count"]} голосов\n'
            result += lunch_item
        return result
    
    def show(self):
        self.lunches = self.lunchAPI.get_lunches(self.user_id)
        message_text = ''
        keyboard = []
        if self.lunches:
            message_text += content.lunch_variants
            message_text += self.__create_message()
            keyboard = self.__create_keyboard()
        else:
            keyboard = keyboards.BACK_MENU
            message_text += content.lunch_empty
        self.telegramBotAPI.edit_message(message_text, self.message_id, keyboard)

class OfficeMenu(Menu):
    def __init__(self, user_id, message_id=None) -> None:
        super().__init__(user_id, message_id)
    
    def __create_message(self, users):
        if not users:
            return content.office_empty

        result = content.users_list
        for i, key in enumerate(users):
            user = users[key]
            result += f'{i + 1}. '
            if 'nickname' in user:
                result += f'[{user["name"]}](https://t.me/{user["nickname"]})'
            else:
                result += user['name']
            result += '\n'
        return result


    def show(self):
        users = self.userAPI.get_users(self.user_id)
        message_text = self.__create_message(users)
        user_presence = self.user_id in list(users.keys()) if users else False

        keyboard = keyboards.OFFICE_MENU_PRESENCE_FALSE if user_presence else keyboards.OFFICE_MENU_PRESENCE_TRUE

        if self.message_id is not None:
            self.telegramBotAPI.edit_message(message_text, self.message_id, keyboard)
        else:
            self.telegramBotAPI.send_message(message_text, keyboard)

class PresenceMenu(Menu):
    def __init__(self, user_id, message_id) -> None:
        super().__init__(user_id, message_id)

    def show(self, new_presence):
        message_text = content.presence_true_response if new_presence else content.presence_false_response
        self.telegramBotAPI.edit_message(message_text, self.message_id, keyboards.BACK_MENU)
