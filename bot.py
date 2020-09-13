import telegram
import argparse
import logging
import requests

from telegram.ext import Updater
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, InputTextMessageContent,
                      ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, CallbackQueryHandler,
                          Filters, RegexHandler, ConversationHandler)
from selects import *
from locations import *
from functools import partial
from utils import get_random_quiz

from stock import *
import requests

from selects import change_money, get_money


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def plot_action(update, context, args, transfer_to=None):
    user = add_user_message(update)
    logger.info('%s\n%s' %(user.username, user.state))
    state_name = user.state if transfer_to is None else transfer_to
    cur_state = states[state_name]

    chat_id = user.telegram_id

    reply_keyboard = cur_state['buttons']
    reply_markup = ReplyKeyboardMarkup(reply_keyboard)
    sample(chat_id)
    plot_obs(chat_id, stock_stats[chat_id]['obs'])

    files = {'photo' : open('obs' + str(chat_id) + '.png', 'rb')}
    status = requests.post('https://api.telegram.org/bot' + args.token + '/sendPhoto?chat_id=' + str(chat_id), files=files)

    update.message.reply_text(cur_state['text'], reply_markup=reply_markup)

    return state_name


def bet_action_up(update, context, args, transfer_to=None):
    user = add_user_message(update)
    logger.info('%s\n%s' %(user.username, user.state))

    bet = int(update.message.text)

    money = get_money(update, context)
    if money < bet:
        state_name = user.state
        cur_state = states[state_name]
        reply_keyboard = cur_state['buttons']
        reply_markup = ReplyKeyboardMarkup(reply_keyboard)
        update.message.reply_text('Ты не можешь поставить больше, чем имеешь! Введи значение заново', reply_markup=reply_markup)
        return state_name



    chat_id = user.telegram_id
    plot_all(chat_id, stock_stats[chat_id]['obs'], stock_stats[chat_id]['test'])

    files = {'photo' : open('all' + str(chat_id) + '.png', 'rb')}
    status = requests.post('https://api.telegram.org/bot' + args.token + '/sendPhoto?chat_id=' + str(chat_id), files=files)
    stock_stats[chat_id]['bet'] = bet

    if stock_stats[chat_id]['test'][-1] > stock_stats[chat_id]['obs'][-1]:
        state_name = 'results_win'
        change_money(update, bet)
    elif stock_stats[chat_id]['test'][-1] < stock_stats[chat_id]['obs'][-1]:
        state_name = 'results_lose'
        change_money(update, -bet)
    else:
        state_name = 'results_draw'

    cur_state = states[state_name]
    reply_keyboard = cur_state['buttons']
    reply_markup = ReplyKeyboardMarkup(reply_keyboard)
    update.message.reply_text(cur_state['text'], reply_markup=reply_markup)

    return state_name


def bet_action_down(update, context, args, transfer_to=None):
    user = add_user_message(update)
    logger.info('%s\n%s' %(user.username, user.state))

    bet = int(update.message.text)

    money = get_money(update, context)
    if money < bet:
        state_name = user.state
        cur_state = states[state_name]
        reply_keyboard = cur_state['buttons']
        reply_markup = ReplyKeyboardMarkup(reply_keyboard)
        update.message.reply_text('Ты не можешь поставить больше, чем имеешь! Введи значение заново', reply_markup=reply_markup)
        return state_name


    chat_id = user.telegram_id
    plot_all(chat_id, stock_stats[chat_id]['obs'], stock_stats[chat_id]['test'])

    files = {'photo' : open('all' + str(chat_id) + '.png', 'rb')}
    status = requests.post('https://api.telegram.org/bot' + args.token + '/sendPhoto?chat_id=' + str(chat_id), files=files)
    stock_stats[chat_id]['bet'] = bet

    if stock_stats[chat_id]['test'][-1] > stock_stats[chat_id]['obs'][-1]:
        state_name = 'results_lose'
        change_money(update, -bet)
    elif stock_stats[chat_id]['test'][-1] < stock_stats[chat_id]['obs'][-1]:
        state_name = 'results_win'
        change_money(update, bet)
    else:
        state_name = 'results_draw'

    cur_state = states[state_name]
    reply_keyboard = cur_state['buttons']
    reply_markup = ReplyKeyboardMarkup(reply_keyboard)
    update.message.reply_text(cur_state['text'], reply_markup=reply_markup)

    return state_name


def leave_stock_action(update, context, transfer_to=None):
    user = add_user_message(update)
    logger.info('%s\n%s' %(user.username, user.state))
    state_name = user.state if transfer_to is None else transfer_to
    change_state(user, state_name)
    cur_state = states[state_name]

    logger.info(cur_state)

    chat_id = user.telegram_id
    stock_stats.pop(chat_id)

    reply_keyboard = cur_state['buttons']
    reply_markup = ReplyKeyboardMarkup(reply_keyboard)

    update.message.reply_text(cur_state['text'], reply_markup=reply_markup)

    return state_name

def show_answer(update, context):
    right_answer = context.user_data['right_answer']
    user_answer = update.message.text
    if right_answer.lower().strip() == user_answer.lower().strip():
        reply_text = 'Отлично! +15 олегро 💰 за смекалку. '
        change_money(update, 15)
    else:
        reply_text = 'Не верно! На самом деле: ' + right_answer + '\n -5 олегро 💰.'
        change_money(update, -5)
    update.message.reply_text(reply_text)
    return False

def show_question(update, context):
    quiz, right_answer = get_random_quiz()
    context.user_data['right_answer'] = right_answer[3:]
    reply_text = '\n'.join(quiz)
    reply_keyboard = [[quiz[1][3:], quiz[2][3:]], [quiz[3][3:], quiz[4][3:]], ['Назад🔙', 'Меню📋']]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard)
    update.message.reply_text(reply_text, reply_markup=reply_markup)
    return True


def start_stock_action(update, context, transfer_to=None):
    user = add_user_message(update)
    logger.info('%s\n%s' %(user.username, user.state))
    state_name = user.state if transfer_to is None else transfer_to
    change_state(user, state_name)
    cur_state = states[state_name]

    logger.info(cur_state)

    money = get_money(update, context)
    add_text = '\nУ тебя целых ' + str(money) + ' олегро!'
    reply_keyboard = cur_state['buttons']
    reply_markup = ReplyKeyboardMarkup(reply_keyboard)

    update.message.reply_text(cur_state['text'] + add_text, reply_markup=reply_markup)

    return state_name


def action(update, context, additional_action=None, transfer_to=None):
    user = add_user_message(update)
    logger.info('%s\n%s' %(user.username, user.state))
    state_name = user.state if transfer_to is None else transfer_to
    change_state(user, state_name)
    cur_state = states[state_name]

    logger.info(cur_state)
    replied = False
    if additional_action is not None:
        replied = additional_action(update, context)
    if not replied:
        reply_keyboard = cur_state['buttons']
        reply_markup = ReplyKeyboardMarkup(reply_keyboard)

        update.message.reply_text(cur_state['text'], reply_markup=reply_markup)

    return state_name


def help(update, context):
    update.message.reply_text('''Чтобы начать взаимодействие с ботом, напиши /start. Если что-то пойдет не так и бот сломается (вдруг), пожалуйста, напиши сначала /cancel,а после /start''')


def error(update, context, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! Come again to play game!',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', type=str, default='no-token :)')
    return parser.parse_args(args)


def main():
    args = parse_args(None)
    updater = Updater(token=args.token, use_context=True)
    j = updater.job_queue
    # updater = Updater(TOKEN, request_kwargs=REQUEST_KWARGS)
    generate_teams(num=25)

    bot_changing_job = j.run_repeating(changing_bots_callback, interval=20, first=0)

    weekly_rating_job = j.run_repeating(weekly_rating_callback, interval=60 * 2, first=0)

    energy_job = j.run_repeating(energy_callback, interval=60 * 2, first=0)


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', partial(action, transfer_to='start'))],

        states={
            'start': [
                RegexHandler('🌐Форум🌐', forum),
                RegexHandler('Обучение Олега', partial(action, transfer_to='oleg')),
                RegexHandler('📈Биржа📈', partial(start_stock_action, transfer_to='stock')),
                RegexHandler('Квизы', partial(action, transfer_to='game')),
                RegexHandler('Рейтинг команд🏆', partial(action, transfer_to='start', additional_action=print_team_rating)),
                RegexHandler('Профиль', partial(action, transfer_to='profile')),
                RegexHandler(
                    '^((?!(🌐Форум🌐)|(📈Биржа📈)|(Обучение Олега)).)*$', partial(action, transfer_to='start'))
            ],
            'forum': [
                RegexHandler('Подойти к рационалистам', forum_game, pass_user_data=True),
                RegexHandler('Уйти', partial(action, transfer_to='start'))
            ],
            'forum_game' : [
                RegexHandler('Да', forum_game_play, pass_user_data=True),
                RegexHandler('Нет', partial(action, transfer_to='start'))
            ],
            'forum_game_playing' : [
                MessageHandler(Filters.text, forum_game_check, pass_user_data=True)
            ],

            'stock': [
                RegexHandler('Готов!', partial(plot_action, args=args, transfer_to='bet')),
                RegexHandler('Назад🔙', partial(action, transfer_to='start')),
            ],

            'bet' : [
                RegexHandler('Вверх☝️', partial(action, transfer_to='bet up')),
                RegexHandler('Вниз👇', partial(action, transfer_to='bet down')),
                RegexHandler('Назад🔙', partial(action, transfer_to='stock')),
                RegexHandler('Меню📋', partial(action, transfer_to='start')),
            ],

            'bet up' : [
                RegexHandler('^[0-9]', partial(bet_action_up, args=args)),
                RegexHandler('Назад🔙', partial(action, transfer_to='bet')),
            ],

            'bet down' : [
                RegexHandler('^[0-9]', partial(bet_action_down, args=args)),
                RegexHandler('Назад🔙', partial(action, transfer_to='bet')),
            ],

            'results_win' : [
                RegexHandler('Назад🔙', partial(leave_stock_action, transfer_to='stock')),
                RegexHandler('Меню📋', partial(action, transfer_to='start')),
            ],

            'results_lose' : [
                RegexHandler('Назад🔙', partial(leave_stock_action, transfer_to='stock')),
                RegexHandler('Меню📋', partial(action, transfer_to='start')),
            ],

            'results_draw' : [
                RegexHandler('Назад🔙', partial(leave_stock_action, transfer_to='stock')),
                RegexHandler('Меню📋', partial(action, transfer_to='start')),
            ],

            # 'oleg' : [
            #     RegexHandler('Назад🔙', partial(action, transfer_to='start')),
            #     RegexHandler('Меню📋', partial(action, transfer_to='start')),
            #
            # ],

            'profile': [
                RegexHandler('Поиск команды', partial(action, transfer_to='teaming', additional_action=print_team_list)),
                RegexHandler('Моя команда', partial(action, transfer_to='profile', additional_action=list_user_team)),
                RegexHandler('Статус', partial(action, transfer_to='profile', additional_action=show_user)),
                RegexHandler('Назад🔙', partial(action, transfer_to='start')),
                RegexHandler('Меню📋', partial(action, transfer_to='start')),
            ],
            'teaming':[
                RegexHandler('Назад🔙', partial(action, transfer_to='profile')),
                RegexHandler('Меню📋', partial(action, transfer_to='start')),
                RegexHandler('^([a-z]|[A-Z]|[а-я]|[A-Я])', partial(action, transfer_to='profile', additional_action=assign_team)),

            ],
            'game': [
                RegexHandler('Назад🔙', partial(action, transfer_to='start')),
                RegexHandler('Меню📋', partial(action, transfer_to='start')),
                RegexHandler(
                    '^((?!(Назад🔙)|(Меню📋)).)*$', partial(action, transfer_to='game2', additional_action=show_question), pass_user_data=True)
            ],
            'game2': [
                RegexHandler('Назад🔙', partial(action, transfer_to='game')),
                RegexHandler('Меню📋', partial(action, transfer_to='start')),
                RegexHandler('^((?!(Назад🔙)|(Меню📋)).)*$', partial(action, transfer_to='game3', additional_action=show_answer), pass_user_data=True)
            ],
            'game3': [
                RegexHandler('Назад🔙', partial(action, transfer_to='game')),
                RegexHandler('Меню📋', partial(action, transfer_to='start')),
                RegexHandler('Продолжаем!', partial(action, transfer_to='game'), pass_user_data=True)
            ],
        },

        fallbacks=[CommandHandler('cancel', cancel),
                   CommandHandler('help', help)]
    )
    # conv_handler.states.update(list_of_meetings_states)
    # conv_handler.states.update(workspace_states)
    # conv_handler.states.update(cancel_states)
    # conv_handler.states.update(meeting_states)
    # conv_handler.states.update(location_states)
    updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
