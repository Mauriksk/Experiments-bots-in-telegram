from config import *
import telebot
import threading

# Instance of telegram bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

#Response to command /start
@bot.message_handler(commands=['start', 'help', 'ayuda'])
def cmd_start(message):
    welcome_message = "Hi what's up buddy?" + '\n'
    welcome_message += "Here a list of commans" + '\n'
    welcome_message += "/CV" + '\n'
    welcome_message += "/Linkeding" + '\n'
    bot.reply_to(message, )

@bot.message_handler(commands=['CV'])
def cmd_start(message):
    archivo = open("C:/Users/mauri/Downloads/Mauricio+Torres+Frontend-Developer.pdf", "rb")
    bot.send_document(message.chat.id, archivo, caption="This is my CV!!")

@bot.message_handler(commands=['Linkedin'])
def cmd_start(message):
    bot.send_chat_action(message.chat.id, "typing")
    linkedin_ref = '<b>To see my profile just check my </b>'
    linkedin_ref+= '<a href="https://www.linkedin.com/in/mauricio-torres-frontend/">Linkedin</a>'
    bot.send_message(message.chat.id, linkedin_ref, parse_mode="html", disable_web_page_preview = False)

# Replay to messages that are not commands
@bot.message_handler(content_types=['text'])
def bot_message_text(message):
    linkedin_ref = '<b>To see my profile just check my </b>'
    linkedin_ref+= '<a href="https://www.linkedin.com/in/mauricio-torres-frontend/">Linkedin</a>'
    if message.text.startswith("/"):
        bot.send_message(message.chat.id, "Send a valid command")
    else:
        bot.send_message(message.chat.id, linkedin_ref, parse_mode="html", disable_web_page_preview = False)

def recive_messages():
    bot.infinity_polling()

if __name__ == '__main__':
    print('Starting bot')
    thread_bot = threading.Thread(name="thread_bot", target=recive_messages)
    thread_bot.start()
    print('End')
    

