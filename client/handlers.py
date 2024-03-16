import keyboards
import content

from presenters import MainMenu, LunchMenu, OfficeMenu, PresenceMenu
from service import TelegramBotAPI, UserAPI, LunchAPI
from constants import Button, Command

class Handler:
    def __init__(self) -> None:
        self.telegramBotAPI = TelegramBotAPI()
        self.userAPI = UserAPI()
        self.lunchAPI = LunchAPI()

class Message(Handler):
    def __init__(self, message) -> None:
        super().__init__()
        self.mainMenu = MainMenu()
        self.message = message

        text = message['text']

        if Command.START.value in text:
            self.start()

        elif Command.SIGN.value in text:
            self.sign()

        elif Command.LUNCH.value in text:
            self.lunch()

        elif Command.HELP.value in text:
            self.help()

        else:
            self.unknown()

    def start(self):
        user_id = self.message['chat']['id']
        user = self.userAPI.get_user(user_id)
        if user:
            self.mainMenu.show(user_id)
        else:
            self.telegramBotAPI.send_message(content.hello_message, user_id)

    def __get_user_name(self):
        first_name = self.message['from']['first_name']
        last_name = self.message['from']['last_name'] if 'last_name' in self.message['from'] else ''

        nickname = self.message['from']['username'] if 'username' in self.message['from'] else ''
        return f'{first_name} {last_name}', nickname

    def sign(self):
        user_id = self.message['chat']['id']
        user_name, user_nickname = self.__get_user_name()
        user = self.userAPI.get_user(user_id)
        if user:
            self.telegramBotAPI.send_message(content.company_change, user_id, keyboards.MAIN_MENU)
            return
        text = self.message['text']
        text_parsed = text.split(' ')
        if len(text_parsed) != 2:
            self.telegramBotAPI.send_message(content.company_code_incorrect, user_id)
            return
        company_id = text_parsed[1]
        user_params = {
            'id': str(user_id),
            'company_id': company_id,
            'name': user_name
        }
        if user_nickname:
            user_params['nickname'] = user_nickname
        company = self.userAPI.add_user(user_params)
        if company:
            self.telegramBotAPI.send_message(content.company_welcome.format(company['name']), user_id, keyboards.MAIN_MENU)
        else:
            self.telegramBotAPI.send_message(content.company_404, user_id)

    def lunch(self):
        user_id = self.message['chat']['id']
        text = self.message['text']
        text_parsed = text.split(' ')
        if len(text_parsed) == 1:
            self.telegramBotAPI.send_message(content.lunch_incorrect, user_id)
            return

        lunch_name = ' '.join(text_parsed[1:])

        user = self.userAPI.get_user(user_id)

        if user['lunch_id'] is not None:
            self.lunchAPI.change_lunch_votes_count(user['lunch_id'], -1)
        new_lunch_id = self.lunchAPI.add_lunch(lunch_name, user['company_id'])
        change_user_lunch_response = self.userAPI.update_user_lunch_id(user['id'], new_lunch_id)

        message_text = ''
        if change_user_lunch_response.ok:
            message_text =  content.lunch_success
        else:
            message_text = content.error_common
        self.telegramBotAPI.send_message(message_text, user_id, keyboards.BACK_MENU)

    def help(self):
        user_id = self.message['chat']['id']
        self.telegramBotAPI.send_message(content.help_message, user_id)

    def unknown(self):
        user_id = self.message['chat']['id']
        self.telegramBotAPI.send_message(content.error_unknown_command, user_id)

class Callback(Handler):
    def __init__(self, callback_query) -> None:
        super().__init__()

        self.presenceMenu = PresenceMenu()
        self.mainMenu = MainMenu()
        self.officeMenu = OfficeMenu()
        self.lunchMenu = LunchMenu()

        self.user_id = str(callback_query['message']['chat']['id'])
        self.message_id = str(callback_query['message']['message_id'])
        self.button = callback_query['data']

        user = self.userAPI.get_user(self.user_id)

        if not user:
            self.unknown_user()

        elif self.button == Button.BACK.value:
            self.show_main_menu()

        elif self.button == Button.OFFICE.value:
            self.show_office_menu()

        elif self.button == Button.LUNCH_SHOW.value:
            self.show_lunch_menu()

        elif self.button == Button.PRESENCE_FALSE.value:
            self.toggle_presence(False)

        elif self.button == Button.PRESENCE_TRUE.value:
            self.toggle_presence(True)

        elif Button.LUNCH_VOTE.value in self.button:
            self.vote()

    def show_main_menu(self):
        self.mainMenu.show(self.user_id, self.message_id)
    
    def show_office_menu(self):
        self.officeMenu.show(self.user_id, self.message_id)

    def show_lunch_menu(self):
        self.lunchMenu.show(self.user_id, self.message_id)

    def toggle_presence(self, new_presence):
        response = self.userAPI.toggle_user_presence(self.user_id, new_presence)

        if response.ok:
            self.presenceMenu.show(self.user_id, self.message_id, new_presence)
        else:
            self.telegramBotAPI.edit_message(content.error_common, self.user_id, self.message_id, keyboards.BACK_MENU)

    def vote(self):
        button_parsed = self.button.split('_')

        if len(button_parsed) != 3:
            self.telegramBotAPI.send_message(content.error_common, self.user_id, keyboards.BACK_MENU)
            return

        new_lunch_id = int(button_parsed[2])
        user = self.userAPI.get_user(self.user_id)

        if user['lunch_id'] == new_lunch_id:
            self.telegramBotAPI.edit_message(content.vote_double, self.user_id, self.message_id, keyboards.BACK_MENU)
            return

        user_update_response = self.userAPI.update_user_lunch_id(self.user_id, new_lunch_id)
        if user['lunch_id'] is not None:
            self.lunchAPI.change_lunch_votes_count(user['lunch_id'], -1)
        new_lunch_update_response = self.lunchAPI.change_lunch_votes_count(new_lunch_id, 1)

        message_text = ''
        if user_update_response.ok and new_lunch_update_response.ok:
            message_text = content.vote_success
        else:
            message_text = content.error_common
        self.telegramBotAPI.edit_message(message_text, self.user_id, self.message_id, keyboards.BACK_MENU)

    def unknown_user(self):
        message_text = content.hello_message
        self.telegramBotAPI.edit_message(message_text, self.user_id, self.message_id)
