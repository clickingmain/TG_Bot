import telebot

bot = telebot.TeleBot('2118835094:AAF91vOnYY2kO613fjDDmXnyoX0hzPh9lvE')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello World!")

bot.polling(none_stop=True)