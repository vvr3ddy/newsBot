#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

import os
import logging
import requests
import json
import simplejson
from pprint import pprint
from html import escape
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler, ConversationHandler, Filters, MessageHandler, Updater
from telegram import ParseMode, bot, chat, update
import telegram
from autologging import logged, traced



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


FIRST = range(1)
I_NEWS, NEWS, GUIDE, CAT = range(4)

@traced
@logged
def escape_html(message):
    return message.replace("&", "&amp;").replace("<", "&lt;")

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
@traced
@logged
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi 😊') 

@traced
@logged
def indiaNews(update, context):
    id = str(update.message.chat_id)
    news_api_key = "8a26f01fc57841feba29455a2acb0105"
    """Send a message when the command /gnews is issued."""
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
        update.message.reply_text("""News from Google Feed
            powered by : NewsApi""")
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
            if(image == None):
                image = 'https://bitsofco.de/content/images/2018/12/Screenshot-2018-12-16-at-21.06.29.png'

            # Finally spam the user with news 🌚
            #bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
            context.bot.send_photo(chat_id = id, photo = str(image), caption =
                                    f"\n<b>HeadLine :</b><i>{escape_html(title)}</i>"
                                    f"\n<b>Author   :</b><i>{escape_html(author)}</i>"
                                    f'\n<b>Source   :</b><a href ="{url_string}">Link</a>',
                                    parse_mode="HTML")  
    else :
        #bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
        context.bot.send_photo(chat_id = id, photo = str(image), caption =
                                    f"\n<b>The Bot has encountered some error.</b>"
                                    f"\n<b>What can you do ?</b>"
                                    f"\n<i>1. Retry the same command again.</i>"
                                    f"\n<i>2. Notify the creator about the issue.</i>",
                                    parse_mode="HTML")  

@traced
@logged
def world_news(update, context):
    """Send a message when the command /news is issued."""
    id = str(update.message.chat_id)
    news_api_key = "8a26f01fc57841feba29455a2acb0105"
    received_message = update.message.text
    splitMsg = received_message.split(" ", 2)
    if len(splitMsg) == 1:
        splitMsg.append('us')
        update.message.reply_text("Country not specified Using default country as US")
    
    country = str(splitMsg[1])

    #Set the URL for fetching NEWS
    url = "http://newsapi.org/v2/top-headlines?country={}&apiKey={}".format(str(country), news_api_key)
    #check the response of JSON
    response = requests.get(url)
    #Retrieve JSON DATA
    json_data = response.json()

    #We see that some news do not have any images, so the feed stops. Give this a temp fix
    error_image = str("https://cheapdigitalservices.com/wp-content/uploads/error-with-wordpress.png")
    if str(json_data['status']) == 'ok' :    
        update.message.reply_text("""Top 10 Headlines from {} powered by : NewsApi""".format(country))
        for count in range(10):
            # Get data from the JSON Response
            source = json_data['articles'][count]['source']['name']
            title = json_data['articles'][count]['title']
            newsUrl = json_data['articles'][count]['url']
            url_string = str(newsUrl)
            description = json_data['articles'][count]['description']
            image = json_data['articles'][count]['urlToImage']
            # If no author is assigned to the headline
            if(source == None):
                source = 'Not Announced'
            if(image == None):
                image = 'https://bitsofco.de/content/images/2018/12/Screenshot-2018-12-16-at-21.06.29.png'

            # Finally spam the user with news 🌚
            context.bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
            context.bot.send_photo(chat_id = id, photo = str(image), caption =
                                    f"\n<b>HeadLine  :</b><i>{escape_html(title)}</i>"
                                    f"\n<b>Source    :</b><i>{escape_html(source)}</i>"
                                    f'\n<b>Full News :</b><a href ="{url_string}">Link</a>',
                                    parse_mode="HTML")  
    else :
        context.bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
        context.bot.send_photo(chat_id = id, photo = str(image), caption =
                                    f"\n<b>The Bot has encountered some error.</b>"
                                    f"\n<b>What can you do ?</b>"
                                    f"\n<i>1. Retry the same command again.</i>"
                                    f"\n<i>2. Notify the creator about the issue.</i>",
                                    parse_mode="HTML")  
@traced
@logged
def categ(update, context):
    """Send a message when the command /news is issued."""
    id = str(update.message.chat_id)
    news_api_key = "8a26f01fc57841feba29455a2acb0105"
    received_message = update.message.text
    splitMsg = received_message.split(" ", 3)   
    if len(splitMsg) == 1:
        splitMsg.append('us')
        update.message.reply_text("Country not specified. Using default country as US")
        splitMsg.append('business')
        update.message.reply_text("Category not specified, using default category as business")
    
    country = str(splitMsg[1]).upper()
    category = str(splitMsg[2]).upper()

        
    url = "http://newsapi.org/v2/top-headlines?country={}&category={}&apiKey={}".format(str(country), category, news_api_key)
    response = requests.get(url)
    json_data = response.json()
    error_image = str("https://cheapdigitalservices.com/wp-content/uploads/error-with-wordpress.png")
    if str(json_data['status']) == 'ok' :    
        update.message.reply_text("""Top 10 Headlines from {} in {} section \n powered by : NewsApi""".format(country, category))
        for count in range(10):
            # Get data from the JSON Response
            source = json_data['articles'][count]['source']['name']
            title = json_data['articles'][count]['title']
            newsUrl = json_data['articles'][count]['url']
            url_string = str(newsUrl)
            description = json_data['articles'][count]['description']
            image = json_data['articles'][count]['urlToImage']
            # If no author is assigned to the headline
            if(source == None):
                source = 'Not Announced'
            if(image == None):
                image = 'https://bitsofco.de/content/images/2018/12/Screenshot-2018-12-16-at-21.06.29.png'

            # Finally spam the user with news 🌚
            context.bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
            context.bot.send_photo(chat_id = id, photo = str(image), caption =
                                    f"\n<b>HeadLine  :</b><i>{escape_html(title)}</i>"
                                    f"\n<b>Source    :</b><i>{escape_html(source)}</i>"
                                    f'\n<b>Full News :</b><a href ="{url_string}">Link</a>',
                                    parse_mode="HTML")  
    else :
        context.bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
        context.bot.send_photo(chat_id = id, photo = str(image), caption =
                                    f"\n<b>The Bot has encountered some error.</b>"
                                    f"\n<b>What can you do ?</b>"
                                    f"\n<i>1. Retry the same command again.</i>"
                                    f"\n<i>2. Notify the creator about the issue.</i>",
                                    parse_mode="HTML")  


@traced
@logged
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
    dp.add_handler(CommandHandler("inews", indiaNews))
    dp.add_handler(CommandHandler("news", world_news)) 
    dp.add_handler(CommandHandler("cat", categ))

    # Add ConversationHandler to dispatcher that will be used for handling
    # updates

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