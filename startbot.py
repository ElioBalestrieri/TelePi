#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 14:52:55 2022

@author: elio
"""

import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def clear_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    with open("DalaiMama_memory.txt", "w") as memfile:
        memfile.truncate()
    update.message.reply_text('\U0001F9F9')


def store_message(update: Update, context: CallbackContext) -> None:
    """Store messages in new lines of txt file."""
    
    with open('DalaiMama_memory.txt', 'a') as memfile:        
        memfile.write('\n' + update.message.text)
    
    update.message.reply_text('\U0001F44D')

def main() -> None:
    """Start the bot."""
    
    # read the token from the separate txt file
    with open('DalaiMama_token.txt', 'r') as tokenfile:        
        token = tokenfile.read()
        
        
    # Create the Updater and pass it your bot's token. in this case we specify here persistence
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("clear", clear_command))

    # store message sent on txt file
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, store_message))

    # Start the Bot
    updater.start_polling()


    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

