from pony.orm import *
from db import *
from dateutil import parser as dt_parser
from utils import get_random_nickname, LEAGUES, LEVELS, LEVEL_TO_LEAGUES, LEAGUES_TO_SIZE
import random


@db_session
def show_user(update, context):
    user = User.get(telegram_id=update.message.from_user.id)
    team_name = user.team.name if user.team is not None else 'Нету ;('
    reply_text = f'''Сейчас у тебя:\n💰 Олегро 💰: \t\t\t{user.coins}\n⚡️Энергия⚡️ : \t\t\t{user.energy}\n\n🎭 Команда 🎭:\t\t\t{team_name}'''
    if user.team is not None:
        reply_text += f'\n🎗Лига команды🎗 :\t\t\t{get_team_league(user.team)}\n'
        reply_text += f'📊 Рейтинг команды в лиге📊 :\t\t\t{get_team_rating(user.team)}'


    update.message.reply_text(reply_text)

@db_session
def list_user_team(update, context):
    user = User.get(telegram_id=update.message.from_user.id)
    if user.team is None:
        update.message.reply_text("У вас нет команды!")
    else:
        team = user.team
        text = get_team_position(update, context)
        update.message.reply_text(text + '\n\nСписок участников команды:\n' + '\n'.join([f"{i+1} - {user.first_name} {user.username} - {user.coins} олегро" for i, user in enumerate(sorted(team.users, key=lambda x: x.coins, reverse=True))]))


def is_team_available(team, user):
    team_league = get_team_league(team)
    if team_league not in LEVEL_TO_LEAGUES[get_user_level(user)]:
        return False
    if len(team.users) >= LEAGUES_TO_SIZE[team_league]:
        return False
    return True

@db_session
def print_team_list(update, context):
    current_user = get_user(update.message.from_user.id)
    teams = sorted(select(team for team in Team)[:], key=lambda x: x.name)

    teams = [team for team in teams if is_team_available(team, current_user)][:40]
    reply_text = "Cписок доступных команд:\n"
    reply_text += '\n'.join([f"{team.name} - {len(team.users)} participants" for i, team in enumerate(teams)])
    update.message.reply_text(reply_text)

@db_session
def print_user_rating(update, context):
    users = sorted(select(user for user in User)[:], key=lambda user: user.coins, reverse=True)
    current_user = get_user(update.message.from_user.id)

    reply_text = f"Вы на {users.index(current_user) + 1} месте с состоянием в {current_user.coins} олегро."
    reply_text += "\nТоп-30 успешных людей:\n"
    reply_text += '\n'.join([f"{i + 1} - {user.first_name} {user.username} - {user.coins} олегро" for i, user in enumerate(users[:30])])
    update.message.reply_text(reply_text)

@db_session
def print_team_rating(update, context, page=1):
    teams = sorted(select(team for team in Team)[:], key=lambda team: get_team_coins(team), reverse=True)
    current_user = get_user(update.message.from_user.id)
    if current_user.team is None:
        reply_text = 'У вас нет команды. Вступите в команду чтобы участвовать в еженедельном рейтинге команд. Вы можете сделать это в своём профиле.'
        reply_text += 'Все члены выигравшей команды получают очки, на которые они могут кастомизировать Олега.'
        update.message.reply_text(reply_text)
    else:
        league = get_team_league(current_user.team)
        teams = [team for team in teams if get_team_league(team) == league]
        reply_text = f"{league} Лига.\nВaша команда {current_user.team.name} cейчас на {teams.index(current_user.team) + 1} месте с состоянием в {get_team_coins(current_user.team)} олегро."
        reply_text += "\nРейтинг команд лиги:\n"
        reply_text += '\n'.join([f"{i + 1} - {team.name} - {get_team_coins(team)} олегро" for i, team in enumerate(teams[:10])])
        update.message.reply_text(reply_text)

@db_session
def get_team_position(update, context):
    teams = sorted(select(team for team in Team)[:], key=lambda team: get_team_coins(team), reverse=True)
    current_user = get_user(update.message.from_user.id)
    league = get_team_league(current_user.team)
    teams = [team for team in teams if get_team_league(team) == league]
    reply_text = f"{league} Лига.\nВaша команда {current_user.team.name} cейчас на {teams.index(current_user.team) + 1} месте с состоянием в {get_team_coins(current_user.team)} олегро."
    return reply_text

@db_session
def assign_team(update, context):
    team_name = update.message.text
    user = update.message.from_user.id
    add_user_to_team(user, team_name)
    show_user(update, context)

@db_session
def change_state(user, state):
    user = User.get(id=user.id)
    user.state = state

@db_session
def change_money(update, money):
    user = User.get(telegram_id=update.message.from_user.id)
    user.coins += money

@db_session
def change_energy(update):
    user = User.get(telegram_id=update.message.from_user.id)
    user.energy = max(0, user.energy - 1)

@db_session
def change_team(user, team):
    user = User.get(id=user.id)
    user.team = team

@db_session
def changing_bots_callback(context):
    bots = select(user for user in User if len(user.last_name) == 1)[:]
    for bot in bots:
        bot.coins += random.randint(int(-0.005*bot.coins), int(0.005*bot.coins))

@db_session
def energy_callback(context):
    users = select(user for user in User)[:]
    for user in users:
        user.energy = min(10, user.energy + 1)

@db_session
def add_user_message(update):
    user = User.get(telegram_id=update.message.from_user.id)
    if user is None:
        user = User.user_from_update(update)
    # message = Message.message_from_update(update, user)
    # user.messages.add(message)
    return user

@db_session
def get_user(telegram_id):
    return User.get(telegram_id=telegram_id)

@db_session
def get_user_by_username(username):
    return User.get(username=username)

@db_session
def get_user_rating(current_user):
    users = sorted(select(user for user in User)[:], key=lambda user: user.coins, reverse=True)
    return users.index(current_user) + 1

def get_user_level(user):
    for level, (low, high) in LEVELS.items():
        if low <= user.coins < high:
            return level

@db_session
def get_team_rating(current_team):
    league = get_team_league(current_team)
    teams = sorted(select(team for team in Team)[:], key=lambda team: get_team_coins(team), reverse=True)
    teams = [team for team in teams if get_team_league(team) == league]
    return teams.index(current_team) + 1

@db_session
def get_or_create_user(telegram_id):
    temp_workspace = get_user(telegram_id)
    return temp_workspace if temp_workspace is not None else User(telegram_id=telegram_id)


@db_session
def get_team(name):
    return Team.get(name=name)


@db_session
def get_energy(update):
    user = User.get(telegram_id=update.message.from_user.id)
    return user.energy

@db_session
def get_or_create_team(name):
    temp_team = get_team(name)
    return temp_team if temp_team is not None else Team(name=name, league=LEAGUES[0])


@db_session
def add_user_to_team(user, team):
    if not isinstance(user, User):
        user = get_user(user)
        if user is None:
            raise ValueError('user is None')
    if not isinstance(team, Team):
        team = get_or_create_team(team)
    team.users.add(user)
    change_team(user, team)


def get_team_coins(team):
    capital = 0
    for user in team.users:
        capital += user.coins
    return capital

@db_session
def weekly_rating_callback(context):
    all_teams = sorted(select(team for team in Team)[:], key=lambda team: get_team_coins(team), reverse=True)
    for i, league in enumerate(LEAGUES):
        teams = [team for team in all_teams if get_team_league(team) == league]
        for team in teams[:int(len(teams) * 0.3)]:
            team.league = LEAGUES[i+1]


def get_team_league(team):
    return team.league


def eval_team_league(team):
    capital = 0
    for user in team.users:
        capital += user.coins
    for league, (low, high) in LEAGUES.items():
        if low <= capital < high:
            return league

@db_session
def generate_teams(num=11):
    for i in range(num):
        team = get_or_create_team(get_random_nickname())
        users = [User.random_user() for i in range(random.randint(2, 25))]
        commit()
        for user in users:
            add_user_to_team(user, team)


@db_session
def get_money(update, context):
    user = User.get(telegram_id=update.message.from_user.id)
    return user.coins
