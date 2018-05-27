import configparser
import sys

import telegram
from nlp.olami import Olami
from flask import Flask, request

config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)

bot = telegram.Bot(token=(config['TELEGRAM']['ACCESS_TOKEN']))


def _set_webhook():
    status = bot.set_webhook(config['TELEGRAM']['WEBHOOK_URL'])
    if not status:
        print('Webhook setup failed')
        sys.exit(1)


@app.route('/hook', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        text = update.message.text
        reply = Olami().nli(text=text)
        update.message.reply_text(reply)
    return 'ok'


if __name__ == "__main__":
    _set_webhook()
    app.run()
