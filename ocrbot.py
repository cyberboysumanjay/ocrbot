#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]

import logging
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import constants
import os

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(constants.welcome_text)


def donate(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(constants.donate_text, parse_mode=ParseMode.MARKDOWN)


def read_image(update: Update, context: CallbackContext) -> None:
    """Send reply of user's message."""
    chat_id = update.message.chat_id
    try:
        photo_file = update.message.photo[-1].get_file()
        img_name = str(chat_id)+'.jpg'
        photo_file.download(img_name)
        output=pytesseract.image_to_string(Image.open(img_name))
        if output:
            update.message.reply_text('`'+str(output)+'`\n\nImage to Text Generated using @imagereaderbot', parse_mode=ParseMode.MARKDOWN, reply_to_message_id = update.message.message_id)
        else:
            update.message.reply_text(constants.no_text_found)
    except Exception as e:
        update.message.reply_text("Error Occured: `"+str(e)+"`")
    finally:
        try:
            os.remove(img_name)
        except Exception:
            pass

def reply_to_text_message(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(constants.reply_to_text_message)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    ocr_bot_token=os.environ.get("BOT_TOKEN", "")
    updater = Updater(ocr_bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("donate", donate))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_to_text_message))
    dispatcher.add_handler(MessageHandler(Filters.photo, read_image))
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()