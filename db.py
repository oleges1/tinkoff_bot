from datetime import datetime, timedelta
from pony.orm import *
from utils import generate_bot_data



db = Database()


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    telegram_id = Optional(int, nullable=True)
    first_name = Optional(str, nullable=True)
    last_name = Optional(str, nullable=True)
    username = Optional(str, nullable=True)
    state = Optional(str, nullable=True)
    coins = Optional(int, nullable=True)
    energy = Optional(int, nullable=True)
    exp = Optional(int, nullable=True)
    team = Optional('Team', nullable=True)

    @staticmethod
    def random_user():
        return User(
            **generate_bot_data()
        )

    @staticmethod
    def user_from_update(update):
        from_user = update.message.from_user
        return User(
            telegram_id=from_user.id,
            first_name=from_user.first_name,
            last_name=from_user.last_name,
            username=from_user.username,
            coins=100,
            state='start',
            energy=10
        )


class Team(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    users = Set(User)
    league = Optional(str)

    # TODO: admins = Set(User)


# class Location(db.Entity):
#     id = PrimaryKey(int, auto=True)
#     name = Optional(str)
#     meetings = Set('Meeting')
#     workspace = Required(Workspace)
#
#
# class Meeting(db.Entity):
#     id = PrimaryKey(int, auto=True)
#     name = Optional(str)
#     users = Set(User)
#     location = Required(Location)
#     start_time = Optional(datetime)
#     end_time = Optional(datetime)


db.bind(provider='sqlite', filename='sql', create_db=True)
db.generate_mapping(create_tables=True)


states = {
    'start': {
        'buttons' : [
            ['🌐Форум🌐', '📈Биржа📈', '🧐Квизы🧐'],
            ['Профиль','🏆Рейтинг команд🏆'],
        ],
        'text' : """Ты можешь отправиться на:

🌐Форум🌐 - за финансовыми сражениями

📈Биржу📈 - испытать удачу

🧐Квизы🧐 - проверить свою финансовую грамотность и поотвечать на интересные вопросы :)

Или заглянуть в профиль""",
    },


    'stock' : {
        'buttons' : [
            ['Готов!'],
            ['Назад🔙']
        ],
        'text' : 'Ты пришел на биржу. Заходя в игру, ты увидишь курс акций какой-то компании за последние сутки. Чтобы не раскрывать дополнительные данные о компании, назовем ее "Оргело". Твоей целью будет предсказать, повысится или понизиться курс в течение следующих 12 часов. Готов сыграть?'
    },

    # 'oleg' : {
    #     'buttons' : [
    #         ['Олег'],
    #         ['Назад🔙', 'Меню📋']
    #     ],
    #     'text' : 'Олег'
    # },

    'bet' : {
        'buttons' : [
            ['Вверх☝️', 'Вниз👇'],
            ['Назад🔙', 'Меню📋']
        ],
        'text' : 'Спрогнозируй, в какую сторону пойдет график курса '
    },

    'bet up' : {
        'buttons' : [['Назад🔙']],
        'text' : 'Ты решил играть на повышение. Сколько олегро ты готов поставить на то, что курс повысится?'
    },

    'bet down' : {
        'buttons' : [['Назад🔙']],
        'text' : 'Ты решил играть на понижение. Сколько олегро ты готов поставить на то, что курс понизится?'
    },

    'results_win' : {
        'buttons' : [['Назад🔙', 'Меню📋']],
        'text' : 'Ты абсолютно прав! Можешь посмотреть на то, каким дальше был график и отпраздновать победу!'
    },

    'results_lose' : {
        'buttons' : [['Назад🔙', 'Меню📋']],
        'text' : 'К сожалению, твой прогноз оказался неверен. Можешь посмотреть на то, каким дальше был график.'
    },

    'results_draw' : {
        'buttons' : [['Назад🔙', 'Меню📋']],
        'text' : 'Это какая-то мистика, но через 12 часов значения курса ровно такие же, как и в конце периода, который ты наблюдал! Мы вернем тебе деньги за ставку.'
    },

    'profile': {
        'buttons' : [['Статус', 'Моя команда', 'Поиск команды'], ['Назад🔙', 'Меню📋']],
        'text': 'Это профиль твоего персонажа.'
    },

    'teaming': {
        'buttons': [['Назад🔙', 'Меню📋']],
        'text': 'Напиши сюда название команды и я либо создам такую команду, либо отыщу её'
    },
    'game': {
        'buttons': [['Готов 💪'], ['Назад🔙', 'Меню📋']],
        'text': 'Привет. Я приготовил для тебя парочку интересных вопросов. За правильные ответы ты будешь получать немного олегпро 💰 и опыта. Готов?'
    },
    'game2': {},
    'game3': {
        'buttons': [['Назад🔙', 'Меню📋'], ['Продолжаем!']],
        'text': 'Ну что еще разок?'
    },
}
