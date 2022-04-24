# Умный почтовый ящик

## Зависимости

```bash
sudo apt-get install -y i2c-tools python3-smbus # взаимодействие через I2C
pip install pyTelegramBotAPI # библиотека для Telegram бота
```
## Запуск

```bash
export CHAT_ID=...       # айди Телеграм аккаунта
export BOT_TOKEN=...    # токен Телеграм бота

python main.py
```


## Описание

+ `lcd.py`

  Вывод данных на LCD-экран через шину I2C

+ `mailbox.py`

   Хранит состояние почтового ящика: кол-во писем, история их попадания. Также обновляет счетчик на экране

+ `main.py`

   Запускает два треда:

    1. Сервер для Telegram бота
    1. Главный поток, ответственный за измерение расстояния с сенсора. Как только оно уменьшается больше чем в два раза, значит в ящик закинули письмо

    Функция `get_distance` использует следующую формулу:
    ![Формула1](https://cdn.shopify.com/s/files/1/0176/3274/files/hc-sr04-eq3_1024x1024.png?v=1561459504)
    ![Формула2](https://cdn.shopify.com/s/files/1/0176/3274/files/hc-sr04-eq4_1024x1024.png?v=1561459539)