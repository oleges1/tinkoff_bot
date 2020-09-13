import numpy as np
from matplotlib.figure import Figure


stock_stats = dict()


def save_bet(update, context, chat_id, bet):
    stock_stats[chat_id]['bet'] = bet


def sample(chat_id, period_length=2160, distribution='normal'):
    if distribution == 'normal':
        diffs = np.random.normal(scale=0.01, size=period_length)
        values = np.cumsum(diffs)
        values -= values.min()
        values += np.random.normal(scale=1, size=1) ** 2
    elif distribution == 'bern':
        diffs = np.random.binomial(n=1, p=0.5, size=period_length) * 2 - 1
        values = np.cumsum(diffs)
        values -= values.min()
        values += np.random.randint(10, 40)

    observed = period_length * 2 // 3
    values_obs = values[:observed]
    values_test = values[observed:]

    stock_stats[chat_id] = {
        'obs' : values_obs,
        'test' : values_test
    }


def plot_obs(chat_id, sample_process, max_length=None):
    if max_length is None or max_length >= len(sample_process):
        support = np.arange(len(sample_process))
        process = sample_process
    else:
        start = len(sample_process) - max_length
        support = np.arange(start, len(sample_process))
        process = sample_process[start:]

    fig = Figure(figsize=(12, 6))
    ax = fig.add_subplot(111)
    ax.plot(support, process)

    ax.set_title('Наблюдаемая динамика курса акций Оргело', fontsize=16)
    ax.set_xlabel('Время', fontsize=15)
    ax.set_ylabel('Значение курса акции', fontsize=15)
    ax.grid()

    fig.savefig('obs' + str(chat_id) + '.png')


def plot_all(chat_id, obs, test):
    support_obs = np.arange(len(obs))
    support_test = np.arange(len(obs), len(obs) + len(test))

    fig = Figure(figsize=(12, 6))
    ax = fig.add_subplot(111)
    ax.plot(support_obs, obs, label='Наблюдаемая часть графика')
    ax.plot(support_test, test, label='Скрытая часть графика')

    ax.set_title('Наблюдаемая и скрытая динамика курса акций Оргело', fontsize=16)
    ax.set_xlabel('Время', fontsize=15)
    ax.set_ylabel('Значение курса акции', fontsize=15)
    ax.grid()
    ax.legend()

    fig.savefig('all' + str(chat_id) + '.png')


def sample_and_plot(period_length=1440, max_length=1440, distribution='normal'):
    sample_process = sample(period_length, distribution)
    plot(sample_process, max_length)

    return sample_process

