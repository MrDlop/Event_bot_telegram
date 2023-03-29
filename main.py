import asyncio
import datetime

from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler

from data import db_session, users, offers, events
import config

db_session.global_init("databases/db.db")

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
    ['Прошедшее'],
    ['Назад']
], one_time_keyboard=False)
help_message = "/start - запуск бота\n/mailing - включение/выключение рассылки в данном чате\n/mailing_group - " \
               "включение/выключение рассылки в группе\n/help - получение " \
               "информации о боте \n /ad - по поводу рекламы"


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
        await update.message.reply_text(help_message + '\n' + "/special - спец команды")
    elif type_user == 'admin_1':
        await update.message.reply_text(help_message + '\n' + "/special - спец команды")


async def special(update, context):
    db_sess = db_session.create_session()
    type_user = db_sess.query(users.User).filter(users.User.telegram_id == str(update.message.chat_id)).first().type
    db_sess.close()
    if type_user == "admin_1":
        await update.message.reply_text('Выберите категорию:', reply_markup=keyboard_admin_1)
        return "admin_1"
    elif type_user == "admin_0":
        await update.message.reply_text('Выберите категорию:', reply_markup=keyboard_admin_0)
        return "admin_0"
    else:
        await update.message.reply_text("Error 1: Вы не имеете доступа к данной команде")
        return ConversationHandler.END


async def admin_1(update, context):
    if update.message.text.lower() == "выложить мероприятие":
        await update.message.reply_text("Введите название мероприятия")
        return "setEvent_name"
    elif update.message.text.lower() == 'мероприятия':
        db_sess = db_session.create_session()
        event = db_sess.query(offers.Offer).filter(offers.Offer.is_event == 0).all()
        db_sess.close()
        for event_i in event:
            await update.message.reply_text(event_i)
        return ConversationHandler.END


async def admin_0(update, context):
    if update.message.text.lower() == "добавить админа":
        await update.message.reply_text("Введите id")
        return "setAdmin"
    elif update.message.text.lower() == "удалить админа":
        await update.message.reply_text("Введите id")
        return "delAdmin"
    elif update.message.text.lower() == "выложить мероприятие":
        await update.message.reply_text("Введите название мероприятия")
        return "setEvent_name"
    elif update.message.text.lower() == "рассылка":
        await update.message.reply_text("Введите текст рассылки")
        return "distribution"
    elif update.message.text.lower() == 'ответить':
        await update.message.reply_text("Введите id")
        return "reply2"
    elif update.message.text.lower() == 'реклама':
        db_sess = db_session.create_session()
        ads = db_sess.query(offers.Offer).filter(offers.Offer.is_event == 0).all()
        db_sess.close()
        for ad_i in ads:
            await update.message.reply_text(str(ad_i))
        return ConversationHandler.END
    elif update.message.text.lower() == 'мероприятия':
        print(1)
        db_sess = db_session.create_session()
        event = db_sess.query(offers.Offer).filter(offers.Offer.is_event == 1).all()
        print(event)
        db_sess.close()
        for event_i in event:
            await update.message.reply_text(str(event_i))
        return ConversationHandler.END


async def reply2(update, context):
    await update.message.reply_text("Введите сообщение")
    context.user_data['id'] = update.message.text
    return "reply3"


async def reply3(update, context):
    try:
        context.bot.send_message(context.user_data['id'], update.message.text)
        await update.message.reply_text("Ok")
    except:
        await update.message.reply_text("Неккоректные данные")
    return ConversationHandler.END


async def distribution(update, context):
    db_sess = db_session.create_session()
    user = db_sess.query(users.User).filter(users.User.distribution == 1).all()
    db_sess.close()
    for i in user:
        context.bot.send_message(i.telegram_id, update.message.text)


async def setEvent_name(update, context):
    event = events.Event()
    event.name = update.message.text

    context.user_data['event'] = event

    await update.message.reply_text("Введите тип мероприятия")
    return "setEvent_type"


async def setEvent_type(update, context):
    context.user_data['event'].type = update.message.text
    await update.message.reply_text("Введите дату мероприятия (ДД.ММ.ГГГГ-ДД.ММ.ГГГГ)")
    return "setEvent_date"


async def setEvent_date(update, context):
    try:
        message = update.message.text.split('-')
        date_start = datetime.date(*list(map(int, message[0].split('.')))[::-1])
        date_end = datetime.date(*list(map(int, message[1].split('.')))[::-1])
        context.user_data['event'].date_start = date_start
        context.user_data['event'].date_end = date_end
        await update.message.reply_text("Введите ссылку на мероприятие")
        return "setEvent_link"
    except:
        await update.message.reply_text("Неккоректные данные, введите снова")
        return "setEvent_date"


async def setEvent_link(update, context):
    context.user_data['event'].event = update.message.text
    await update.message.reply_text("Введите описание мероприятия")
    return "setEvent_description"


async def setEvent_description(update, context):
    context.user_data['event'].description = update.message.text
    db_sess = db_session.create_session()
    db_sess.add(context.user_data['event'])
    db_sess.close()
    return ConversationHandler.END


async def delAdmin(update, context):
    db_sess = db_session.create_session()
    db_sess.query(users.User).filter(users.User.telegram_id == str(update.message.text)).delete()
    db_sess.close()
    await update.message.reply_text("Ok")
    return ConversationHandler.END


async def setAdmin(update, context):
    try:
        context.bot.send_message(update.message.text, "Test admin in LP bot")
        db_sess = db_session.create_session()
        db_sess.query(users.User).filter(users.User.telegram_id == str(update.message.text)).first().type = 2
        db_sess.commit()
        db_sess.close()
        await update.message.reply_text("Ok")
    except:
        await update.message.reply_text("Error")
        await update.message.reply_text("Введите id")
        return "setAdmin"


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
        db_sess = db_session.create_session()
        event = db_sess.query(events.Event).filter(events.Event.status == 0).all()
        db_sess.close()
        for i in event:
            await update.message.reply_text(str(i))
        await update.message.reply_text("Выберите тип", reply_markup=keyboard_type)
        return "typeEvent"
    elif update.message.text.lower() == 'прошедшее':
        db_sess = db_session.create_session()
        event = db_sess.query(events.Event).filter(events.Event.status == 1).all()
        db_sess.close()
        for i in event:
            await update.message.reply_text(str(i))
        await update.message.reply_text("Выберите тип", reply_markup=keyboard_type)
        return "typeEvent"
    else:
        await update.message.reply_text("Привет, это Life-Programming-bot", reply_markup=keyboard_start)
        return "menu"


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


async def update_event(update, context):
    db_sess = db_session.create_session()
    cm = db_sess.query(events.Event).all()
    for i in range(len(cm)):
        if cm[i].date_start >= datetime.datetime.now():
            cm[i].status = 1
        else:
            cm[i].status = 0
    db_sess.commit()
    db_sess.close()


def main():
    application = Application.builder().token(config.TOKEN).build()

    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("mailing", mailing))
    application.add_handler(CommandHandler("update_event", update_event))

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
    application.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler('special', special)],
            states={
                "admin_0": [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_0)],
                "admin_1": [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_1)],
                "setAdmin": [MessageHandler(filters.TEXT & ~filters.COMMAND, setAdmin)],
                "delAdmin": [MessageHandler(filters.TEXT & ~filters.COMMAND, delAdmin)],
                "setEvent_name": [MessageHandler(filters.TEXT & ~filters.COMMAND, setEvent_name)],
                "setEvent_type": [MessageHandler(filters.TEXT & ~filters.COMMAND, setEvent_type)],
                "setEvent_date": [MessageHandler(filters.TEXT & ~filters.COMMAND, setEvent_date)],
                "setEvent_link": [MessageHandler(filters.TEXT & ~filters.COMMAND, setEvent_link)],
                "setEvent_description": [MessageHandler(filters.TEXT & ~filters.COMMAND, setEvent_description)],
                "distribution": [MessageHandler(filters.TEXT & ~filters.COMMAND, distribution)],
                "reply2": [MessageHandler(filters.TEXT & ~filters.COMMAND, reply2)],
                "reply3": [MessageHandler(filters.TEXT & ~filters.COMMAND, reply3)],
            },
            fallbacks=[CommandHandler('help', help_command)]
        )
    )

    application.run_polling()


if __name__ == '__main__':
    main()
