from config.config import *
import telebot
#Inline Buttons 
from telebot.types import InlineKeyboardMarkup # to create keyboard buttons
from telebot.types import InlineKeyboardButton # to define buttons
import requests
from bs4 import BeautifulSoup

N_RES_PAG = 15
MAX_WIDTH = 8
DIR = {"Busquedas": "./busquedas/"}
for key in DIR:
    try:
        os.mddir(key)
    except:
        pass


bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['buttons'])
def cmd_buttons(message):
    markup = InlineKeyboardMarkup(row_width=1) # number of buttos, default value is 3
    b1  = InlineKeyboardButton('Linkedin', url='https://www.linkedin.com/in/mauricio-torres-frontend/')
    b2  = InlineKeyboardButton('Follow my instagram', url='https://www.instagram.com/mauritor664/')
    b_close = InlineKeyboardButton("Close", callback_data="close")
    markup.add(b1, b2, b_close)
    bot.send_message(message.chat.id, "Check my social medias!!", reply_markup=markup)

@bot.callback_query_handler(func=lambda x: True)
def response_inline_button(call):
    chat_id = call.from_user.id
    message_id = call.message.id
    if call.data == 'close':
        bot.delete_message(chat_id, message_id)
        

@bot.message_handler(commands=['search'])
def cmd_search(message):
    #With join i create an array with the words separated with + ( in this case )
    # and with split y cut the array into a string but just with the 1 position to last
    text_search = "+".join(message.text.split()[1:])
    if not text_search:
        text = 'You shoud put a text.\n'
        text+= 'Example:\n'
        text+= f'<code>{"PornHub teens"}'
        bot.send_message(message.chat.id, text, parse_mode='html')
        return 1
    else:
        url = f'https://www.google.es/search?q{text_search}&num=100'
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
        headers = {"user-agent": user_agent}
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            print(f'ERROR searching: {res.status_code} {res.reason}')
            bot.send_message(message.chat.id, "An error has occurred try later")
            return 1
        else:
            soup = BeautifulSoup(res.text, "html.parser")
            elements = soup.find_all("div", class_="g")
            lists = []
            for element in elements:
                try:
                    title = element.find("h3").text
                    url = element.find("a").attrs.get("href")
                    if not url.startswith("http"):
                        url = "https://google.es" + url
                    if [title, url] in lists:
                        continue
                    lists.append([title, url])
                except:
                    continue

def show_page(list, chat_id, message_id_:None):
    markup = InlineKeyboardMarkup()

if __name__ == '__main__':
    print('Starting...')
    bot.infinity_polling()
