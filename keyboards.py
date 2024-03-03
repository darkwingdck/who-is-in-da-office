import content

from constants import Button

MAIN_MENU = {
    'inline_keyboard': [
        [
            {
                'text': content.office,
                'callback_data': Button.OFFICE.value
            },
            {
                'text': content.lunch,
                'callback_data': Button.LUNCH.value
            }
        ]
    ]
}

OFFICE_MENU_PRESENCE_TRUE = {
    'inline_keyboard': [
        [
            {
                'text': content.back,
                'callback_data': Button.BACK.value
            },
            {
                'text': content.presence_true,
                'callback_data': Button.PRESENCE_TRUE.value
            }
        ]
    ]
}

OFFICE_MENU_PRESENCE_FALSE = {
    'inline_keyboard': [
        [
            {
                'text': content.back,
                'callback_data': Button.BACK.value
            },
            {
                'text': content.presence_false,
                'callback_data': Button.PRESENCE_FALSE.value
            }
        ]
    ]
}

LUNCH_MENU = {
    'inline_keyboard': [
        [
            {
                'text': content.back,
                'callback_data': Button.BACK.value
            }
        ]
    ]
}
