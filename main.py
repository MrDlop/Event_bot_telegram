import time

from telegram import ReplyKeyboardMarkup

import config
import json
from datetime import date
from datetime import datetime
import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from data import db_session, users, user_types, offers, event_types, events

db_session.global_init("databases/db.db")

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(update, context)s', level=logging.DEBUG
# )
#
# logger = logging.getLogger(__name__)

#  init keyboard
keyboard_start = ReplyKeyboardMarkup([
    ['Мероприятия'],
    ['Предложить мероприятие']
], one_time_keyboard=False)
keyboard_admin_0 = ReplyKeyboardMarkup([
    ['Выложить мероприятие'],
    ['Добавить админа'],
    ['Удалить админа'],
    ['Рассылка'],
    ['Ответить'],
    ['Реклама'],
    ['Мероприятия']
], one_time_keyboard=False)
keyboard_admin_1 = ReplyKeyboardMarkup([
    ['Выложить мероприятие'],
    ['Реклама'],
    ['Мероприятия']
], one_time_keyboard=False)
keyboard_type = ReplyKeyboardMarkup([
    ['Предстоящее'],
    ['Текущее'],
    ['Прошедшее'],
    ['Назад']
], one_time_keyboard=False)
help_message = "/start - запуск бота\n/mailing - включение/выключение рассылки в данном чате\n/mailing_group - " \
               "включение/выключение рассылки в группе\n/help - получение " \
               "информации о боте \n /ad - по поводу рекламы"


# async def forward(string):
#     t = 0
#     for i_2 in config_json['id']:
#         if t > 20:
#             t = 0
#             time.sleep(30)
#         if config_json['id'][i_2]:
#             try:
#                 bot.send_message(i_2, string)
#                 t += 1
#             except:
#                 config_json['id'][i_2] = False
#                 continue

async def mailing(update, context):
    db_sess = db_session.create_session()
    sensor_all = db_sess.query(users.User).filter(users.User.telegram_id == str(update.message.chat_id)).all()
    if len(sensor_all) == 0:
        db_sess = db_session.create_session()
        new_chat = users.User()
        new_chat.type = "user"
        new_chat.telegram_id = str(update.message.chat_id)
        new_chat.distribution = 1
        db_sess.add(new_chat)
        db_sess.commit()
        db_sess.close()
        await update.message.reply_text("On")
        return ConversationHandler.END
    sensor = sensor_all[0].distribution
    if sensor:
        sensor_all[0].distribution = not sensor
        await update.message.reply_text("Off")
    else:
        sensor_all[0].distribution = not sensor
        await update.message.reply_text("On")
    db_sess.commit()
    db_sess.close()


async def mailing_group(update, context):
    await update.message.reply_text("Введите id группы", reply_markup=keyboard_start)
    return 1


async def mailing_group_add(update, context):
    try:
        await update.message.reply_text("Введите id группы")
        context.bot.send_message(str(update.message.text), "LP bot connected")
        db_sess = db_session.create_session()
        sensor_all = db_sess.query(users.User).filter(users.User.telegram_id == str(update.message.text)).all()
        if len(sensor_all) == 0:
            db_sess = db_session.create_session()
            new_chat = users.User()
            new_chat.type = "user"
            new_chat.telegram_id = str(update.message.text)
            new_chat.distribution = 1
            db_sess.add(new_chat)
            db_sess.commit()
            db_sess.close()
            await update.message.reply_text("On")
            return ConversationHandler.END
        sensor = sensor_all[0].distribution
        if sensor:
            sensor_all[0].distribution = bool(1 - sensor)
            await update.message.reply_text("Off")
        else:
            sensor_all[0].distribution = bool(1 - sensor)
            await update.message.reply_text("On")
        db_sess.close()

    except:
        await update.message.reply_text("Данные введены неккоректно")
    return ConversationHandler.END


async def start_handler(update, context):
    await update.message.reply_text("Привет, это Life-Programming-bot", reply_markup=keyboard_start)
    return "menu"


async def help_command(update, context):
    db_sess = db_session.create_session()

    type_user = db_sess.query(users.User).filter(users.User.telegram_id == str(update.message.chat_id)).first().type
    db_sess.close()
    if type_user == 'user':
        await update.message.reply_text(help_message)
    elif type_user == 'admin_0':
        await update.message.reply_text(help_message + '\n' + "/special - спец команды"
                                                              "\n/update_json - обновление config.json"
                                                              "\n/update_event - обновление "
                                                              "актуальности событий")
    elif type_user == 'admin_1':
        await update.message.reply_text(help_message + '\n' + "/special - спец команды"
                                                              "\n/update_json - обновление config.json"
                                                              "\n/update_event - обновление "
                                                              "актуальности событий")


# async def special(update, context):
#     if str(update.message.chat_id) in config_json['id_admin']:
#         if (str(update.message.chat_id)) in config_json['id_chief']:
#             await update.message.reply_text('Выберите категорию:', reply_markup=keyboard_chief)
#             bot.register_next_step_handler(message, chief)
#         else:
#             await update.message.reply_text('Выберите категорию:', reply_markup=keyboard_admin)
#             bot.register_next_step_handler(message, admin)
#     else:
#         await update.message.reply_text("Error 1: Вы не имеете доступа к данной команде")


# async def admin(update, context):
#     if message.text.lower() == "выложить мероприятие":
#         await update.message.reply_text("Введите название мероприятия")
#         bot.register_next_step_handler(message, setEvent_name)
#     elif message.text.lower() == 'мероприятия':
#         for event_i in config_json['admin']['event']:
#             await update.message.reply_text(config_json['admin']['event'][event_i])


# async def chief(update, context):
#     if message.text.lower() == "добавить админа":
#         await update.message.reply_text("Введите id")
#         bot.register_next_step_handler(message, setAdmin)
#     elif message.text.lower() == "удалить админа":
#         await update.message.reply_text("Введите id")
#         bot.register_next_step_handler(message, delAdmin)
#     elif message.text.lower() == "выложить мероприятие":
#         await update.message.reply_text("Введите название мероприятия")
#         bot.register_next_step_handler(message, setEvent_name)
#     elif message.text.lower() == "рассылка":
#         await update.message.reply_text("Введите текст рассылки")
#         bot.register_next_step_handler(message, distribution)
#     elif message.text.lower() == 'ответить':
#         await update.message.reply_text("Введите id")
#         bot.register_next_step_handler(message, reply2)
#     elif message.text.lower() == 'реклама':
#         for ad_i in config_json['admin']['ad']:
#             await update.message.reply_text(config_json['admin']['ad'][ad_i])
#     elif message.text.lower() == 'мероприятия':
#         for event_i in config_json['admin']['event']:
#             await update.message.reply_text(config_json['admin']['event'][event_i])


# async def reply2(update, context):
#     await update.message.reply_text("Введите сообщение")
#     bot.register_next_step_handler(message, reply3, message.text)


# async def reply3(message, messId):
#     try:
#         bot.send_message(messId, message.text)
#         await update.message.reply_text("Ok")
#     except:
#         await update.message.reply_text("Неккоректные данные")


# async def distribution(update, context):
#     forward(message.text)


# async def setEvent_name(update, context):
#     number = str(len(config_json['event']))
#     config_json['event'][number] = {'name': "", "type": "", "date": "", "description": "", "link": ""}
#     config_json['event'][number]['name'] = message.text
#     await update.message.reply_text("Введите тип мероприятия")
#     bot.register_next_step_handler(message, setEvent_type, str(int(number)))
#
#
# async def setEvent_type(message, number):
#     config_json['event'][number]['type'] = message.text
#     await update.message.reply_text("Введите дату мероприятия")
#     bot.register_next_step_handler(message, setEvent_date, number)
#
#
# async def setEvent_date(message, number):
#     try:
#         if len(str(((message.text.partition('.')[2]).partition('.')[2]).partition('-')[0])) != 4:
#             raise
#         if not date(
#                 int(((message.text.partition('.')[2]).partition('.')[2]).partition('-')[0]),
#                 int((message.text.partition('.')[2]).partition('.')[0]),
#                 int(message.text.partition('.')[0])) < date(
#             int(((((message.text.partition('.')[2]).partition('.')[2]).partition('-')[2]).partition(
#                 '.')[2]).partition('.')[2]),
#             int(((((message.text.partition('.')[2]).partition('.')[2]).partition('-')[2]).partition(
#                 '.')[2]).partition('.')[0]),
#             int((((message.text.partition('.')[2]).partition('.')[2]).partition('-')[2]).partition(
#                 '.')[0])):
#             raise
#         if len(str(((((message.text.partition('.')[2]).partition('.')[2]).partition('-')[2]).partition(
#                 '.')[2]).partition('.')[2])) != 4:
#             raise
#         config_json['event'][number]['date'] = message.text
#         relevanceEvent2(number, message.text)
#
#         await update.message.reply_text("Введите ссылку на мероприятие")
#         bot.register_next_step_handler(message, setEvent_link, number)
#     except:
#         await update.message.reply_text("Неккоректные данные, введите снова")
#         bot.register_next_step_handler(message, setEvent_date, number)
#
#
# async def setEvent_link(message, number):
#     config_json['event'][number]['link'] = message.text
#     await update.message.reply_text("Введите описание мероприятия")
#     bot.register_next_step_handler(message, setEvent_description, number)
#
#
# async def setEvent_description(message, number):
#     config_json['event'][number]['description'] = message.text
#     with open("config.json", "w") as file:
#         json.dump(config_json, file)
#     forward(config_json['event'][number]['name'] + '\nТип: ' + config_json['event'][number]['type'] + '\nСтатус: ' + \
#             config_json['event'][number]['status'] + '\nПроходит ' + config_json['event'][number][
#                 'date'] + '\nОписание: ' + config_json['event'][number]['description'] + '\nПодробнее: ' + \
#             config_json['event'][number]['link'])
#
#
# async def delAdmin(update, context):
#     if message.text in config_json['id_admin']:
#         config_json['id_admin'][str(message.text)] = False
#         with open("config.json", "w") as file:
#             json.dump(config_json, file)
#         await update.message.reply_text("Ok")
#
#
# async def setAdmin(update, context):
#     try:
#         bot.send_message(message.text, "Test admin in LP bot")
#         config_json['id_admin'][str(message.text)] = True
#         with open("config.json", "w") as file:
#             json.dump(config_json, file)
#         await update.message.reply_text("Ok")
#     except:
#         await update.message.reply_text("Error")
#         await update.message.reply_text("Введите id")
#         bot.register_next_step_handler(message, setAdmin)
#
#


async def ad(update, context):
    await update.message.reply_text("Введите текст рекламы")
    return 1


async def ad_in(update, context):
    db_sess = db_session.create_session()
    offer = offers.Offer()
    offer.is_event = 0
    offer.name = update.message.text
    offer.ref = update.message.chat_id
    db_sess.add(offer)
    db_sess.commit()
    db_sess.close()
    await update.message.reply_text("Ваше предложение проходит проверку")
    return ConversationHandler.END


async def menu(update, context):
    if update.message.text.lower() == 'предложить мероприятие':
        await update.message.reply_text("Введите название мероприятия")
        return "name"
    elif update.message.text.lower() == 'мероприятия':
        await update.message.reply_text("Выберите тип", reply_markup=keyboard_type)
        return "typeEvent"


async def typeEvent(update, context):
    if update.message.text.lower() == 'предстоящее':
        i = 0
        pass
    # if message.text.lower() == 'предстоящее' or message.text.lower() == 'текущее' \
    #         or message.text.lower() == 'прошедшее':
    #     for i2 in config_json['event']:
    #         if str(config_json['event'][i2]['status']) == str(message.text):
    #             await update.message.reply_text(
    #                 config_json['event'][i2]['name'] + '\nТип: ' + config_json['event'][i2][
    #                     'type'] + '\nСтатус: ' +
    #                 config_json['event'][i2]['status'] + '\nПроходит ' + config_json['event'][i2][
    #                     'date'] + '\nОписание: ' + config_json['event'][i2][
    #                     'description'] + '\nПодробнее: ' +
    #                 config_json['event'][i2]['link'])
    #     bot.register_next_step_handler(message, typeEvent)
    # elif message.text.lower() == "назад":
    #     await update.message.reply_text("Выберите пункт", reply_markup=keyboard_start)
    # else:
    #     await update.message.reply_text("Выберите тип", reply_markup=keyboard_type)
    #     bot.register_next_step_handler(message, typeEvent)


async def name(update, context):
    try:
        await update.message.reply_text("Введите ссылку на мероприятие")
        context.user_data['name'] = update.message.text
        return "link"
    except:
        await update.message.reply_text("Данные введены неккоректно")
        await update.message.reply_text("Введите название мероприятия")
        return "name"


async def link(update, context):
    try:
        db_sess = db_session.create_session()
        offer = offers.Offer()
        offer.is_event = 1
        offer.name = context.user_data['name']
        offer.ref = update.message.text
        db_sess.add(offer)
        db_sess.commit()
        db_sess.close()
        await update.message.reply_text("Мероприятие отправлено на проверку")
        return ConversationHandler.END
    except:
        await update.message.reply_text("Данные введены неккоректно")
        await update.message.reply_text("Введите ссылку на мероприятие")
        return "link"


def main():
    application = Application.builder().token(config.TOKEN).build()

    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("mailing", mailing))
    # application.add_handler(CommandHandler("update_event", update_event))
    # application.add_handler(CommandHandler("special", special))

    application.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler('mailing_group', mailing_group)],
            states={
                1: [MessageHandler(filters.TEXT & ~filters.COMMAND, mailing_group_add)]
            },
            fallbacks=[CommandHandler('help', help_command)]
        )
    )
    application.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler('start', start_handler)],
            states={
                "menu": [MessageHandler(filters.TEXT & ~filters.COMMAND, menu)],
                "name": [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
                "typeEvent": [MessageHandler(filters.TEXT & ~filters.COMMAND, typeEvent)],
                "link": [MessageHandler(filters.TEXT & ~filters.COMMAND, link)]
            },
            fallbacks=[CommandHandler('help', help_command)]
        )
    )
    application.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler('ad', ad)],
            states={
                1: [MessageHandler(filters.TEXT & ~filters.COMMAND, ad_in)]
            },
            fallbacks=[CommandHandler('help', help_command)]
        )
    )
    application.run_polling()


if __name__ == '__main__':
    main()
