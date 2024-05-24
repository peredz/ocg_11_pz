import telebot
from telebot import types


bot = telebot.TeleBot('6430445311:AAHBRFqKoSWSBWH3cEtXMMyMl9GRfCJ4jSY')


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    hello_text = (f'Привет <b>{message.chat.first_name}</b>\n'
                  f'Это бот для советов по теме <u>Как избегать'
                  f' зависимости от цифровых устройств и технологий</u>')
    bot.send_message(message.chat.id, hello_text,
                     parse_mode='html')
    main_mess_show(message)


@bot.message_handler(content_types=["text"])
def msg(message):
    if message.text == 'Определение зависимости':
        Definition_of_Dependency(message)
    elif message.text == 'Установление границ':
        Setting_Boundaries(message)
    elif message.text == 'Развитие других интересов':
        Developing_Other_Interests(message)
    elif message.text == 'Осознанное использование':
        Mindful_Usage(message)
    elif message.text == 'Социальные связи в реальной жизни':
        Strengthening_Real_life_Social_Connections(message)
    elif message.text == 'Цифровой детокс':
        Digital_Detox(message)
    elif message.text == 'Обращение за помощью':
        Seeking_PProfessional_Help(message)
    elif message.text == 'Полезные статьи':
        Usefull_articles(message)
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                           resize_keyboard=True,
                                           row_width=8)
        markup_list = ['Определение зависимости', 'Установление границ',
                       'Развитие других интересов', 'Осознанное использование',
                       'Социальные связи в реальной жизни', 'Цифровой детокс',
                       'Обращение за помощью', 'Полезные статьи']
        for mark_text in markup_list:
            markup.add(mark_text)
        bot.send_message(message.chat.id, '<b>Неизвестная команда:</b>',
                         parse_mode='html', reply_markup=markup)

def Definition_of_Dependency(message):
    message_text = '''<b>Что такое зависимость от цифровых устройств?</b>

Чрезмерное использование смартфонов, компьютеров, планшетов и других гаджетов.
Невозможность контролировать время, проведенное за экраном.
Пренебрежение важными аспектами жизни (работа, учеба, личные отношения) ради использования цифровых устройств.'''
    bot.send_message(message.chat.id, message_text, parse_mode='html')


def Setting_Boundaries(message):
    message_text = '''<b>Что такое зависимость от цифровых устройств?</b>

Чрезмерное использование смартфонов, компьютеров, планшетов и других гаджетов.
Невозможность контролировать время, проведенное за экраном.
Пренебрежение важными аспектами жизни (работа, учеба, личные отношения) ради использования цифровых устройств.'''
    bot.send_message(message.chat.id, message_text, parse_mode='html')


def Developing_Other_Interests(message):
    message_text = '''<b>Почему важно развивать другие интересы?</b>

Увлечение спортом, хобби или социальными мероприятиями помогает отвлечься от экранов.
Активный образ жизни способствует физическому и психологическому благополучию.
Найдите занятия, которые приносят радость и не связаны с технологиями (чтение, рисование, прогулки).'''
    bot.send_message(message.chat.id, message_text, parse_mode='html')


def Mindful_Usage(message):
    message_text = '''<b>Как практиковать осознанное использование технологий?</b>

Задавайте себе вопрос: "Почему я сейчас беру в руки телефон? Это действительно необходимо?"
Используйте специальные приложения для мониторинга и ограничения экранного времени.
Учитесь выключать уведомления и проверять сообщения в определенные часы.'''
    bot.send_message(message.chat.id, message_text, parse_mode='html')


def Strengthening_Real_life_Social_Connections(message):
    message_text = '''<b>Как укрепить социальные связи в реальной жизни?</b>

Проводите больше времени с друзьями и семьей лицом к лицу.
Организуйте мероприятия без использования технологий (настольные игры, прогулки, пикники).
Старайтесь вести беседы и взаимодействовать с людьми, а не через мессенджеры и социальные сети.'''
    bot.send_message(message.chat.id, message_text, parse_mode='html')


def Digital_Detox(message):
    message_text = '''<b>Что такое цифровой детокс и как его провести?</b>

Планируйте регулярные периоды (например, выходные или отпуск) без использования цифровых устройств.
Оповестите близких и коллег о своем намерении, чтобы они могли поддержать вас.
Найдите замену активности, связанной с технологиями, которая приносит удовольствие (спорт, творчество).'''
    bot.send_message(message.chat.id, message_text, parse_mode='html')


def Seeking_PProfessional_Help(message):
    message_text = '''<b>Когда стоит обратиться за профессиональной помощью?</b>

Если вы чувствуете, что не можете справиться с зависимостью самостоятельно.
Если зависимость негативно влияет на ваше психическое здоровье и качество жизни.
Консультации с психологом или специалистом по зависимостям могут помочь разработать индивидуальную стратегию преодоления зависимости.'''
    bot.send_message(message.chat.id, message_text,  parse_mode='html')


def Usefull_articles(message):
    message_text = '''<b>Вот ссылки на некоторые полезные статьи</b>

    https://www.wrike.com/ru/blog/kak-izbavitsa-ot-tsifrovoy-zavisimosti-za-30-dney/
    https://www.marieclaire.ru/psychology/digital-detox-8-sposobov-izbavitsya-ot-tsifrovoy-zavisimosti-/
    https://pomoschryadom.ru/helpful-articles/safety/kak-borotsya-s-internet-zavisimostyu'''
    bot.send_message(message.chat.id, message_text, parse_mode='html')


def main_mess_show(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                       resize_keyboard=True,
                                       row_width=8)
    markup_list = ['Определение зависимости', 'Установление границ',
                   'Развитие других интересов', 'Осознанное использование',
                   'Социальные связи в реальной жизни', 'Цифровой детокс',
                   'Обращение за помощью', 'Полезные статьи']
    for mark_text in markup_list:
        markup.add(mark_text)
    bot.send_message(message.chat.id, 'Выберете:',
                     parse_mode='html', reply_markup=markup)


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except:
        pass
