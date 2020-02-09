from .bot import  bot


@bot.message_handler(commands=['start'])
def cmd_start(message):
    return bot.reply_to(message, 'Hello, I\'m bot!')
