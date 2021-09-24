"""
Simple Bot to reply to Telegram messages taken from the python-telegram-bot examples.
"""

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

f = open("token.txt","r")
lines=f.readlines()
TOKEN = lines[0]
f.close()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    chat_id = update.message.chat_id
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    username = update.message.from_user.username
    #update.message.reply_text("Hello {}!".format(first_name))
    context.bot.send_message(chat_id, "Hello {}!".format(first_name))

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def welcome(update, context):
    """Send a welcome message."""
    chat_id = update.message.chat_id
    welcome_text = "R-Ladies is a worldwide organization to promote gender diversity in the R community. We are a part of R-Ladies Global, in Reading. \n \n Our main objective is to promote the programming R language by sharing knowledge; therefore, anyone interested in learning R is welcome, independently of knowledge level 🥰 \n \n Our target public is the gender minorities, so cis or trans women, trans men, and non-binary people and queer. \n \n We want to make this place a safe haven for learning, so feel free to ask questions and be aware that any form of harassment is not tolerable. \n \n Thank you! 💖" 
    for member in update.message.new_chat_members:
        new_member_name = member.first_name
    welcome_message = "Welcome, {}! \n \n {}".format(new_member_name, welcome_text)
    
    if len(update.message.new_chat_members) > 0 :
      context.bot.send_message(chat_id = chat_id, text = welcome_message) 
    

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()