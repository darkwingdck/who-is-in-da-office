hello_message = '''
    👋 *Привет! На связи бот WIIDO*.\n\nЧтобы начать пользоваться ботом, тебе нужно узнать у коллег секретный код компании. После этого ты сможешь узнать, кто придет завтра в офис и куда планируют идти на обед!\n\nВведи /sign <код своей компании>, чтобы зарегистрироваться.\n\nP.S. Если ты хочешь протестировать работу бота, введи\n`/sign test-pass`
'''
help_message = '''
/sign <код компании> - зарегистрироваться. Чтобы узнать код компании, обратись к коллегам.
/lunch <название> - предложить вариант обеда
/start - перезапуск бота
/help - помощь\n
Если остались вопросы, напиши [мне в личные сообщения](https://t.me/darkwingdck)
'''

office = '💼 Кто завтра в офис?'
lunch = '🥪 Что завтра на обед?'
back = '« Назад'

choose_option = 'Выбери одну из опций'

company_code_incorrect = '✍️  Чтобы зарегистрироваться, введи /sign <код компании>.\nНапример, `/sign test-pass`'
company_welcome = '✨ Добро пожаловать в компанию *{0}*!'
company_404 = '🤔 Кажется, такой компании пока не существует('
company_change = 'Пока поменять компанию можно только через [человека, который лишил тебя этой фичи](https://t.me/darkwingdck)'

lunch_incorrect = '✍️  Чтобы предложить вариант, набери /lunch <название варианта>.\nНапример, `/lunch Раменная на углу`'
lunch_success = '✨ *Прекрасно!* ✨\n\nЯ записал твой вариант, можешь звать друзей голосовать'
lunch_variants = '*Вот варианты, которые предолжили твои коллеги*\n\nТы можешь проголосовать, либо добавить свой вариант, введя команду /lunch <название варианта>.\nНапример, `/lunch Те вкусные блины в соседнем здании`'
lunch_empty = '*Пусто!*\n\nПохоже, пока никто не предложил, куда сходить на обед. Чтобы добавить варинт, набери команду /lunch <название варианта>.\nНапример, `/lunch Плов`'

users_list = 'Вот список людей, которые идут завтра в офис:\n\n'
office_empty = 'Похоже, пока в офис никто не собирается. Будь первым!'

error_common = 'Что-то пошло не так! Попробуй позвать на помощь [автора этого бага](https://t.me/darkwingdck)'
error_unknown_command = '🧐 Не понимаю тебя. Нажми /help для списка доступных команд'

vote_double = 'Ты уже проголосовал за этот вариант'
vote_success = 'Ваш голос очень важен для нас!'

presence_true = '💼 Я завтра в офис!'
presence_false = '🏠 Останусь завтра дома!'
presence_true_response = '✨ *Отлично!* ✨\n\nБудем рады видеть тебя в офисе'
presence_false_response = '🥺 Увидимся в следующий раз!'
