import smtplib
from email.mime.text import MIMEText
import conf


def send_email(data):
    sender = conf.sender
    password = conf.password
    receiver = conf.receiver

    text = 'Имя клиента: ' + str(data.get('name')) \
           + '\nГород: ' + str(data.get('city')) \
           + '\nТип платформы: ' + str(data.get('platform_type')) + '\n'

    if data.get('phone') is not None:
        text = text + 'Телефон: ' + str(data.get('phone')) + '\n'
    if data.get('mail') is not None:
        text = text + 'Почта: ' + str(data.get('mail')) + '\n'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    print(text)
    msg = MIMEText(text)

    msg['Subject'] = 'Данные о клиентах от бота'
    msg['From'] = sender
    msg['To'] = receiver

    server.ehlo()
    server.starttls()

    try:
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string().encode('utf-8'))
        return "The message was sent successfully!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"

