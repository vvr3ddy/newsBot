#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import os
import logging
import requests
import json
import simplejson
from pprint import pprint
from html import escape

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import bot, chat
import telegram




# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def escape_html(message):
    return message.replace("&", "&amp;").replace("<", "&lt;")

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi 😊')

def gNews(update, context):
    """Send a message when the command /gnews is issued."""

    id = str(update.message.chat_id)
    news_api_key = os.environ.get("news_api_key","")
    url = "http://newsapi.org/v2/top-headlines?sources=google-news-in&apiKey={}".format(news_api_key)
    response = requests.get(url)
    json_data = response.json()

    received_message = update.message.text
    splitMsg = received_message.split(" ", 1)
    error_image = str("https://cheapdigitalservices.com/wp-content/uploads/error-with-wordpress.png")
    if len(splitMsg) == 1:
        splitMsg.append('0')
    
    value = int(splitMsg[1])
    if value > 10  :
        value = 10
    elif value <= 0 :
        value = 10

    if str(json_data['status']) == 'ok' :    
        update.message.reply_text('News from Google Feed\
            powered by : NewsApi')
        for count in range(value):
            # Get data from the JSON Response
            author = json_data['articles'][count]['author']
            title = json_data['articles'][count]['title']
            newsUrl = json_data['articles'][count]['url']
            url_string = str(newsUrl)
            description = json_data['articles'][count]['description']
            image = json_data['articles'][count]['urlToImage']
            # If no author is assigned to the headline
            if(author == None):
                author = 'Not Announced'

            # Finally spam the user with news 🌚
            bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
            context.bot.send_photo(chat_id = id, photo = str(image), caption =
                                    f"\n<b>HeadLine :</b><i>{escape_html(title)}</i>"
                                    f"\n<b>Author   :</b><i>{escape_html(author)}</i>"
                                    f'\n<b>Source   :</b><a href ="{url_string}">Link</a>',
                                    parse_mode="HTML")  
    else :
        bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
        context.bot.send_photo(chat_id = id, photo = str(image), caption =
                                    f"\n<b>The Bot has encountered some error.</b>"
                                    f"\n<b>What can you do ?</b>"
                                    f"\n<i>1. Retry the same command again.</i>"
                                    f"\n<i>2. Notify the creator about the issue.</i>",
                                    parse_mode="HTML")  



def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    
def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    bot_token = os.environ.get("BOT_TOKEN","")
    updater = Updater(bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("gnews", gNews))
    #dp.add.handler(CommandHandler("tnews", tNews)) --> todo
    

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