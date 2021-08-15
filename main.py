import time
import telebot
import config
import json
from datetime import date
from datetime import datetime

# telegram

bot = telebot.TeleBot(config.TOKEN)

with open("config.json", "r") as f:
    config_json = json.load(f)

keyboard_start = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add('Мероприятия').row(
    'Предложить мероприятие')
keyboard_chief = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add('Выложить мероприятие').row('Добавить '
                                                                                                         'админа',
                                                                                                         'Удалить '
                                                                                                         'админа',
                                                                                                         'Рассылка',
                                                                                                         'Ответить',
                                                                                                         'Реклама',
                                                                                                         'Мероприятия')
keyboard_admin = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add('Выложить мероприятие').row('Реклама',
                                                                                                         'Мероприятия')
keyboard_type = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add('Предстоящее').add('Текущее') \
    .add('Прошедшее').add('Назад')
help_message = "/start - запуск бота\n/mailing - включение/выключение рассылки в данном чате\n/mailing_group - " \
               "включение/выключение рассылки в группе\n/help - получение " \
               "информации о боте \n /ad - по поводу рекламы"


def forward(string):
    t = 0
    for i_2 in config_json['id']:
        if t > 20:
            t = 0
            time.sleep(30)
        if config_json['id'][i_2]:
            try:
                bot.send_message(i_2, string)
                t += 1
            except:
                config_json['id'][i_2] = False
                continue


def relevanceEvent(dateEvent):
    return date(datetime.now().year, datetime.now().month, datetime.now().day) > dateEvent


def relevanceEvent2(number, day):
    a = relevanceEvent(date(
        int(((day.partition('.')[2]).partition('.')[2]).partition('-')[0]),
        int((day.partition('.')[2]).partition('.')[0]),
        int(day.partition('.')[0])))
    b = relevanceEvent(date(
        int(((((day.partition('.')[2]).partition('.')[2]).partition('-')[2]).partition(
            '.')[2]).partition('.')[2]),
        int(((((day.partition('.')[2]).partition('.')[2]).partition('-')[2]).partition(
            '.')[2]).partition('.')[0]),
        int((((day.partition('.')[2]).partition('.')[2]).partition('-')[2]).partition(
            '.')[0])))
    if not a and not b:
        config_json['event'][number]['status'] = 'Предстоящее'
    elif a and not b:
        config_json['event'][number]['status'] = 'Текущее'
    else:
        config_json['event'][number]['status'] = 'Прошедшее'


@bot.message_handler(commands=['mailing'])
def mailing(message):
    if not str(message.chat.id) in config_json['id']:
        config_json['id'][str(message.chat.id)] = True
        with open("config.json", "w") as file:
            json.dump(config_json, file)
        bot.send_message(message.chat.id, "On", reply_markup=keyboard_start)
    else:
        if config_json['id'][str(message.chat.id)]:
            config_json['id'][str(message.chat.id)] = False
            with open("config.json", "w") as file:
                json.dump(config_json, file)
            bot.send_message(message.chat.id, "Off", reply_markup=keyboard_start)
        else:
            config_json['id'][str(message.chat.id)] = True
            with open("config.json", "w") as file:
                json.dump(config_json, file)
            bot.send_message(message.chat.id, "On", reply_markup=keyboard_start)


@bot.message_handler(commands=['mailing_group'])
def mailing_group(message):
    bot.send_message(message.chat.id, "Введите id группы")
    bot.register_next_step_handler(message, mailing_group_add)


def mailing_group_add(message):
    try:
        bot.send_message(str(message.text), "LP bot connected")
        if not str(message.text) in config_json['id']:
            config_json['id'][str(message.text)] = True
            with open("config.json", "w") as file:
                json.dump(config_json, file)
            bot.send_message(message.chat.id, "On", reply_markup=keyboard_start)
        else:
            if config_json['id'][str(message.text)]:
                config_json['id'][str(message.text)] = False
                with open("config.json", "w") as file:
                    json.dump(config_json, file)
                    bot.send_message(message.chat.id, "Off", reply_markup=keyboard_start)
            else:
                config_json['id'][str(message.text)] = True
                with open("config.json", "w") as file:
                    json.dump(config_json, file)
                bot.send_message(message.chat.id, "On", reply_markup=keyboard_start)
    except:
        bot.send_message(message.chat.id, "Данные введены неккоректно")


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Привет, это Life-Programming-bot", reply_markup=keyboard_start)


@bot.message_handler(commands=['ad'])
def ad(message):
    bot.send_message(message.chat.id, "Введите текст рекламы")
    bot.register_next_step_handler(message, ad_in)


def ad_in(message):
    for i_ad_in in config_json['id_chief']:
        bot.send_message(i_ad_in, "Реклама" + '\n' + str(message.chat.id) + '\n' + message.text)
    config_json['admin']['event'][len(config_json['admin']['ad'])] = "Реклама" + '\n' + str(
        message.chat.id) + '\n' + message.text
    with open("config.json", "w") as file:
        json.dump(config_json, file)
    bot.send_message(message.chat.id, "Ваше предложение проходит проверку")


@bot.message_handler(commands=['help'])
def help_command(message):
    if str(message.chat.id) in config_json['id_chief']:
        if config_json['id_chief'][str(message.chat.id)]:
            bot.send_message(message.chat.id, help_message + '\n' + "/special - спец команды (уровень доступа "
                                                                    "1)\n/update_json - обновление "
                                                                    "config.json\n/update_event - обновление "
                                                                    "актуальности событий")
        elif str(message.chat.id) in config_json['id_admin']:
            if config_json['id_admin'][str(message.chat.id)]:
                bot.send_message(message.chat.id, help_message + '\n' + "/special - спец.команды (уровень доступа "
                                                                        "2)\n/update_json - обновление "
                                                                        "config.json\n/update_event - обновление "
                                                                        "актуальности событий")
            else:
                bot.send_message(message.chat.id, help_message)
        else:
            bot.send_message(message.chat.id, help_message)
    elif str(message.chat.id) in config_json['id_admin']:
        if config_json['id_admin'][str(message.chat.id)]:
            bot.send_message(message.chat.id, help_message + '\n' + "/special - спец.команды (уровень доступа "
                                                                    "2)\n/update_json - обновление "
                                                                    "config.json\n/update_event - обновление "
                                                                    "актуальности событий")
        else:
            bot.send_message(message.chat.id, help_message)
    else:
        bot.send_message(message.chat.id, help_message)


@bot.message_handler(commands=['update_json'])
def update_json(message):
    global config_json
    with open("config.json", "r") as f:
        config_json = json.load(f)
    bot.send_message(message.chat.id, "Ok")


@bot.message_handler(commands=['update_event'])
def update_event(message):
    for i in config_json['event']:
        eventDate = config_json['event'][i]['date']
        config_json['event'][i]['start'] = relevanceEvent(date(
            int(((eventDate.partition('.')[2]).partition('.')[2]).partition('-')[0]),
            int((eventDate.partition('.')[2]).partition('.')[0]),
            int(eventDate.partition('.')[0])))
        config_json['event'][i]['end'] = relevanceEvent(date(
            int(((((eventDate.partition('.')[2]).partition('.')[2]).partition('-')[2]).partition(
                '.')[2]).partition('.')[2]),
            int(((((eventDate.partition('.')[2]).partition('.')[2]).partition('-')[2]).partition(
                '.')[2]).partition('.')[0]),
            int((((eventDate.partition('.')[2]).partition('.')[2]).partition('-')[2]).partition(
                '.')[0])))
    with open("config.json", "w") as file:
        json.dump(config_json, file)
    bot.send_message(message.chat.id, "Ok")


@bot.message_handler(commands=['special'])
def special(message):
    if str(message.chat.id) in config_json['id_admin']:
        if (str(message.chat.id)) in config_json['id_chief']:
            bot.send_message(message.chat.id, 'Выберите категорию:', reply_markup=keyboard_chief)
            bot.register_next_step_handler(message, chief)
        else:
            bot.send_message(message.chat.id, 'Выберите категорию:', reply_markup=keyboard_admin)
            bot.register_next_step_handler(message, admin)
    else:
        bot.send_message(message.chat.id, "Error 1: Вы не имеете доступа к данной команде")


def admin(message):
    if message.text.lower() == "выложить мероприятие":
        bot.send_message(message.chat.id, "Введите название мероприятия")
        bot.register_next_step_handler(message, setEvent_name)
    elif message.text.lower() == 'мероприятия':
        for event_i in config_json['admin']['event']:
            bot.send_message(message.chat.id, config_json['admin']['event'][event_i])


def chief(message):
    if message.text.lower() == "добавить админа":
        bot.send_message(message.chat.id, "Введите id")
        bot.register_next_step_handler(message, setAdmin)
    elif message.text.lower() == "удалить админа":
        bot.send_message(message.chat.id, "Введите id")
        bot.register_next_step_handler(message, delAdmin)
    elif message.text.lower() == "выложить мероприятие":
        bot.send_message(message.chat.id, "Введите название мероприятия")
        bot.register_next_step_handler(message, setEvent_name)
    elif message.text.lower() == "рассылка":
        bot.send_message(message.chat.id, "Введите текст рассылки")
        bot.register_next_step_handler(message, distribution)
    elif message.text.lower() == 'ответить':
        bot.send_message(message.chat.id, "Введите id")
        bot.register_next_step_handler(message, reply2)
    elif message.text.lower() == 'реклама':
        for ad_i in config_json['admin']['ad']:
            bot.send_message(message.chat.id, config_json['admin']['ad'][ad_i])
    elif message.text.lower() == 'мероприятия':
        for event_i in config_json['admin']['event']:
            bot.send_message(message.chat.id, config_json['admin']['event'][event_i])


def reply2(message):
    bot.send_message(message.chat.id, "Введите сообщение")
    bot.register_next_step_handler(message, reply3, message.text)


def reply3(message, messId):
    try:
        bot.send_message(messId, message.text)
        bot.send_message(message.chat.id, "Ok")
    except:
        bot.send_message(message.chat.id, "Неккоректные данные")


def distribution(message):
    forward(message.text)


def setEvent_name(message):
    number = str(len(config_json['event']))
    config_json['event'][number] = {'name': "", "type": "", "date": "", "description": "", "link": ""}
    config_json['event'][number]['name'] = message.text
    bot.send_message(message.chat.id, "Введите тип мероприятия")
    bot.register_next_step_handler(message, setEvent_type, str(int(number)))


def setEvent_type(message, number):
    config_json['event'][number]['type'] = message.text
    bot.send_message(message.chat.id, "Введите дату мероприятия")
    bot.register_next_step_handler(message, setEvent_date, number)


def setEvent_date(message, number):
    try:
        if len(str(((message.text.partition('.')[2]).partition('.')[2]).partition('-')[0])) != 4:
            raise
        if not date(
                int(((message.text.partition('.')[2]).partition('.')[2]).partition('-')[0]),
                int((message.text.partition('.')[2]).partition('.')[0]),
                int(message.text.partition('.')[0])) < date(
            int(((((message.text.partition('.')[2]).partition('.')[2]).partition('-')[2]).partition(
                '.')[2]).partition('.')[2]),
            int(((((message.text.partition('.')[2]).partition('.')[2]).partition('-')[2]).partition(
                '.')[2]).partition('.')[0]),
            int((((message.text.partition('.')[2]).partition('.')[2]).partition('-')[2]).partition(
                '.')[0])):
            raise
        if len(str(((((message.text.partition('.')[2]).partition('.')[2]).partition('-')[2]).partition(
                '.')[2]).partition('.')[2])) != 4:
            raise
        config_json['event'][number]['date'] = message.text
        relevanceEvent2(number, message.text)

        bot.send_message(message.chat.id, "Введите ссылку на мероприятие")
        bot.register_next_step_handler(message, setEvent_link, number)
    except:
        bot.send_message(message.chat.id, "Неккоректные данные, введите снова")
        bot.register_next_step_handler(message, setEvent_date, number)


def setEvent_link(message, number):
    config_json['event'][number]['link'] = message.text
    bot.send_message(message.chat.id, "Введите описание мероприятия")
    bot.register_next_step_handler(message, setEvent_description, number)


def setEvent_description(message, number):
    config_json['event'][number]['description'] = message.text
    with open("config.json", "w") as file:
        json.dump(config_json, file)
    forward(config_json['event'][number]['name'] + '\nТип: ' + config_json['event'][number]['type'] + '\nСтатус: ' + \
            config_json['event'][number]['status'] + '\nПроходит ' + config_json['event'][number][
                'date'] + '\nОписание: ' + config_json['event'][number]['description'] + '\nПодробнее: ' + \
            config_json['event'][number]['link'])


def delAdmin(message):
    if message.text in config_json['id_admin']:
        config_json['id_admin'][str(message.text)] = False
        with open("config.json", "w") as file:
            json.dump(config_json, file)
        bot.send_message(message.chat.id, "Ok")


def setAdmin(message):
    try:
        bot.send_message(message.text, "Test admin in LP bot")
        config_json['id_admin'][str(message.text)] = True
        with open("config.json", "w") as file:
            json.dump(config_json, file)
        bot.send_message(message.chat.id, "Ok")
    except:
        bot.send_message(message.chat.id, "Error")
        bot.send_message(message.chat.id, "Введите id")
        bot.register_next_step_handler(message, setAdmin)


@bot.message_handler(content_types=['text'])
def menu(message):
    if message.text.lower() == 'предложить мероприятие':
        try:
            bot.send_message(message.chat.id, "Введите название мероприятия")
            bot.register_next_step_handler(message, name)
        except:
            bot.send_message(message.chat.id, "Данные введены неккоректно")
    elif message.text.lower() == 'мероприятия':
        bot.send_message(message.chat.id, "Выберите тип", reply_markup=keyboard_type)
        bot.register_next_step_handler(message, typeEvent)


def typeEvent(message):
    if message.text.lower() == 'предстоящее' or message.text.lower() == 'текущее' \
            or message.text.lower() == 'прошедшее':
        for i2 in config_json['event']:
            if str(config_json['event'][i2]['status']) == str(message.text):
                bot.send_message(message.chat.id,
                                 config_json['event'][i2]['name'] + '\nТип: ' + config_json['event'][i2][
                                     'type'] + '\nСтатус: ' +
                                 config_json['event'][i2]['status'] + '\nПроходит ' + config_json['event'][i2][
                                     'date'] + '\nОписание: ' + config_json['event'][i2][
                                     'description'] + '\nПодробнее: ' +
                                 config_json['event'][i2]['link'])
        bot.register_next_step_handler(message, typeEvent)
    elif message.text.lower() == "назад":
        bot.send_message(message.chat.id, "Выберите пункт", reply_markup=keyboard_start)
    else:
        bot.send_message(message.chat.id, "Выберите тип", reply_markup=keyboard_type)
        bot.register_next_step_handler(message, typeEvent)


def name(message):
    try:
        bot.send_message(message.chat.id, "Введите ссылку на мероприятие")
        bot.register_next_step_handler(message, link, message.text)
    except:
        bot.send_message(message.chat.id, "Данные введены неккоректно")
        bot.send_message(message.chat.id, "Введите название мероприятия")
        bot.register_next_step_handler(message, name)


def link(message, message_name):
    try:
        for il in config_json['id_admin']:
            if config_json['id_admin'][il]:
                bot.send_message(il, str(message.chat.id) + '\n' + message_name + '\n' + message.text)
        config_json['admin']['event'][len(config_json['admin']['event'])] = str(
            message.chat.id) + '\n' + message_name + '\n' + message.text
        with open("config.json", "w") as file:
            json.dump(config_json, file)
    except:
        bot.send_message(message.chat.id, "Данные введены неккоректно")
        bot.send_message(message.chat.id, "Введите ссылку на мероприятие")
        bot.register_next_step_handler(message, link, message.text)


bot.polling()
