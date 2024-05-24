import YandexAPI
import adress
from sqlalchemy import select
from data import db_session
from data.users import User
from data.users import City
from data.users import Subscribe
from datetime import datetime


def check_new_user_or_not(user_id):
    db_session.global_init('db/cities.db')
    db_sess = db_session.create_session()
    res = db_sess.query(User).filter(User.id == user_id)
    db_sess.commit()
    res = [i.id for i in res]
    if res:
        return False
    return True


def check_new_ct_or_not(user_id):
    db_session.global_init('db/cities.db')
    db_sess = db_session.create_session()
    res = db_sess.query(User).get(user_id)
    db_sess.commit()
    if res:
        return False
    else:
        return True


def register(user_id):
    db_session.global_init('db/cities.db')
    db_sess = db_session.create_session()
    user = User()
    user.id = user_id
    user.reg_time = datetime.now()
    db_sess.add(user)
    db_sess.commit()


def new_ct(user_id, adrs):
    adr = adress.city_guess(adrs)
    counrty = adr[0]
    region = adr[1]
    city = adr[2]

    db_session.global_init('db/cities.db')
    db_sess = db_session.create_session()
    ct = City()
    ct.user_id = user_id
    ct.county = counrty
    ct.region = region
    ct.city = city
    if adr[3]:
        ct.street_with_type = adr[3]
    if adr[4]:
        ct.house = adr[4]
    db_sess.add(ct)
    db_sess.commit()


def get_all_cities(user_id):
    db_session.global_init('db/cities.db')
    db_sess = db_session.create_session()
    cities = db_sess.query(City).filter(City.user_id == user_id)
    db_sess.commit()
    cts = []
    for i in cities:
        if i.street_with_type:
            if i.house:
                cts.append(f'{i.city} {i.street_with_type} {i.house}')
            else:
                cts.append(f'{i.city} {i.street_with_type}')
        else:
            cts.append(i.city)
    return cts


def adr_remaker(adres):
    adres = adres.split()
    if len(adres) == 1:
        for _ in range(2): adres.append(None)
    elif len(adres) == 3:
        adres = [adres[0], ' '.join(adres[1:3]), None]
    elif len(adres) == 4:
        adres = [adres[0], ' '.join(adres[1:3]), adres[3]]
    return adres


def dell_city(user_id, city):
    if city not in get_all_cities(user_id):
        return False
    db_session.global_init('db/cities.db')
    db_sess = db_session.create_session()
    city = adr_remaker(city)
    city = db_sess.query(City).filter(City.user_id == user_id,
                                      City.city == city[0],
                                      City.street_with_type == city[1],
                                      City.house == city[2]).first()
    try:
        db_sess.delete(city)
        db_sess.commit()
        return True
    except BaseException:
        db_sess.commit()
        return False


def new_subscribe(user_id, city):
    db_session.global_init('db/cities.db')
    db_sess = db_session.create_session()
    city = adr_remaker(city)
    try:
        city_id = db_sess.query(City).filter(City.user_id == user_id,
                                             City.city == city[0],
                                             City.street_with_type == city[1],
                                             City.house == city[2]).first().id
    except IndexError:
        return False
    city = city[0]
    user_sub_cities_id = [i.ct_id for i in db_sess.query(Subscribe).filter(Subscribe.user_id == user_id)]
    if city_id in user_sub_cities_id:
        db_sess.commit()
        return False
    if city_id:
        db_session.global_init('db/cities.db')
        db_sess = db_session.create_session()
        sub = Subscribe()
        sub.ct_id = city_id
        sub.user_id = user_id
        sub.time_gr = YandexAPI.time_line(city)
        db_sess.add(sub)
        db_sess.commit()
        return sub.ct_id
    db_sess.commit()
    return False


def sub_time_setter(user_id, time, ct_id):
    db_session.global_init('db/cities.db')
    db_sess = db_session.create_session()
    sub = db_sess.query(Subscribe).filter(Subscribe.user_id == user_id, Subscribe.ct_id == ct_id).first()
    if sub:
        sub.time_gr = (time - sub.time_gr) % 24
        db_sess.commit()
        return True
    db_sess.commit()
    return False


def get_all_subs(user_id):
    db_session.global_init('db/cities.db')
    db_sess = db_session.create_session()
    cities = db_sess.query(Subscribe).filter(Subscribe.user_id == user_id)
    cts = [i.ct_id for i in cities]
    cities = []
    for i in cts:
        if adr := db_sess.query(City).filter(City.id == i).first():
            if adr.street_with_type:
                if adr.house:
                    cities.append(f'{adr.city} {adr.street_with_type} {adr.house}')
                else:
                    cities.append(f'{adr.city} {adr.street_with_type}')
            else:
                cities.append(adr.city)
    # cities = [db_sess.query(City).filter(City.id == i)[0] for i in cts]
    return cities


def dell_sub(user_id, city):
    city = adr_remaker(city)
    db_session.global_init('db/cities.db')
    db_sess = db_session.create_session()
    city_id = db_sess.query(City).filter(City.user_id == user_id,
                                         City.city == city[0],
                                         City.street_with_type == city[1],
                                         City.house == city[2]).first().id
    sub = db_sess.query(Subscribe).filter(Subscribe.user_id == user_id, Subscribe.ct_id == city_id).first()
    db_sess.delete(sub)
    db_sess.commit()
    return city


def mailing_on_cur_hour():
    now = datetime.utcnow().hour
    db_session.global_init('db/cities.db')
    db_sess = db_session.create_session()
    subs = [i.ct_id for i in db_sess.query(Subscribe).filter(Subscribe.time_gr == now)]
    cities = [(db_sess.query(City).filter(City.id == i).first()) for i in subs]
    cts = []
    for i in [i for i in cities if i]:
        if i.street_with_type:
            if i.house:
                cts.append([i.user_id, f'{i.city} {i.street_with_type} {i.house}'])
            else:
                cts.append([i.user_id, f'{i.city} {i.street_with_type}'])
        else:
            cts.append([i.user_id, i.city])
    return cts