import random
names = ['Александр', 'Андрей', 'Анжела', 'Валентин', 'Георгий', 'Олег', 'Денис', 'Ярослав', 'Анна', 'Иван', 'Екатерина', 'Алексей', 'Агата']
nicknames = ['Mammoth', '2', 'Blinker', 'FearLeSS', 'Slug-em-dog', 'RawSkills', 'Danqqqqq', '3P-own', 'VileHero', 'Predator', 'Freaky', 'Ratbuster', 'NeoGermal', 'FireBrang', 'Fatsy', 'Bear', 'HolyCombo', 'ThickSKN', 'Dark', 'Matter', 'BuffFreak', 'HOV', '2nd', 'Hand', 'Joe', 'ThermalMode', 'Flotsams54', 'Redneck', 'Giorgio', 'CodeExia', 'Roadspike', 'Mechani-Man', 'Kazami', 'of', 'Truth', 'Gbbledgoodk', 'High', 'Beam', 'Eye', 'Devil', 'Swing', 'Setter', 'Tea', 'Kettle', 'MrOnsTr', 'Wrangler', 'Jim', 'Flint', 'Cast-Iron', 'Kinged', 'Lucifurious', 'Lewd', 'Dice', 'RZR', 'LerveDr', 'Flyswat', 'Briggs', 'Legacy', 'Shade', 'Nightman', 'PP', 'Dubs', 'Prone', 'Hemingway', 'Mirmillone', 'Scooby', 'Did', 'Stealth', 'Slinger', 'Preach', 'Man', 'Unseen', 'Crossing', 'Guard', 'Bad', 'Bond', 'Force', 'FRMhndshk', 'Easy', 'Mac', 'Sky', 'SkyGod', 'Toxic-oxide', 'Silent', 'GiddeeUP', 'Irish', 'Dze', 'Apex', 'DragonBlood', 'Tse', 'Tse', 'Guy', 'Shay', 'IceDog', 'Dallas', 'Foxface', 'Sloth', 'Lounge', 'Master', 'Sprinkle', 'Lovenuts', 'Sokol', 'DeathDancer', 'Zorkle', 'Sporkle', 'Skool', 'Pompeii', 'Unicorn', 'Noise', 'Toy', 'Flash', 'Achilles', 'Mountain', 'Whip', 'Chu', 'Elektrik', 'Bad', 'Badminton', 'Sly', 'Silvermoon', 'LocKz', 'THRESHmSTR', 'Tin', 'Mutt', 'ReiGnZ', 'High-Fructose', 'Sweet', 'Bacon', 'Coldy', 'Sepukku', 'Crazy', 'Rox', 'Beo', 'Valley', 'Guardian', '1st', 'Degree', 'Ice', 'Sw00sh', 'Bom', 'Crossed', 'Unleashed', 'Ba1t', 'Sick', 'Saurus', 'Corny', 'SneakerKid', 'Mad', 'Viral', 'Steel', 'ShadowFax', 'Clang', 'Glyph', 'Ex0tic', 'Hermopolis', 'xFRST', 'VPR', 'ManManMan', 'Mosquit-No', 'LyRz', 'Firedog', 'ELLerG!c', 'Lime', 'German', 'Coach', 'Hex', 'Panther', 'Energy', 'Y0dler', 'xSTORMx', 'Blade', 'WeldMaster', 'Die', 'Slice', 'Tunez', 'Steel', 'Cut', 'Toe', 'Free', 'Ham', 'Truth', 'Forger', 'Dr.', 'Jam', 'Man', 'Lskeee', 'Black', 'Walnut', 'Seattle', 'Jay', 'Pexxious', 'Journeyman', 'RDTN', 'Venious', 'Plegasus', 'Whip', '2T', 'Grotas', 'Carrot', 'Joker', 'Skirble', 'Sherm', 'Switch', 'Solitaire', 'Gro', 'Hobo', 'Samurai', 'Prof.', 'Smirk', 'Indestructible', 'Potato', 'Good', 'William', 'GuTzd', 'Kamikaze', 'Grandma', 'Infinite', 'Hole', 'Are', 'Ess', 'Tee', 'Badger', 'the', 'Burglar', 'Sw33per', 'Sir', 'Squire', 'Mauve', 'Cactus', 'Hidden', 'Tree', 'Deano', 'Bruh', 'AxelRoad', 'Uncle', 'Buddy', 'Fadey', 'Goldman', 'Copilot', 'Z-Boy', 'Fl00d', 'Bones', 'DZE', 'Danger', 'Menace', 'Vermilion', 'Muzish', 'Hang', '11', 'TrinitySoul', 'Cooger', 'Delicious', 'Wing', 'BlackExcalibur', 'Kazmii', 'Doz', 'Risen', 'AirportHobo', 'XD', 'Prez', 'Dog', 'ShadowDancer', 'Cumulo', 'Baked', 'ZD']
surnames = list('АБВГДЖЗКЛМНПРСТФЦХЧШЩЯ')
LEAGUES = [
    '⚪️Белая⚪️',
    '🟤Коричневая🟤',
    '🟢Зелёная🟢',
    '🔵Синяя🔵',
    '🟣Фиолетовая🟣',
    '🟠Оранжевая🟠',
    '🔴Красная🔴',
    '⚫️Чёрная⚫️'
]

LEVELS = {
    'Стажёр' :      [0, 5000],
    'Джуниор':      [5000, 10000],
    'Миддл':        [10000, 30000], 
    'Сениор':       [20000, 50000],
    'Знающий':      [50000, 80000],
    'Лид':          [80000, 100000],
    'Волк':         [100000, 1000000]
}

LEVEL_TO_LEAGUES = {
    'Стажёр' :      ['⚪️Белая⚪️'],
    'Джуниор':      ['⚪️Белая⚪️', '🟤Коричневая🟤'],
    'Миддл':        ['🟤Коричневая🟤', '🟢Зелёная🟢', '🔵Синяя🔵'], 
    'Сениор':       ['🟢Зелёная🟢', '🔵Синяя🔵', '🟣Фиолетовая🟣', '🟠Оранжевая🟠'],
    'Знающий':      ['🔵Синяя🔵', '🟣Фиолетовая🟣', '🟠Оранжевая🟠', '🔴Красная🔴'],
    'Лид':          ['🟣Фиолетовая🟣', '🟠Оранжевая🟠', '🔴Красная🔴', '⚫️Чёрная⚫️'],
    'Волк':         ['🟠Оранжевая🟠', '🔴Красная🔴', '⚫️Чёрная⚫️']
}

LEAGUES_TO_SIZE = {
    '⚪️Белая⚪️' :       10,
    '🟤Коричневая🟤' :  15,
    '🟢Зелёная🟢':      20,
    '🔵Синяя🔵':        25, 
    '🟣Фиолетовая🟣':   30,
    '🟠Оранжевая🟠':    35,
    '🔴Красная🔴':      40,
    '⚫️Чёрная⚫️':       50
}

def get_random_name():
    return names[random.randint(0, len(names) - 1)] + ' ' + surnames[random.randint(0, len(surnames) - 1)] + '.'

def get_random_question():
    questions = [
            'Сколько процентов российского экспорта составляют нефть и газ?',
            'На сколько процентов упал рубль в период с 2014 по 2017?',
            'Какая примерная себестоимость чашки капучино в рублях',
            'Сколько рублей в год средний автомобилист Москвы тратит на свою машину?']
    answers = [59, 50, 22, 70800]
    i = random.randint(0, len(questions) - 1)
    return questions[i], answers[i]

def get_random_nickname():
    nick = nicknames[random.randint(0, len(nicknames) - 1)]
    if random.random() > 0.5:
        nick = nick.lower()
    return nick

def generate_bot_data():
    bot_id = random.randint(1, 1000000)

    return {
        'telegram_id':bot_id,
        'first_name':names[random.randint(0, len(names) - 1)],
        'last_name':surnames[random.randint(0, len(surnames) - 1)],
        'username':get_random_nickname(),
        'coins':random.randint(0, 1000),
        'state':'start',
        'energy':random.randint(0, 10)
    }

with open('quizes.txt', 'r') as f:
    lines = f.readlines()
quizes = []
i = 0
while i < len(lines):
    quizes.append(lines[i:i+5])
    i += 5
print(quizes)

def get_random_quiz():
    i = random.randint(0, len(quizes) - 1)
    quiz = []
    ans = None
    for item in quizes[i]:
        item = item.strip()
        if item.endswith('!!!!'):
            quiz.append(item[:-4])
            ans = item[:-4]
        else:
            quiz.append(item)
    return quiz, ans
