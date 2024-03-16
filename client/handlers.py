import keyboards
import content

from presenters import MainMenu, LunchMenu, OfficeMenu, PresenceMenu
from service import TelegramBotAPI, UserAPI, LunchAPI
from constants import Button, Command

class Handler:
    def __init__(self, user_id) -> None:
        self.telegramBotAPI = TelegramBotAPI(user_id)
        self.userAPI = UserAPI()
        self.lunchAPI = LunchAPI()

class Message(Handler):
    def __init__(self, message) -> None:
        self.user_id = str(self.message['chat']['id'])
        super().__init__(self.user_id)

        self.message = message
        self.text = self.message['text']
        self.command_args = self.text.split(' ')
        self.user = self.userAPI.get_user(self.user_id)

        self.mainMenu = MainMenu(self.user_id)

        if Command.START.value in self.text:
            self.start()

        elif Command.SIGN.value in self.text:
            self.sign()

        elif Command.LUNCH.value in self.text:
            self.lunch()

        elif Command.HELP.value in self.text:
            self.help()

        else:
            self.unknown_command()

    def start(self):
        if self.user:
            self.mainMenu.show()
        else:
            self.telegramBotAPI.send_message(content.hello_message, self.user_id)

    def __get_user_name(self):
        first_name = self.message['from']['first_name']
        last_name = self.message['from']['last_name'] if 'last_name' in self.message['from'] else ''
        nickname = self.message['from']['username'] if 'username' in self.message['from'] else ''

        return f'{first_name} {last_name}', nickname

    def sign(self):
        if self.user:
            self.telegramBotAPI.send_message(content.company_change, keyboards.MAIN_MENU)
            return

        if len(self.command_args) != 2:
            self.telegramBotAPI.send_message(content.company_code_incorrect)
            return

        user_name, user_nickname = self.__get_user_name()
        user_company_id = self.command_args[1]
        user_params = {
            'id': self.user_id,
            'company_id': user_company_id,
            'name': user_name
        }
        if user_nickname:
            user_params['nickname'] = user_nickname
        company = self.userAPI.add_user(user_params)

        if company:
            self.telegramBotAPI.send_message(content.company_welcome.format(company['name']), keyboards.MAIN_MENU)
        else:
            self.telegramBotAPI.send_message(content.company_404)

    def lunch(self):
        if len(self.command_args) == 1:
            self.telegramBotAPI.send_message(content.lunch_incorrect)
            return

        if not self.user:
            self.telegramBotAPI.send_message(content.hello_message)
            return

        if self.user['lunch_id'] is not None:
            self.lunchAPI.change_lunch_votes_count(self.user['lunch_id'], -1)

        new_lunch_name = ' '.join(self.command_args[1:])
        new_lunch_id = self.lunchAPI.add_lunch(new_lunch_name, self.user['company_id'])

        response = self.userAPI.update_user_lunch_id(self.user['id'], new_lunch_id)
        message_text = content.lunch_success if response.ok else content.error_common

        self.telegramBotAPI.send_message(message_text, keyboards.BACK_MENU)

    def help(self):
        self.telegramBotAPI.send_message(content.help_message)

    def unknown_command(self):
        self.telegramBotAPI.send_message(content.error_unknown_command)

class Callback(Handler):
    def __init__(self, callback_query) -> None:
        self.user_id = str(callback_query['message']['chat']['id'])
        super().__init__(self.user_id)

        self.message_id = str(callback_query['message']['message_id'])
        self.button = callback_query['data']

        self.presenceMenu = PresenceMenu(self.user_id, self.message_id)
        self.mainMenu = MainMenu(self.user_id, self.message_id)
        self.officeMenu = OfficeMenu(self.user_id, self.message_id)
        self.lunchMenu = LunchMenu(self.user_id, self.message_id)

        self.user = self.userAPI.get_user(self.user_id)

        if not self.user:
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
        self.mainMenu.show()
    
    def show_office_menu(self):
        self.officeMenu.show()

    def show_lunch_menu(self):
        self.lunchMenu.show()

    def toggle_presence(self, new_presence):
        response = self.userAPI.toggle_user_presence(self.user_id, new_presence)

        if response.ok:
            self.presenceMenu.show(new_presence)
        else:
            self.telegramBotAPI.edit_message(content.error_common, self.message_id, keyboards.BACK_MENU)

    def vote(self):
        button_parsed = self.button.split('_')

        if len(button_parsed) != 3:
            self.telegramBotAPI.send_message(content.error_common, keyboards.BACK_MENU)
            return

        new_lunch_id = int(button_parsed[2])

        if self.user['lunch_id'] == new_lunch_id:
            self.telegramBotAPI.edit_message(content.vote_double, self.message_id, keyboards.BACK_MENU)
            return

        user_update_response = self.userAPI.update_user_lunch_id(self.user_id, new_lunch_id)
        if self.user['lunch_id'] is not None:
            self.lunchAPI.change_lunch_votes_count(self.user['lunch_id'], -1)
        new_lunch_update_response = self.lunchAPI.change_lunch_votes_count(new_lunch_id, 1)

        message_text = ''
        if user_update_response.ok and new_lunch_update_response.ok:
            message_text = content.vote_success
        else:
            message_text = content.error_common
        self.telegramBotAPI.edit_message(message_text, self.message_id, keyboards.BACK_MENU)

    def unknown_user(self):
        self.telegramBotAPI.edit_message(content.hello_message, self.message_id)
