from enum import Enum

class Command(Enum):
    START = '/start'
    SIGN_UP = '/sign_up'
    LUNCH = '/lunch'

class Button(Enum):
    OFFICE = 'office'
    LUNCH_SHOW = 'lunch_show'
    LUNCH_VOTE = 'lunch_vote'
    BACK = 'back'
    PRESENCE_TRUE = 'presence_true'
    PRESENCE_FALSE = 'presence_false'
