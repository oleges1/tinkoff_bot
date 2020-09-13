from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from utils import *
import random, time
from selects import change_money, change_energy, get_energy, get_money

FORUM, FORUM_GAME, FORUM_GAME_PLAY = 'forum', 'forum_game', 'forum_game_playing'

def forum(update, context):
    msg = 'Прийдя на форум вы видите как активно дискутирует группа прикладных рационалистов. На стене висит местный рейтинг участников клуба общения. Что будете делать?\n'
    reply_keyboard_menu = [['Подойти к рационалистам'],
                           ['Уйти']]

    update.message.reply_text(
        msg,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard_menu, one_time_keyboard=True))

    return FORUM

def forum_game(update, context):
    if get_energy(update) > 0:
        if get_money(update, context) >= 100:
            msg = 'Вас сажают за стол и предлагают сыграть в игру на финансовую калиброванность. Правила следующие: играют два участника, каждый ставит ставку в 100 олегро. Обоим участникам задаётся вопрос, ответ на который является числом. Тот кто ответит точнее всего, побеждает и забирает деньги. Хотите попробовать?\n'
            
            reply_keyboard_menu = [['Да'],
                                ['Нет']]

            update.message.reply_text(
                msg,
                reply_markup=ReplyKeyboardMarkup(reply_keyboard_menu, one_time_keyboard=True))

            return FORUM_GAME
        else:
            update.message.reply_text("У вас нет денег, возвращайтесь когда найдёте хотя бы 100 олегро.", 
                        reply_markup=ReplyKeyboardMarkup([['Уйти']], one_time_keyboard=True))
            return "start"
    else:
        update.message.reply_text("Вы очень устали, возвращайтесь когда наберётесь сил.",
                    reply_markup=ReplyKeyboardMarkup([['Уйти']], one_time_keyboard=True))
        return "start"



def find_player(context):
    partner_name = context.job.context[1]
    question = context.job.context[2]
    
    context.bot.send_message(chat_id=context.job.context[0], text='Игрок найден!')
    msg = f'''С вами играет {partner_name}\n\nВопрос:\n{question}\nВремя пошло.'''
    context.bot.send_message(chat_id=context.job.context[0], text=msg)

def time_is_up(context):
    context.bot.send_message(chat_id=context.job.context[0], text="Время вышло!")


def forum_game_play(update, context):
    partner_name = get_random_name()
    question, correct_ans = get_random_question()
    #question = 'Сколько рублей в месяц средний житель Москвы тратит на красную икру?'
    #correct_answer = 2500

    update.message.reply_text('Отлично!\nНа кону 100 олегро. На ответ будет дано 30 секунд.\n\nЖдём другого игрока...')
    
    waiting_time = 1 + random.random() * 5
    context.job_queue.run_once(find_player, waiting_time, context=[update.message.chat_id, partner_name, question])
    
    context.user_data['job'] = context.job_queue.run_once(time_is_up, waiting_time + 30, context=[update.message.chat_id, partner_name, question])
    context.user_data['forum_answer'] = correct_ans
    context.user_data['forum_partner'] = partner_name
    context.user_data['forum_partner_answer'] = (random.randint(-int(correct_ans * 0.8), int(correct_ans)*2) + correct_ans) // 10 * 10
    context.user_data['forum_time'] = time.time() + waiting_time 

    return FORUM_GAME_PLAY

def forum_game_check(update, context):
    correct_ans = context.user_data['forum_answer']
    ans = update.message.text
    try:
        ans = int(ans)
    except:
        update.message.reply_text("Ответ должен быть числом, попробуйте ввести ещё раз.")
        return FORUM_GAME_PLAY

    
    partner_ans = context.user_data['forum_partner_answer']
    partner_name = context.user_data['forum_partner']

    time_passed = time.time() - context.user_data['forum_time']
    if time_passed > 30:
        ans = -1
    else:
        update.message.reply_text("Отлично! Ожидаем соперника...")

        
    def print_results(context):
        if 'job' in context.job.context.user_data:
            context.job.context.user_data['job'].schedule_removal()
            del context.job.context.user_data['job']
        if abs(ans - correct_ans) < abs(partner_ans - correct_ans):
            msg = f'''Вы обыграли {partner_name} Ответ соперника был {partner_ans}. Верный ответ - {correct_ans}.\nПоздравляю, 100 олегро ваши. Хотите закрепить успех?'''
            money = 100
        elif abs(ans - correct_ans) > abs(partner_ans - correct_ans):
            msg = f'''Соперник {partner_name} оказался ближе к истине с ответом в {partner_ans}. Верный ответ - {correct_ans}.\nВы потеряли 100 олегро, но может быть вы сможете отыграться?'''
            money = -100
        else:
            msg = f'''Ничья, вы ответили одинаково - {partner_ans}. Верный ответ - {correct_ans}.\nВсе остались при своих. Такое - редкость. Попробуете ещё раз?'''
            money = 0
        reply_keyboard_menu = [['Да'],
                               ['Нет']]

        change_money(update, money)

        update.message.reply_text(
            msg,
            reply_markup=ReplyKeyboardMarkup(reply_keyboard_menu, one_time_keyboard=True))

    context.job_queue.run_once(print_results, max(0, min(2, 30 - time_passed * (4 * random.random()))), context=context)
    return FORUM_GAME
