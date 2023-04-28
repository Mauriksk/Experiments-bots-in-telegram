from config.config import *
import telebot
from telebot.types import ReplyKeyboardMarkup # This is to create buttons
from telebot.types import ReplyKeyboardRemove # To remove buttons
from random import randint

bot = telebot.TeleBot(TELEGRAM_TOKEN)
users = {}

@bot.message_handler(commands=['start', 'help'])
def cmd_start(message):
    buttons = ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Use the comman /play", reply_markup=buttons)

@bot.message_handler(commands=['play'])
def cmd_play(message):
    number = randint(1,10)
    cid = message.chat.id
    users[cid] = number
    buttons = ReplyKeyboardMarkup(input_field_placeholder='press the button')
    buttons.add('1','2','3','4','5','6','7','8','9','10')
    msg = bot.send_message(message.chat.id, 'Guess the number', reply_markup=buttons)
    bot.register_next_step_handler(msg, check_number)

def check_number(message):
    cid = message.chat.id 