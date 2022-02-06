import telebot
from datebase import *
import msglist
import mail
from time import time
import conf
bot = telebot.TeleBot(conf.token)



def select_data_user(id):
    with db:
        user = User.get(message_chat_id=id)
        return {'name': user.name, 'city': user.city, 'phone': user.phone, 'mail': user.mail,
                'platform_type': user.platform_type}


def insertOrUpdate(id, typePlace, data):
    tpd = {'1': 'Магазин', '2': 'Интернет магазин', '3': 'Инстаграм'}
    if typePlace == 'name':
        User.insert(message_chat_id=id, name=data) \
            .on_conflict(
            conflict_target=[User.message_chat_id],
            update={User.name: data}) \
            .execute()
    elif typePlace == 'city':
        User.insert(message_chat_id=id, city=data) \
            .on_conflict(
            conflict_target=[User.message_chat_id],
            update={User.city: data}) \
            .execute()
    elif typePlace == 'phone':
        User.insert(message_chat_id=id, phone=data) \
            .on_conflict(
            conflict_target=[User.message_chat_id],
            update={User.phone: data}) \
            .execute()
    elif typePlace == 'mail':
        User.insert(message_chat_id=id, mail=data) \
            .on_conflict(
            conflict_target=[User.message_chat_id],
            update={User.mail: data}) \
            .execute()
    elif typePlace == 'pt':
        User.insert(message_chat_id=id, platform_type=tpd.get(data)) \
            .on_conflict(
            conflict_target=[User.message_chat_id],
            update={User.platform_type: tpd.get(data)}) \
            .execute()
    else:
        print("Ошибка, нету такого типа:", typePlace)


# Начали и спросили имя
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, msglist.start_msg)
    msg = bot.send_message(message.chat.id, msglist.name_msg)
    bot.register_next_step_handler(msg, city_msg)


# Записали имя и спросили город
def city_msg(message):
    insertOrUpdate(message.chat.id, 'name', message.text)

    msg = bot.send_message(message.chat.id, msglist.city_msg)
    bot.register_next_step_handler(msg, pf_msg)


# Записали город и спросили платформу
def pf_msg(message):
    insertOrUpdate(message.chat.id, 'city', message.text)

    msg = bot.send_message(message.chat.id, msglist.pt_msg)
    bot.register_next_step_handler(msg, phone_msg)


# Записали город и спросили платформу
def phone_msg(message):
    insertOrUpdate(message.chat.id, 'pt', message.text)

    msg = bot.send_message(message.chat.id, msglist.phone)
    bot.register_next_step_handler(msg, mail_question)


# Спросили нужна ли почта
def mail_question(message):
    insertOrUpdate(message.chat.id, 'phone', message.text)

    msg = bot.send_message(message.chat.id, msglist.mail_question)
    bot.register_next_step_handler(msg, mail_msg)


# Записали платформу и спросили mail
def mail_msg(message):
    if message.text == 'Да' or message.text == 'да':
        msg = bot.send_message(message.chat.id, msglist.mail_msg)
        bot.register_next_step_handler(msg, send_finish_mail)
    else:
        send_finish(message)


# Записали почту и должны будем отправлять итоговое сообщение
def send_finish(message):
    bot.send_message(message.chat.id, msglist.finish_msg)
    mail.send_email(select_data_user(message.chat.id))


# Записали почту и должны будем отправлять итоговое сообщение
def send_finish_mail(message):
    insertOrUpdate(message.chat.id, 'mail', message.text)
    bot.send_message(message.chat.id, msglist.finish_msg)
    mail.send_email(select_data_user(message.chat.id))


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)
