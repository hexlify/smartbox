import RPi.GPIO as GPIO
from time import sleep, time
import telebot
import os
from mailbox import Mailbox
from threading import Thread

# настраиваю GPIO выходы для сенсора
TRIG = 23
ECHO = 24

# телеграм бот
token = os.getenv('BOT_TOKEN')

# твой телеграм профиль
me = os.getenv('CHAT_ID')

bot = telebot.TeleBot(token=token, parse_mode=None)
m = Mailbox()


def tranlate(t):
    return 'Новое письмо'.ljust(26) if t == 'new_mail' else 'Вы почистили ящик'.ljust(20)


@bot.message_handler(commands=['history'])
def get_history(message):
    events = m.history()
    history = 'Пусто' if len(events) == 0 else '\n'.join(
        map(lambda t: f"{tranlate(t[1])}`{t[0]}`", events))
    bot.reply_to(
        message, f'Вот история за последние 7 дней:\n\n{history}', parse_mode="MarkdownV2")


@bot.message_handler(commands=['status'])
def get_status(message):
    bot.reply_to(message, f"Новых писем: {m.mail_count}")


@bot.message_handler(commands=['empty'])
def empty_mailbox(message):
    m.clear()
    bot.reply_to(message, "Ящик почищен")


@bot.message_handler(func=lambda _: True)
def unknown_command(message):
    bot.reply_to(message, "Извини, я не знаю такую команду")


# получить расстояние с сенсора
def get_distance():
    GPIO.output(TRIG, False)
    sleep(1)

    GPIO.output(TRIG, True)
    sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = time()
    while GPIO.input(ECHO) == 0:
        pulse_start = time()

    pulse_end = time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time()

    pulse_duration = pulse_end - pulse_start
    return 17150 * pulse_duration


def run_sensor():
    # подгатавливаем пины
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    # расчитываем расстояние пустого ящика
    red_d = sum([get_distance() for _ in range(3)]) / 3
    print(f'Референсное значение: {red_d}')

    try:
        while True:
            d = get_distance()
            print(d, end='\r')
            if abs(red_d - d) > red_d/2:
                m.receive_mail()
                bot.send_message(me, "У Вас новое письмо")
    except:
        GPIO.cleanup()


if __name__ == '__main__':
    Thread(target=run_sensor).start()
    Thread(target=bot.infinity_polling).start()
