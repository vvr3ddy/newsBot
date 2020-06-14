#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple inline keyboard bot with multiple CallbackQueryHandlers.

This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined as callback query handler. Then, those functions are
passed to the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot that uses inline keyboard that has multiple CallbackQueryHandlers arranged in a
ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line to stop the bot.
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
import logging
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def escape_html(message):
    return message.replace("&", "&amp;").replace("<", "&lt;")


# Stages
FIRST = range(1)
# Callback data


I_NEWS, NEWS, GUIDE, CAT = range(4)


#HELP COMMAND TO START THE HELP
def help(update, context):
    """Send message on `/help`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [InlineKeyboardButton("Main Menu", callback_data=str(GUIDE))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text(
        f"🚨<b> !!!Bleep Bloop!!! </b>🚨"
        f"\nYou have Requested assistance."
        f"\nAnd we are happy to help ✌️",
        reply_markup=reply_markup, parse_mode="HTML"
    )
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST

#FIRST BUTTON
def guide(update, context):
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    #PROVIDE USER TWO BUTTONS TO SELECT
    keyboard = [
        [InlineKeyboardButton("/news", callback_data=str(NEWS)),
         InlineKeyboardButton("/cat", callback_data=str(CAT)),
         InlineKeyboardButton("/i_news", callback_data=str(I_NEWS))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=
        f"\n<b>What is this BOT ?</b>"
        f"\nThis BOT Provides you with latest News updates."
        f"\nThe News stream is updated every 15 minutes once."
        f"\n\n<b>Functionality of the BOT</b>"
        f"\nThis bot has currently three functional commands."
        f"\nSupport for each of the commands is provided clearly."
        f"\nTap on the corresponding button to know more.",
        reply_markup=reply_markup, parse_mode="HTML"
    )
    return FIRST  


#SECOND BUTTON
def i_news(update, context):
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    #PROVIDE USER TWO BUTTONS TO SELECT
    keyboard = [
        [InlineKeyboardButton("/news", callback_data=str(NEWS)),
         InlineKeyboardButton("/cat", callback_data=str(CAT)),
         InlineKeyboardButton("Main Menu", callback_data=str(GUIDE))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=
        f"\nUsage guide for <b>inews</b>"
        f"\n================================================="
        f"\n<b>inews</b> command is specific to fetch news"
        f"\nrelated to India. To fetch news just type /inews.",
        reply_markup=reply_markup, parse_mode="HTML"
    )
    return FIRST

#THIRD BUTTON
def news(update, context):
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    #PROVIDE USER TWO BUTTONS TO SELECT
    keyboard = [
        [InlineKeyboardButton("/inews", callback_data=str(I_NEWS)),
         InlineKeyboardButton("/cat", callback_data=str(CAT)),
         InlineKeyboardButton("Main Menu", callback_data=str(GUIDE))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=
        f"\nUsage guide for <b>news</b> "
        f"\n===================================================="
        f"\nThis command fetches news from a list of countries."
        f"\nThe list of countries supported countries is attached"
        f"\nbelow for reference."
        f"\n\n<b>Usage</b>    : /news {escape_html('<country code> <count>')}"
        f"\n\n<b>Example</b>  : '/news AU 10' yields top 10 headlines from Australia."
        f"\n\n\n<b>Count varies from 1 to 10. By default it is set to 10.</b>"
        f"\n\n<b>If country is not specified, the default goes to US.</b>",
        reply_markup=reply_markup, parse_mode="HTML"
    )
    return FIRST


def cat_help(update, context):
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    #PROVIDE USER TWO BUTTONS TO SELECT
    keyboard = [
        [InlineKeyboardButton("/news", callback_data=str(NEWS)),
         InlineKeyboardButton("/inews", callback_data=str(I_NEWS)),
         InlineKeyboardButton("Main Menu", callback_data=str(GUIDE))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=
        f"\nUsage guide for <b>cat</b>"
        f"\n======================================================"
        f"\nThis command fetches news from a list of countries with a preference over category of news."
        f"\nThe list of countries supported categories is attached below for reference."
        f"\n\n<b>Usage</b> : /cat {escape_html('<country code> <category>')}"
        f"\n\n<b>Ex</b> : '/cat AU Sports' yields top 10 headlines from Australia related to sports."
        f"\n\n\n<b>Default category</b> : Business"
        f"\n<b>Default country</b>  : US",
        reply_markup=reply_markup, parse_down="HTML"
    )
    return FIRST

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(os.environ.get("BOT_TOKEN",""), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'



    #CODE MODIFIED BY VVR
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('help', help)],
        states={
            FIRST: [CallbackQueryHandler(i_news, pattern='^' + str(I_NEWS) + '$'), #NOTE THE  I_NEWS Word at the beginning of the code
                    CallbackQueryHandler(news, pattern='^' + str(NEWS) + '$'),
                    CallbackQueryHandler(cat_help, pattern='^' + str(CAT) + '$'),
                    CallbackQueryHandler(guide, pattern='^' + str(GUIDE) + '$')]
        },
        fallbacks=[CommandHandler('help', help)]
    )

    #END OF CODE BY VVR

    # Add ConversationHandler to dispatcher that will be used for handling
    # updates
    dp.add_handler(conv_handler)

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