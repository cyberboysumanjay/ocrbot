try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
from telegram.ext.dispatcher import run_async
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from telegram import Update, Bot, ParseMode
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! \n\nWelcome to Optical Character Recognizer Bot. \n\nJust send a clear image to the bot and it will recognize the text in the image and send it as a message!\nTo get my contact details tap /contact \nTo get donation details tap /donate\n')

def donate(bot, update):
    """Send a message when the command /donate is issued."""
    bot.send_message(chat_id=201566591,text=str(update.message.chat_id)+" "+str(update.message.from_user.name)+' clicked /donate ')
    update.message.reply_text("To donate you can send any amount you wish to me using the following *Payment Options*:\n\nUPI - `sumanjay@ybl` (Long press to copy)\n[Paytm](https://p-y.tm/SnE-jE9)\n[PayPal](https://paypal.me/sumanjay/10USD)\n[Debit/Credit/Netbanking/Other Wallets](https://www.instamojo.com/@sumanjay)\n\nAfter making payment don't forget to send a screenshot of the Transaction to @cyberboysumanjay", parse_mode=ParseMode.MARKDOWN)

def contact(bot, update):
    """Send a message when the command /contact is issued."""
    update.message.reply_text("Heya! You can find me on \n[Telegram](https://telegram.me/cyberboysumanjay)\n[Facebook](https://facebook.com/imsumanjay)\n[Instagram](https://instagram.com/sumanjay_)\n[Twitter](https://twitter.com/cyberboysj)\n[LinkedIn](https://www.linkedin.com/in/sumanjay-9816a4128)", parse_mode=ParseMode.MARKDOWN)

def search(bot, update):
    """Send reply of user's message."""
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    photo_file.download('testing.jpg')
    try:
        output=pytesseract.image_to_string(Image.open('testing.jpg'))
        update.message.reply_text('`'+str(output)+'`',parse_mode=ParseMode.MARKDOWN,reply_to_message_id=update.message.message_id)
    except Exception as e:
        update.message.reply_text(e)
        try:
            os.remove('testing.jpg')
        except Exception:
            pass

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    """Start the bot."""
    ocr_bot_token=os.environ.get("BOT_TOKEN", "")
    updater = Updater(ocr_bot_token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("donate", donate))
    dp.add_handler(CommandHandler("contact", contact))
    dp.add_handler(MessageHandler(Filters.photo, search))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
