from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters,
                CallbackContext)

import ssl



from pytube import YouTube
from telebot import TeleBot
import telebot
from telebot import types
import configparser
import logging
import redis
from ChatGPT_HKBU import HKBU_ChatGPT

ssl._create_default_https_context = ssl._create_stdlib_context
   
global bot
bot = telebot.TeleBot('6972742316:AAGfE5-aYPEoQN4SF1J5mgaqgm5oi9AQl0Q')
   
global redis1
def main():
    # Load your token and create an Updater for your Bot
    config = configparser.ConfigParser()
    config.read('config.ini')
    global bot
    bot = telebot.TeleBot(config['TELEGRAM']['ACCESS_TOKEN'])
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher
    global redis1
    redis1 = redis.Redis(host=(config['REDIS']['HOST']),
                password=(config['REDIS']['PASSWORD']),
                port=(config['REDIS']['REDISPORT']))
    # You can set this logging module, so you will know when
    # and why things do not work as expected Meanwhile, update your config.ini as:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
    # register a dispatcher to handle message: here we register an echo dispatcher
    #echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    #dispatcher.add_handler(echo_handler)

    # dispatcher for chatgpt
    global chatgpt
    chatgpt = HKBU_ChatGPT(config)
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command),equiped_chatgpt)
    dispatcher.add_handler(chatgpt_handler)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("hello", hello))
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CallbackQueryHandler(message_handler))
    # To start the bot:
    updater.start_polling()
    updater.idle()

def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')
def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        global redis1
        logging.info(context.args[0])
        msg = context.args[0]   # /add keyword <-- this should store the keyword
        redis1.incr(msg)
        update.message.reply_text('You have said ' + msg +  ' for ' +
                        redis1.get(msg).decode('UTF-8') + ' times.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')
def hello(update: Update, context: CallbackContext) -> None: 
    """Send a message when the command /hello is issued.""" 
    try:
        logging.info(context.args[0])
        msg = context.args[0] # /hello keyword <-- this should store the keyword
        update.message.reply_text('Good day, ' + msg + ' ! ' )
    except (IndexError, ValueError): 
         update.message.reply_text('Usage: /hello <keyword>')
def start_command(update: Update, context: CallbackContext) -> None: 
    """Send a message when the command /start is issued.""" 
    try:
        global bot
        #markup = types.InlineKeyboardMarkup(row_width=1)
        #iron = types.InlineKeyboardButton('1 kilo of iron', callback_data= 'answer_iron')
        #cotton = types.InlineKeyboardButton('1 kilo of cotton', callback_data= 'answer_cotton')
        #same = types.InlineKeyboardButton( 'same weight', callback_data= 'answer_same')
        #no_answer = types.InlineKeyboardButton('no correct answer', callback_data= 'no_answer')
        #markup.add(iron, cotton, same, no_answer)
        #bot.send_message(update.effective_chat.id,' Welcome to CC chatbot? \n Please select the below function', reply_markup=markup)
	# 建立 InlineKeyboard
        keyboard_1 = InlineKeyboardMarkup([
            [
              InlineKeyboardButton("A", callback_data="a")
             ], [
                 InlineKeyboardButton("B", callback_data="b")
             ]
         ])
        update.message.reply_text(
        text=' Welcome to CC chatbot? \n Please select the below function', reply_markup=keyboard_1)

    except (IndexError, ValueError): 
        update.message.reply_text('Usage: /hello <keyword>')

def message_handler(update: Update, context: CallbackContext):
    bot.send_message (update.effective_chat.id, update.callback_query.data+'I Congratulations! You are the winner1!')
    yt = YouTube("https://www.youtube.com/watch?v=lOUsz0ggDsk")
    video = yt.streams.filter(file_extension="mp4").get_by_resolution("360p").download("./tmp")
    
    bot.send_video(update.effective_chat.id, open(video, 'rb'))
    

@bot.callback_query_handler(func=lambda call:True)
def answer (callback):
        if callback.message:
             if callback.data == 'answer_iron':
                 bot.send_message (callback.message.chat.id, 'I Congratulations! You are the winner1!')
             elif callback.data == 'answer_cotton':
                 bot.send_message (callback.message.chat.id, 'I Congratulations! You are the winner2!')
             elif callback.data == 'answer_same':
                 bot.send_message (callback.message.chat.id, 'I Congratulations! You are the winner3!')
             else:
                 bot.send_message (callback.message.chat.id,'I Congratulations! You are the winner4!')
def equiped_chatgpt(update, context):
    global chatgpt
    reply_message = chatgpt.submit(update.message.text)
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)
if __name__ == '__main__':
    main()
 