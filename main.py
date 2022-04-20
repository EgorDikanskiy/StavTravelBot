# Copyright 2022 Dikanskiy Egor
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# импорт библиотек

# для бота телеграмм
import telebot

# связь с api ST
import requests

# красивый вывод информации
from telebot import types
import html2text

# Токен
import config

# погода
from pyowm import OWM
from pyowm.utils.config import get_default_config
from pyowm.commons.exceptions import NotFoundError

# работа с датой и временем
import datetime

# рандом
import random

# получение информации о районах
area_lst = 'https://xn--26-6kcaa1auatb4dhgcjdif5fui.xn--p1ai/api/districts'
response_area = requests.get(area_lst)
response_area = response_area.json()
# создание списка с районами
districts = [el['name'] for el in response_area]

# получение информации об обьектах
objects_lst = 'https://xn--26-6kcaa1auatb4dhgcjdif5fui.xn--p1ai/api/objects'
response_objects = requests.get(objects_lst)
response_objects = response_objects.json()
# создание списка с обьектами
places = [el['name'] for el in response_objects]

# подключние к боту
bot = telebot.TeleBot(config.TOKEN)

# раговорные фразы
yes = ['да', 'конечно', 'да.', 'Да', 'Да.', 'Конечно', 'Ещё бы']
no = ['нет', 'Нет', 'не', 'Не', 'Неа']
hi = ['Привет', 'Где отдохнуть?', ' Подскажи, куда прокатиться на выходные?',
      'Куда поехать', 'Куда поехать?']
hotel = ['Где остановиться?', 'Гостиница?', 'Где остановиться', 'Гостиница']
do = ['Как дела?', 'как дела?', 'Как дела', 'как дела']
all_pl = ['Все достопримечательности', 'Все', 'все достопримечательности', 'все']
dist_lst = []

# словарь для правильной работы функции с погодой
dist_city_dct = {'Александровский район': 'Александровское',
                 'Шпаковский район': 'Михайловск',
                 'Ипатовский район': 'Ипатово',
                 'Петровский район': 'Светлоград',
                 'Грачевский район': 'Тугулук',
                 'Изобильненский район': 'Изобильный',
                 'Ставрополь': 'Ставрополь',
                 'Невинномысск': 'Невинномысск',
                 'Кочубеевский район': 'Кочубеевское',
                 'Кисловодск': 'Кисловодск',
                 'Новоселицкий район': 'Новоселицкое',
                 'Новоалександровский район': 'Новоалександровск',
                 'Апанасенковский район': 'Дивное',
                 'Пятигорск': 'Пятигорск',
                 'Арзгирский район': 'Арзгир',
                 'Ессентуки': 'Ессентуки',
                 'Труновский район': 'Донское',
                 'Железноводск': 'Железноводск',
                 'Андроповский район': 'Курсавка',
                 'Красногвардейский район': 'Красногвардейское',
                 'Георгиевский городской округ': 'Георгиевск',
                 'Буденновский район': 'Будённовск',
                 'Лермонтов': 'Лермонтов',
                 'Предгорный район': 'Ессентукская'}

# дни недели
WEEKDAYS = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')

# лучшие места
best_places = ['Александровские каменные столбы', 'Гора Голубиная, камень Черепаха и Бегемот', 'Гора Лягушинка',
               'Самохвалова скала', 'Свято-Троицкий источник', 'Урочище Семистожки', 'Ветряная мельница',
               'Государственный природный заказник «Сафонова дача»', 'Баобаб', 'Гора Два брата',
               'Музей под открытым небом', 'Сосновая роща в селе Бешпагир', 'Грязелечебница', 'Нулевой километр любви',
               'Гора Железная', 'Каскадная лестница', 'Пушкинская галерея', 'Гора Лысая',
               'Золотой родник вблизи села Подлужного', 'Источник вблизи села Московского', 'Лицо воина кочевника',
               'Музей русского самовара', 'Новотроицкое водохранилище', 'Старинная деревянная церковь',
               'Ветряная мельница', 'Балансирующие камни на р.Ольховка', 'Гора Кольцо', 'Каменные красные грибы',
               'Курортный бульвар', 'Лермонтовский водопад', 'Рим-гора', 'Скала Лермонтова',
               'Стеклянная струя и Зеркальный пруд', 'Тропа А.Н.Косыгина в курортном парке', 'Хозяин гор',
               'Кочубеевская ветроэлектростанция', 'Термальный комплекс «Долина гейзеров»', 'Орлиные скалы',
               'Гора Невинская', 'Парк культуры и отдыха Шерстяник', 'Станица Григорополисская',
               'Водопады на реке Кума', 'Ворота любви', 'Гора Бештау', 'Гора Машук', 'Озеро Провал',
               'Водопад у травертинового источника', 'Немецкий мост', 'Травертиновый источник',
               'Экотропа «Эммануэльевское урочище»', 'Гора Бударка', 'Источник в селе Татарка', 'Новокавказский мост',
               'Татарское городище', 'Экологическая тропа на горе Стрижамент']


# узнать ближайшие выходные
def next_closest(from_date, search_day):
    if isinstance(search_day, str):
        search_day = WEEKDAYS.index(search_day.lower())

    from_day = from_date.weekday()
    different_days = search_day - from_day if from_day < search_day else 7 - from_day + search_day
    return from_date + datetime.timedelta(days=different_days)


# токен
appid = "4ffbfb8067b16513c81acdfe9df4454d"


# скорость ветра
def get_wind_direction(deg):
    l = ['С ', 'СВ', ' В', 'ЮВ', 'Ю ', 'ЮЗ', ' З', 'СЗ']
    for i in range(0, 8):
        step = 45.
        min = i * step - 45 / 2.
        max = i * step + 45 / 2.
        if i == 0 and deg > 360 - 45 / 2.:
            deg = deg - 360
        if deg >= min and deg <= max:
            res = l[i]
            break
    return res


# проверка наличия города в базе
def get_city_id(s_city_name):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': s_city_name, 'type': 'like', 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data['list']]
        city_id = data['list'][0]['id']
    except Exception as e:
        print("Exception (find):", e)
        pass
    assert isinstance(city_id, int)
    return city_id


# прогноз погоды
def request_forecast(city_id):
    try:
        lst = []
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        for i in data['list']:
            lst.append((i['dt_txt'])[:16] + ' ' + '{0:+3.0f}'.format(i['main']['temp']) + ' ' +
                       '{0:2.0f}'.format(i['wind']['speed']) + "м/с" + ' ' +
                       get_wind_direction(i['wind']['deg']) + ' ' +
                       i['weather'][0]['description'])
        return lst
    except Exception as e:
        print("Exception (forecast):", e)
        pass


# ответ на комманду /start
@bot.message_handler(commands=['start'])
def start(message):
    # отправка сообщения
    bot.send_message(message.chat.id, f'Привет! \u270B Хочешь отправиться в путешествие?',
                     parse_mode='Markdown')


# ответ на комманду /help
@bot.message_handler(commands=['help'])
def help(message):
    # создание кнопок
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    dist_button = types.KeyboardButton('По районам')
    all_button = types.KeyboardButton('Все достопримечательности')
    markup.add(dist_button)
    markup.add(all_button)

    # отправка сообщения
    bot.send_message(message.chat.id, f'Привет! \u270B \n'
                                      f'Я подскажу какие места можно посетить в Ставропольском крае.\n'
                                      f'Вы можете задавать подобные вопросы:\n'
                                      f'Куда поехать?\n'
                                      f'Где отдохнуть?\n'
                                      f'Куда поехать в выходные?\n'
                                      f'Либо же выбрать достпримечательность или район с помощью кнопок ниже'
                     ,
                     parse_mode='Markdown', reply_markup=markup)


# обработка сообщений пользователя
@bot.message_handler()
def get_user_text(message):
    # если пользователь хочет выбрать район
    if message.text == 'По районам':
        # создание кнопок
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        back = types.KeyboardButton('Назад')
        markup.add(back)
        for el in response_area:
            button = types.KeyboardButton(el['name'])
            markup.add(button)

        # отправка сообщения
        bot.send_message(message.chat.id, 'Выберите район', reply_markup=markup)
        return

    # если пользователь приветствует бота
    elif message.text in hi:
        msg = bot.send_message(message.chat.id, f'Привет! \u270B Хочешь отправиться в путешествие?',
                               parse_mode='Markdown')

        # отправка сообщения
        # следующая по очереди фунция 'yes_or_not'
        bot.register_next_step_handler(msg, yes_or_not)

    # если пользователь выбрал район
    elif message.text in districts:
        # создание кнопок
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        back = types.KeyboardButton('Назад')
        markup.add(back)
        for el in response_area:
            if el['name'] == message.text:
                id = el['id']
        for el in response_objects:
            if el['district_id'] == id:
                button = types.KeyboardButton(el['name'])
                markup.add(button)

        # отправка сообщения
        bot.send_message(message.chat.id, 'Выберите достопримечательность', reply_markup=markup)
        return

    # если пользователь выбрал достопримечательность
    elif message.text in places:
        try:
            for el in response_objects:
                if el['name'] == message.text:
                    # название достопримечательности
                    name = el['name']

                    # id достопримечательности
                    id_object = el['id']

                    # информация об обьекте
                    info_object = f'https://xn--26-6kcaa1auatb4dhgcjdif5fui.xn--p1ai/api/object/{id_object}'
                    info = requests.get(info_object)
                    info = info.json()

                    # описание достопримечательности
                    description = info['description']
                    description = html2text.html2text(description)

                    # фото достопримечательности
                    image = f"https://xn--26-6kcaa1auatb4dhgcjdif5fui.xn--p1ai/cache/thumb/{el['image']}"

                    # координаты достопримечательности
                    cords = f"{el['lat']} {el['lon']}"

                    for i in response_area:
                        if i['id'] == el['district_id']:
                            district = i['name']

            dist_lst.append(district)

            # создание кнопок
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            wet = types.KeyboardButton('Узнать погоду')
            markup.add(wet)

            # отправка фото достопримечательности
            bot.send_photo(message.chat.id, image)

            # если сообщение слишком длинное
            if len(description) < 4096:
                # отправка сообщения
                bot.send_message(message.chat.id, f'*{name}*\n\n'
                                                  f'[{cords}](https://yandex.ru/maps/36/stavropol/?ll={cords.split()[1]}%2'
                                                  f'C{cords.split()[0]}&mode=whatshere&whatshere%5Bpoint%5D={cords.split()[1]}%'
                                                  f'2C{cords.split()[0]}&whatshere%5Bzoom%5D=16&z=15)\n\n'
                                                  f'{district}\n\n'
                                                  f'{description}', parse_mode='Markdown', reply_markup=markup)
            else:
                for x in range(0, len(description), 4096):
                    # отправка сообщения
                    bot.send_message(message.chat.id, description[x:x + 4096])
            return
        except Exception:
            # отправка сообщения
            bot.send_message(message.chat.id, 'Ошибка', parse_mode='Markdown')

    # если пользователь хочет вернуться назад
    elif message.text == 'Назад':
        # возвращение на начальную страницу
        start(message)

    # если пользователь хочет просмотреть все достопримечательнсти
    elif message.text == 'Все достопримечательности':
        # создание кнопок
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        back = types.KeyboardButton('Назад')
        markup.add(back)
        for el in places[0:98]:
            button = types.KeyboardButton(el)
            markup.add(button)
        more = types.KeyboardButton('Далее')
        markup.add(more)

        # отправка сообщения
        bot.send_message(message.chat.id, 'Выберите достопримечательность', reply_markup=markup)

    # если пользователь хочет посмотреть ещё достопримечательнсти
    elif message.text == 'Далее':
        # создание кнопок
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        back = types.KeyboardButton('Назад')
        markup.add(back)
        for el in places[99:195]:
            button = types.KeyboardButton(el)
            markup.add(button)

        # отправка сообщения
        bot.send_message(message.chat.id, 'Выберите достопримечательность', reply_markup=markup)

    # супер фунция подбора достопримечательности
    elif 'выходные' in message.text:
        current_date = datetime.datetime.now().date()
        # ближайшие выходные
        holiday = str(next_closest(datetime.datetime.strptime(str(current_date), '%Y-%m-%d'), 'saturday'))[:10]
        s_city_name = 'Ставрополь'
        city_id = get_city_id(s_city_name)
        # проноз погоды
        lst = request_forecast(city_id)
        # супер проверка
        for el in lst:
            if el[:10] == holiday:
                info = el.split()
                if info[1] == '09:00':
                    temp = int(info[2])
                    wind = int(info[3][:1])
                    if temp >= 5 and wind <= 10:
                        place = random.choice(best_places)
                        bot.send_message(message.chat.id, f'Советуем посетить {place}!', parse_mode='Markdown')
                        try:
                            for el in response_objects:
                                if el['name'] == place:
                                    # название достопримечательности
                                    name = el['name']

                                    # id достопримечательности
                                    id_object = el['id']

                                    # информация об обьекте
                                    info_object = f'https://xn--26-6kcaa1auatb4dhgcjdif5fui.xn--p1ai/api/object/{id_object}'
                                    info = requests.get(info_object)
                                    info = info.json()

                                    # описание достопримечательности
                                    description = info['description']
                                    description = html2text.html2text(description)

                                    # фото достопримечательности
                                    image = f"https://xn--26-6kcaa1auatb4dhgcjdif5fui.xn--p1ai/cache/thumb/{el['image']}"

                                    # координаты достопримечательности
                                    cords = f"{el['lat']} {el['lon']}"

                                    for i in response_area:
                                        if i['id'] == el['district_id']:
                                            district = i['name']

                            dist_lst.append(district)

                            # создание кнопок
                            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                            wet = types.KeyboardButton('Узнать погоду')
                            markup.add(wet)

                            # отправка фото достопримечательности
                            bot.send_photo(message.chat.id, image)

                            # если сообщение слишком длинное
                            if len(description) < 4096:
                                # отправка сообщения
                                bot.send_message(message.chat.id, f'*{name}*\n\n'
                                                                  f'[{cords}](https://yandex.ru/maps/36/stavropol/?ll={cords.split()[1]}%2'
                                                                  f'C{cords.split()[0]}&mode=whatshere&whatshere%5Bpoint%5D={cords.split()[1]}%'
                                                                  f'2C{cords.split()[0]}&whatshere%5Bzoom%5D=16&z=15)\n\n'
                                                                  f'{district}\n\n'
                                                                  f'{description}', parse_mode='Markdown',
                                                 reply_markup=markup)
                            else:
                                for x in range(0, len(description), 4096):
                                    # отправка сообщения
                                    bot.send_message(message.chat.id, description[x:x + 4096])
                            return
                        except Exception:
                            # отправка сообщения
                            bot.send_message(message.chat.id, 'Ошибка', parse_mode='Markdown')
                    else:
                        bot.send_message(message.chat.id, 'На этих выходных лучше остаться дома', parse_mode='Markdown')
                    break


    # если пользователь отвечает да
    elif message.text in yes:
        msg = bot.send_message(message.chat.id, f'Хочешь отправиться в путешествие?',
                               parse_mode='Markdown')

        # отправка сообщения
        # следующая по очереди фунция 'yes_or_not'
        bot.register_next_step_handler(msg, yes_or_not)

    # если пользователь хочет узнать ближайший отель
    elif message.text in hotel:
        # отправка сообщения
        bot.send_message(message.chat.id, f'К сожалению, у меня нет данных о гостиницах. \U0001F622',
                         parse_mode='Markdown')

    # если пользователь хочет узнать куда поехать
    elif message.text in do:
        msg = bot.send_message(message.chat.id, f'Отлично! Хотите отправиться в путешествие?',
                               parse_mode='Markdown')

        # отправка сообщения
        # следующая по очереди фунция 'yes_or_not'
        bot.register_next_step_handler(msg, yes_or_not)

    # если пользователь хочет узнать погоду
    elif message.text == 'Узнать погоду':
        try:
            # создание кнопок
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            dist_button = types.KeyboardButton('По районам')
            all_button = types.KeyboardButton('Все достопримечательности')
            markup.add(dist_button)
            markup.add(all_button)
            city_name = dist_city_dct[dist_lst[-1]]
            wet_stat = weather(city_name)

            # отправка сообщения
            bot.send_message(message.chat.id, f'Сейчас в {city_name} {wet_stat[0]} ℃, {wet_stat[1]}.\n'
                                              f'Ветер {wet_stat[2]} м/c, влажность -  {wet_stat[3]}%',
                             parse_mode='Markdown', reply_markup=markup)
        except Exception:

            # отправка сообщения
            bot.send_message(message.chat.id, f'Извините, не могу сейчас узнать погоду в этом месте.',
                             parse_mode='Markdown', reply_markup=markup)

    # если бот не понял пользователя
    else:
        # отправка сообщения
        bot.send_message(message.chat.id, f'Я вас не понимаю.', parse_mode='Markdown')


# ответ на 'да' или 'нет'
def yes_or_not(message):
    # если пользователь отвечает да
    if message.text in yes:
        msg = bot.send_message(message.chat.id, f'Вот список районов с достопримечательностями. Выбирай.',
                               parse_mode='Markdown')
        # создание кнопок
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        back = types.KeyboardButton('Назад')
        markup.add(back)
        for el in response_area:
            button = types.KeyboardButton(el['name'])
            markup.add(button)
        bot.send_message(message.chat.id, 'Выберите район', reply_markup=markup)

        # отправка сообщения
        # следующая по очереди фунция 'get_user_text'
        bot.register_next_step_handler(msg, get_user_text)

    # если пользователь приветсвует бота
    elif message.text in hi:
        msg = bot.send_message(message.chat.id, f'Хочешь отправиться в путешествие?',
                               parse_mode='Markdown')

        # отправка сообщения
        # следующая по очереди фунция 'yes_or_not'
        bot.register_next_step_handler(msg, yes_or_not)

    # если пользователь отвечает нет
    elif message.text in no:
        msg = bot.send_message(message.chat.id, f'Тогда я отдохну. \U0001F634', parse_mode='Markdown')

        # отправка сообщения
        # следующая по очереди фунция 'get_user_text'
        bot.register_next_step_handler(msg, get_user_text)

    # если пользователь хочет узнать ближайший отель
    elif message.text in hotel:
        msg = bot.send_message(message.chat.id, f'К сожалению, у меня нет данных о гостиницах. \U0001F622',
                               parse_mode='Markdown')

        # отправка сообщения
        # следующая по очереди фунция 'get_user_text'
        bot.register_next_step_handler(msg, get_user_text)

    # если пользователь хочет узнать куда поехать
    elif message.text in do:
        msg = bot.send_message(message.chat.id, f'Отлично! Хотите отправиться в путешествие?',
                               parse_mode='Markdown')

        # отправка сообщения
        # следующая по очереди фунция 'get_user_text'
        bot.register_next_step_handler(msg, get_user_text)

    # если пользователь бот не понял пользователя
    else:
        msg = bot.send_message(message.chat.id, f'Я вас не понимаю.', parse_mode='Markdown')

        # отправка сообщения
        # следующая по очереди фунция 'get_user_text'
        bot.register_next_step_handler(msg, get_user_text)


# погода
def weather(city_name):
    try:
        # подключений к api
        config_dict = get_default_config()
        config_dict['language'] = 'ru'

        # токен
        owm = OWM('4ffbfb8067b16513c81acdfe9df4454d')

        # город
        city = city_name

        # получение данных
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(city)
        w = observation.weather

        # получение температуры
        temperature = w.temperature('celsius')['temp']

        # получение статуса
        status = w.detailed_status

        # получение скорости ветра
        wind = w.wind()['speed']

        # получение влажности
        humidity = w.humidity

        # возвращение результата
        return (temperature, status, wind, humidity)
    except NotFoundError:
        pass


bot.polling(none_stop=True)
