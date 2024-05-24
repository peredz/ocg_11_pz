import json

import requests
import adress
import consts


def get_weather(city, num_of_days, hours='false'):

    lat, lon = adress.city_cords(city)
    headers = {'X-Yandex-API-Key': 'da277cd7-3def-464b-9995-739b10a23d31'}
    params = {'lang': 'ru_RU', 'limit': str(num_of_days), 'hours': hours, 'extra': 'false'}
    res = requests.get(f'https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}', headers=headers, params=params)
    if 'errors' in json.loads(res.text):
        return False
    return res


def week_weather(city):
    if adress.city_guess(city):
        weather = get_weather(adress.city_cords(city), 1, hours='true')
        return weather.json()
    return False


def get_fact(city, how_much_hours=6, td=False):

    try:
        if td:
            weather = get_weather(city, 1, hours='true').json()
        else:
            weather = get_weather(city, 2, hours='true').json()
    except BaseException as e:

        print('Ошибка', e, 'не открыть как json')
        return False

    if not(weather):
        return False

    hour_now = (weather['info']['tzinfo']['offset'] // 3600)
    hour = (int(weather['now_dt'][11:13]) + hour_now) % 24
    if how_much_hours == 6:
        if hour >= 18:
            hours = weather['forecasts'][0]['hours'][hour:]
            for i in weather['forecasts'][1]['hours'][:6 - (24 - hour)]:
                hours.append(i)
        else:
            hours = weather['forecasts'][0]['hours'][hour:hour + 6]
    else:
        if td:
            hours = weather['forecasts'][0]['hours']
        else:
            hours = weather['forecasts'][1]['hours']
    if weather['geo_object']['district']:
        adr = ', '.join([weather['geo_object']['district']['name'], weather['geo_object']['locality']['name']])
    elif weather['geo_object']['province']:
        adr = ', '.join([weather['geo_object']['province']['name'], weather['geo_object']['locality']['name']])
    else:
        adr = ''
    cur_temp = weather['fact']['temp']
    condition = consts.CONDS[weather['fact']['condition']]
    cur_tmp_feels_like = weather['fact']['feels_like']
    time = f'{hour}:{weather["now_dt"][14:16]}'
    wind_speed = weather['fact']['wind_speed']
    wind_dir = consts.DIRS[weather['fact']['wind_dir']]
    humidity = weather['fact']['humidity']
    pressure_mm = weather['fact']['pressure_mm']
    hours = [[f"{i['hour']}:00", consts.CONDS_SMILE[i['condition']], i['temp']] for i in hours]

    return [adr, time, cur_temp, condition, cur_tmp_feels_like, wind_speed, wind_dir, humidity, pressure_mm, hours]


def shablon_maker(city):
    if not(res := get_fact(city)):
        return False
    adr, time, cur_tmp, condition, cur_tmp_feels_like, wind_speed, wind_dir, humidity, pressure_mm, hours = res
    shablon = f'''{adr}
Сейчас {time}.
{cur_tmp}° {condition} Ощущается как {cur_tmp_feels_like}°
💨{wind_speed} м/с, {wind_dir}    💧{humidity}%    🧭{pressure_mm} мм рт.
_______________________________________
{'   '.join([i[0] for i in hours])}
{'       '.join([i[1] for i in hours])}
{'       '.join([f"{i[2]}°" for i in hours])}
 _______________________________________'''
    return shablon


def shablon_maker_day(city, td_tm):
    if not(res := get_fact(city, how_much_hours=24, td=td_tm)):
        return False
    adr, time, cur_tmp, condition, cur_tmp_feels_like, wind_speed, wind_dir, humidity, pressure_mm, hours = res
    if td_tm:
        header = f'''\n{cur_tmp}° {condition} Ощущается как {cur_tmp_feels_like}°
💨{wind_speed} м/с, {wind_dir}    💧{humidity}%    🧭{pressure_mm} мм рт. 
__________________________________________'''
    else:
        header = ''
    day = 'сегодня' if td_tm else 'завтра'
    shablon = f'''{adr}
Погода на {day}:{header}
{'   '.join([i[0] for i in hours[:6]])}
{'       '.join([i[1] for i in hours[:6]])}
{'       '.join([f"{i[2]}°" for i in hours[:6]])}
__________________________________________
{'   '.join([i[0] for i in hours[6:12]])}
{'       '.join([i[1] for i in hours[6:12]])}
{'       '.join([f"{i[2]}°" for i in hours[6:12]])}
__________________________________________
{'   '.join([i[0] for i in hours[12:18]])}
{'       '.join([i[1] for i in hours[12:18]])}
{'       '.join([f"{i[2]}°" for i in hours[12:18]])}
__________________________________________
{'   '.join([i[0] for i in hours[18:24]])}
{'       '.join([i[1] for i in hours[18:24]])}
{'       '.join([f"{i[2]}°" for i in hours[18:24]])}
___________________________________________'''
    return shablon


def week_forecas(city):
    try:
        forecasts = get_weather(city, 7, hours='false').json()
        if forecasts['geo_object']['district']:
            header = ', '.join([forecasts['geo_object']['district']['name'],
                                forecasts['geo_object']['locality']['name']])
        else:
            header = ', '.join([forecasts['geo_object']['province']['name'],
                                forecasts['geo_object']['locality']['name']])
        days = []
        for i in forecasts['forecasts']:
            day = i['parts']['day_short']
            days.append([day['temp'], consts.CONDS_SMILE[day['condition']]])
        print(days)
        shablon = f'''{header}
Погода на неделю:
пн       вт       ср       чт       пт       сб       вск
{'     '.join([i[1] for i in days])}
{'      '.join([f"{i[0]}°" for i in days])}'''
        return shablon
    except BaseException as e:
        print('Ошибка', e, 'я тут')
        return False
    # x = (get_weather('Владивосток', 7).json()['forecasts'][0]['parts'])
    # print(x['day_short']['temp'])
    # print(x['day_short']['condition'])


def time_line(city):
    try:
        abbr = int(get_weather(city, num_of_days=1).json()['info']['tzinfo']['abbr'])
    except BaseException:
        abbr = 0
    return abbr