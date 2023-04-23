from config.config import *
import telebot
from telebot.types import ReplyKeyboardMarkup # This is to create buttons
from telebot.types import ForceReply # To quote a message

bot = telebot.TeleBot(TELEGRAM_TOKEN)

#
@bot.message_handler(commands=['start', 'help'])
def cmd_start(message):
    bot.send_message(message.chat.id, "How is your name?")

@bot.message_handler(commands=['replay'])
def replay_message(message):
    markup = ForceReply()
    msg = bot.send_message(message.chat.id, "How is your name?", reply_markup=markup)
    bot.register_next_step_handler(msg, ask_age)

def ask_age(message):
    name = message.text
    markup = ForceReply()
    msg = bot.send_message(message.chat.id, "How old are you ?" + name, reply_markup=markup)
    bot.register_next_step_handler(msg, ask_sex)

def ask_sex(message):
    if not message.text.isdigit():
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "ERROR: Please respond a valid age. \n how old are you?")
        bot.register_next_step_handler(msg, ask_sex)
    else:
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True,
            input_field_placeholder='Click here',
            resize_keyboard=True
            )
        markup.add("Man", "Woman")#buttons
        msg = bot.send_message(message.chat.id, "which is your sex?", reply_markup=markup)
        bot.register_next_step_handler(msg, save_data)

def save_data(message):
    if message.text != "Man" and message.text != "woman":
        msg = bot.send_message(message.chat.id, "ERROR: Sex not valid. \n which is your sex?")
        bot.register_next_step_handler(msg, save_data)


if __name__ == '__main__':
    print("STARTING BOT...")
    bot.infinity_polling()