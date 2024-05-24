from multiprocessing.context import Process
import telebot
import time
from telebot import types
import schedule
import DB_stuff
import YandexAPI
import adress


bot = telebot.TeleBot('6430445311:AAHBRFqKoSWSBWH3cEtXMMyMl9GRfCJ4jSY')


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    if DB_stuff.check_new_user_or_not(message.chat.id):
        DB_stuff.register(message.chat.id)
    hello_text = [f'Привет <b>{message.chat.first_name}</b>\n',
                  f'Это бот для погоды\n'
                  f'Введите адрес']
    bot.send_message(message.chat.id, f'{hello_text[0]}\n{hello_text[1]}',
                     parse_mode='html')
    bot.register_next_step_handler(message, new_city)


@bot.message_handler(content_types=["text"])
def msg(message):
    if message.text == 'Узнать погоду':
        markup = all_cities_markup(message)
        bot.send_message(message.chat.id, 'Прогноз по адресу', reply_markup=markup)
        bot.register_next_step_handler(message, weather_fork)
    elif message.text == 'Рассылка':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                           resize_keyboard=True,
                                           row_width=3)
        markup.add('Новая рассылка')
        markup.add('Удалить рассылку')
        markup.add('Отмена')
        bot.send_message(message.chat.id, 'Управление рассылками', reply_markup=markup)
        bot.register_next_step_handler(message, mailing)
    elif message.text == 'Адреса':
        change_cities(message)
    else:
        bot.send_message(message.chat.id, 'Неизвестная команда')
        main_mess_show(message)


def wait(message, adrs):
    if len(message.text) > 1:
        if message.text[0:2].lower() == 'да':
            DB_stuff.new_ct(message.from_user.id, adrs)
            bot.send_message(message.chat.id, 'Адрес добавлен',
                             parse_mode='html')
            main_mess_show(message)
        else:
            bot.send_message(message.chat.id, f'Напишите адрес еще раз',
                             parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, new_city)
    else:
        bot.send_message(message.chat.id, f'Напишите адрес еще раз',
                         parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, new_city)


def main_mess_show(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                       resize_keyboard=True,
                                       row_width=3)
    markup.add('Узнать погоду')
    markup.add('Рассылка')
    markup.add('Адреса')
    bot.send_message(message.chat.id, 'главное меню:',
                     parse_mode='html', reply_markup=markup)


def new_city(message):
    adr = adress.city_guess(message.text)
    if adr:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                           resize_keyboard=True,
                                           row_width=2)
        markup.add(f'Да: {" ".join([i for i in adr if i])}')
        markup.add('Нет, повторить попытку')
        bot.send_message(message.chat.id, f'Ваш адрес: <u>{" ".join([i for i in adr if i])}</u>?',
                         parse_mode='html',
                         reply_markup=markup)
        bot.register_next_step_handler(message, wait, " ".join([i for i in adr if i]))
    else:
        bot.send_message(message.chat.id, f'Программа не может найти адрес\n'
                                          f'повторите попытку',
                         parse_mode='html')
        bot.register_next_step_handler(message, new_city)


def weather_fork(message):
    guess = adress.city_guess(message.text)
    if guess:
        adres = ' '.join([i for i in guess if i])
    else:
        adres = False
    if adres:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                           resize_keyboard=True,
                                           row_width=4)
        markup.add('Погода сейчас')
        markup.add('Погода на сегодня')
        markup.add('Погода на завтра')
        markup.add('Погода на неделю')

        bot.send_message(message.chat.id, 'Погоду на:', reply_markup=markup)
        bot.register_next_step_handler(message, what_weather, adres)
    else:
        bot.send_message(message.chat.id, 'Ошибка, для введенного вами адреса невозможно получить прогноз')
        main_mess_show(message)


def what_weather(message, adres):
    if message.text == 'Погода сейчас':
        weather_6_hours(message, adres)
    elif message.text == 'Погода на сегодня':
        weather_day(message, adres, True)
    elif message.text == 'Погода на завтра':
        weather_day(message, adres, False)
    elif message.text == 'Погода на неделю':
        weather_week(message, adres)
    else:
        weather_week(message, adres)


def weather_6_hours(message, adres):
    res = YandexAPI.shablon_maker(adres)
    if res:
        bot.send_message(message.chat.id, res)
    else:
        bot.send_message(message.chat.id, 'Ошибка.\nСкорее всего вы написали неправильный адрес')
    main_mess_show(message)


def weather_day(message, adres, td):
    res = YandexAPI.shablon_maker_day(adres, td)
    if res:
        bot.send_message(message.chat.id, res)
    else:
        bot.send_message(message.chat.id, 'Ошибка.\nСкорее всего вы написали неправильный адрес')
    main_mess_show(message)


def weather_week(message, adres):
    res = YandexAPI.week_forecas(adres)
    if res:
        bot.send_message(message.chat.id, res)
    else:
        bot.send_message(message.chat.id, 'Ошибка.\nСкорее всего вы написали неправильный адрес')
    main_mess_show(message)


def change_cities(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                       resize_keyboard=True,
                                       row_width=3)
    markup.add('Добавить адрес')
    markup.add('Убрать адрес')
    markup.add('Выйти')
    bot.send_message(message.chat.id, 'Что изменить?',
                     parse_mode='html',
                     reply_markup=markup)
    bot.register_next_step_handler(message, changer)


def changer(message):
    if message.text == 'Добавить адрес':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Введите адрес',
                         parse_mode='html',
                         reply_markup=markup)
        bot.register_next_step_handler(message, new_city)
    elif message.text == 'Убрать адрес':
        city_deleter_chooser(message)
    else:
        main_mess_show(message)


def city_deleter_chooser(message):
    markup = all_cities_markup(message)
    markup.add('Отменить')
    bot.send_message(message.chat.id, 'Выберете адрес', reply_markup=markup)
    bot.register_next_step_handler(message, city_deleter)


def city_deleter(message):
    if message.text == 'Отменить':
        main_mess_show(message)
    else:
        if DB_stuff.dell_city(message.chat.id, message.text):
            bot.send_message(message.chat.id, f'Адрес <b>{message.text}</b> удален',
                             parse_mode='html')
            main_mess_show(message)
        else:
            bot.send_message(message.chat.id, f'Произошла ошибка при удалении адреса',
                             parse_mode='html')
            main_mess_show(message)


def mailing(message):
    if message.text == 'Отмена':
        main_mess_show(message)
    elif message.text == 'Новая рассылка':
        markup = all_cities_markup(message)
        markup.add('Отменить')
        bot.send_message(message.chat.id, 'Выберете адрес', reply_markup=markup)
        bot.register_next_step_handler(message, sub_checker)
    elif message.text == 'Удалить рассылку':
        subs = DB_stuff.get_all_subs(message.chat.id)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                           resize_keyboard=True,
                                           row_width=len(subs) + 1)
        for i in subs:
            markup.add(i)
        markup.add('Отменить')
        bot.send_message(message.chat.id, 'Выберете адрес у которого удалить рассылку', reply_markup=markup)
        bot.register_next_step_handler(message, dell_sub)
    else:
        main_mess_show(message)


def sub_checker(message):
    if message.text in DB_stuff.get_all_cities(message.chat.id):
        if x := DB_stuff.new_subscribe(message.chat.id, message.text):
            time_asker(message, x)
        else:
            bot.send_message(message.chat.id, 'На один адрес можно добавлять ТОЛЬКО одну рассылку',
                             parse_mode='html')
            bot.send_message(message.chat.id, 'Чтобы добавить рассылку на данный адрес, удалите прошлую',
                             parse_mode='html')
            main_mess_show(message)
    elif message.text == 'Отменить':
        main_mess_show(message)
    else:
        bot.send_message(message.chat.id,
                         'Рассылку можно добавить только на сохраненный адрес.'
                         '\nЕсли вы ранее не добавляли адрес, для которого хотите подключить рассылку,'
                         ' то:\n <b>Адреса</b>➡<b>Добавить адрес</b>',
                         parse_mode='html')
        #<b>Изменить⚙</b>
        main_mess_show(message)


def time_asker(message, ct_id):
    bot.send_message(message.chat.id, 'Укажите время рассылки (по местному времени)')
    bot.register_next_step_handler(message, mailing_time, ct_id)


def mailing_time(message, ct_id):
    if message.text.isdigit():
        if 0 <= int(message.text) <= 23:
            if DB_stuff.sub_time_setter(message.chat.id, int(message.text), ct_id):
                bot.send_message(message.chat.id, 'Рассылка добавлена')
                main_mess_show(message)
            else:
                bot.send_message(message.chat.id, 'Не получилось добавить рассылку(')
                main_mess_show(message)
        else:
            bot.send_message(message.chat.id, 'Введите число от 0 до 23')
            time_asker(message, ct_id)
    else:
        bot.send_message(message.chat.id, 'Введите число от 0 до 23')
        time_asker(message, ct_id)


def dell_sub(message):
    if message.text == 'Отменить':
        main_mess_show(message)
    elif message.text in DB_stuff.get_all_cities(message.chat.id):
        DB_stuff.dell_sub(message.chat.id, message.text)
        bot.send_message(message.chat.id, f'Рассылка <b>{message.text}</b> удалена', parse_mode='html')
        main_mess_show(message)
    else:
        bot.send_message(message.chat.id, f'Произошла ошибка при удалении рассылки', parse_mode='html')
        main_mess_show(message)


def all_cities_markup(message):
    cities = DB_stuff.get_all_cities(message.chat.id)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                       resize_keyboard=True,
                                       row_width=len(cities) + 1)
    for i in cities:
        markup.add(i)
    return markup


def send_mailings():
    for i in DB_stuff.mailing_on_cur_hour():
        bot.send_message(i[0], YandexAPI.shablon_maker(i[1]))


# async def scheduler():
#     aioschedule.every(10).seconds.do(send_mailings)
#
#     while True:
#         await aioschedule.run_pending()
#         await asyncio.sleep(1)
#
#
# async def on_startup():
#     await asyncio.create_task(scheduler())
#
#
# async def main():
#     for i in range(400):
#         try:
#             bot.polling(none_stop=True)
#
#         except Exception as e:
#             print(e)  # или просто print(e) если у вас логгера нет,
#             # или import traceback; traceback.print_exc() для печати полной инфы
#             time.sleep(15)
#
#
# asyncio.run(scheduler())
# asyncio.run(main())

#вот тут
schedule.every().hour.at(':00').do(send_mailings)


class ScheduleMessage():
    def try_send_schedule():
        while True:
            schedule.run_pending()
            time.sleep(1)

    def start_process():
        p1 = Process(target=ScheduleMessage.try_send_schedule, args=())
        p1.start()


if __name__ == '__main__':
    ScheduleMessage.start_process()
    try:
        bot.polling(none_stop=True)
    except:
        pass
