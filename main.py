import configparser
import logging

import telegram
from flask import Flask, request
from telegram import ReplyKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

from nlp.olami import Olami

# Load data from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initial Flask app
app = Flask(__name__)

# Initial bot by Telegram access token
bot = telegram.Bot(token=(config['TELEGRAM']['ACCESS_TOKEN']))

welcome_message = 'Hello~ 本 Bot 是用 http://bit.ly/2KxJF1F 開源程式碼所完成\n\n' \
                  '您可以問我\n' \
                  '天氣，例如：「台北天氣如何」\n' \
                  '百科，例如：「川普是誰」\n' \
                  '新聞，例如：「今日新聞」\n' \
                  '音樂，例如：「我想聽周杰倫的等你下課」\n' \
                  '日曆，例如：「現在時間」\n' \
                  '詩詞，例如：「我想聽水調歌頭這首詩」\n' \
                  '笑話，例如：「講個笑話」\n' \
                  '故事，例如：「說個故事」\n' \
                  '股票，例如：「台積電的股價」\n' \
                  '食譜，例如：「蛋炒飯怎麼做」\n' \
                  '聊天，例如：「你好嗎」'
reply_keyboard_markup = ReplyKeyboardMarkup([['播放陳奕迅的歌'],
                                             ['播放Cmon in~專輯的歌'],
                                             ['播放誰來剪月光'],
                                             ['播放金曲獎類型的歌']])


@app.route('/hook', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return 'ok'


def start_handler(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text(welcome_message, reply_markup=reply_keyboard_markup)


def help_handler(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text(welcome_message, reply_markup=reply_keyboard_markup)


def reply_handler(bot, update):
    """Reply message."""
    text = update.message.text
    user_id = update.message.from_user.id
    reply = Olami().nli(text, user_id)
    update.message.reply_text(reply)


def error_handler(bot, update, error):
    """Log Errors caused by Updates."""
    logger.error('Update "%s" caused error "%s"', update, error)
    update.message.reply_text('對不起唷~ 我需要多一點時間來處理 Q_Q')


# New a dispatcher for bot
dispatcher = Dispatcher(bot, None)

# Add handlers for handling message, there are many kinds of message. For this handler, it particular handle text
# message.
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))
dispatcher.add_handler(CommandHandler('start', start_handler))
dispatcher.add_handler(CommandHandler('help', help_handler))
dispatcher.add_error_handler(error_handler)

if __name__ == "__main__":
    # Running server
    app.run(debug=True)
