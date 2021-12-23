import logging
import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter

from vse42 import wrapper

# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token = "5015591679:AAEn0naed6fNPHv2WVlAgXQQDUIUfzzj2I8")
dp = Dispatcher(bot)

# инициализируем соединение с БД
db = SQLighter('db.db')

# инициализируем парсер
sg = wrapper('lastkey.txt')

# команда приветствия
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Приветствую! Я являюсь телеграм ботом, созданным для рассылки самых свежих новостей, связанных"
                         " с городом Кемерово! Подпишись на меня, чтобы всегда быть в центре событий!")


# Команда активации подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if (not db.subscriber_exists(message.from_user.id)):
        # если юзера нет в базе, добавляем его
        db.add_subscriber(message.from_user.id)
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, True)

    await message.answer(
        "Вы успешно подписались на рассылку!\nЖдите, скоро выйдут новые обзоры и вы узнаете о них первыми =)")


# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if (not db.subscriber_exists(message.from_user.id)):
        # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
        db.add_subscriber(message.from_user.id, False)
        await message.answer("Вы итак не подписаны.")
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, False)
        await message.answer("Вы успешно отписались от рассылки.")

        #проверяем наличие новых новостей
async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        #now = datetime.utcnow()
        #await bot.send_message(801307098, f"{now}", disable_notification = True)
        new_events = sg.new_events()

        if(new_events):
            new_events.reverse()
            for ng in new_events:
                nfo = sg.event_info(ng)

                subscriptions = db.get_subscriptions()

                #отправка новости
                with open(sg.dowload_image(nfo['image']), 'rb') as photo:
                    for s in subscriptions:
                        await bot.send_photo(
                            s[1],
                            photo,
                            caption = nfo['title'] + "\n" + "Оценка: " + nfo['score'] + "\n" + nfo['excerpt'] + "\n\n" +
                                    nfo['link'],
                            disable_notification = True
                        )

                        sg.update_lastkey(nfo['id'])


if __name__  == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(30))
    executor.start_polling(dp, skip_updates=True)
