import config
import logging

from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)


async def echo(message: types.Message):
    await message.answer(message.text)

if __name__  == '__main__':
    executor.start_polling(dp, skip_updates=True)