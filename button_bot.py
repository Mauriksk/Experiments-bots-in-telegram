from config.config import *
import telebot
from telebot.types import ReplyKeyboardMarkup # This is to create buttons
from telebot.types import ForceReply # To quote a message
from telebot.types import ReplyKeyboardRemove # To remove buttons

bot = telebot.TeleBot(TELEGRAM_TOKEN)
users = {}

#
@bot.message_handler(commands=['start', 'help'])
def cmd_start(message):
    markup = ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Use the comman /replay", reply_markup=markup)

@bot.message_handler(commands=['replay'])
def replay_message(message):
    markup = ForceReply()
    msg = bot.send_message(message.chat.id, "How is your name?", reply_markup=markup)
    bot.register_next_step_handler(msg, ask_age)

def ask_age(message):
    users[message.chat.id] = {}
    users[message.chat.id]['name'] = message.text
    markup = ForceReply()
    msg = bot.send_message(message.chat.id, "How old are you ?", reply_markup=markup)
    bot.register_next_step_handler(msg, ask_sex)

def ask_sex(message):
    if not message.text.isdigit():
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "ERROR: Please respond a valid age. \n how old are you?")
        bot.register_next_step_handler(msg, ask_sex)
    else:
        users[message.chat.id]['age'] = int(message.text)
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
    else:
        users[message.chat.id]['sex'] = message.text
        text = 'Printed data:\n'
        text += f'<code>Name:</code> {users[message.chat.id]["name"]}\n'
        text += f'<code>Age :</code> {users[message.chat.id]["age"]}\n'
        text += f'<code>Sex :</code> {users[message.chat.id]["sex"]}\n'
        markup = ReplyKeyboardRemove()
        bot.send_message(message.chat.id, text, parse_mode='html', reply_markup=markup)
        print(users)
        #To delet dictionary
        del users[message.chat.id]


if __name__ == '__main__':
    print("STARTING BOT...")
    bot.infinity_polling()