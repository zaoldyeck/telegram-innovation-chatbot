# Telegram Innovation Chatbot
A Telegram Bot powered by [OLAMI](https://tw.olami.ai/) can understand Chinese. Has the ability to search music data due to integrating [KKBOX Open API](https://developer.kkbox.com/).
<br/>
Try it out via https://t.me/innovation_chatbot

## Articles
There are three articles talk about how to build this project.
<br/>
[（一）一步步打造 Telegram Bot](https://medium.com/@zaoldyeck9970/%E6%89%8B%E6%8A%8A%E6%89%8B%E6%95%99%E4%BD%A0%E6%80%8E%E9%BA%BC%E6%89%93%E9%80%A0-telegram-bot-a7b539c3402a)
<br/>
[（二）為 Chatbot 增加 NLP 功能](https://medium.com/@zaoldyeck9970/%E5%88%A9%E7%94%A8-olami-open-api-%E7%82%BA-chatbot-%E5%A2%9E%E5%8A%A0-nlp-%E5%8A%9F%E8%83%BD-e6b37940913d)
<br/>
[（三）為 Chatbot 添加新技能](https://medium.com/@zaoldyeck9970/add-custom-skill-into-chatbot-cef9bfeeef52)

## Development
1. Ensure you have registered these accounts.
    1. [Telegram](https://telegram.org/)
    2. [OLAMI](https://tw.olami.ai/)
    3. [KKBOX Developers](https://developer.kkbox.com/)
    4. [Heroku](https://www.heroku.com/)
2. Create bot, get `access token`
    1. Talk to [BotFather](https://telegram.me/botfather)
    2. Type `/newbot`
3. Create [OLAMI](https://tw.olami.ai/) App, get `key` and `secret`
    1. Log in [OLAMI](https://tw.olami.ai/) admin console
    2. 建立新應用 => fill information => 提交
    3. 變更設定 => 對話系統模組 => check all => 儲存設定
    4. Copy `App key` and `App Secret`
4. Create [KKBOX Developers](https://developer.kkbox.com/) App, get `id` and `secret`
    1. Log in [KKBOX Developers](https://developer.kkbox.com/)
    2. My Apps => Create new app => fill information => submit
    3. Copy `ID` and `Secret`
5. Clone this project, edit config.ini
    1. `$ git clone https://github.com/zaoldyeck/telegram-innovation-chatbot.git`
    2. Edit config.ini, fill in Telegram Bot `ACCESS_TOKEN`, OLAMI `APP_KEY` and `APP_SECRET`, KKBOX `ID` and `SECRET`
6. Deploy program to [Heroku](https://www.heroku.com/)
    1. Log in [Heroku](https://www.heroku.com/) account
    2. New => create new app => fill information => Create app
    3. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
    4. In local terminal console
    ```
    $ cd telegram-innovation-chatbot
    $ git commit -m "Edit config.ini"
    $ heroku login
    $ heroku git:remote -a {your_heroku_app_name}
    $ git push heroku master
    ```
7. Setting chatbot's webhook
    1. Get Heroku App url from App "Settings" page or "Open app". It should be `https://{$your_heroku_app_name}.herokuapp.com/`, then webhook url is `https://{$your_heroku_app_name}.herokuapp.com/hook`
    2. Open browser and enter `https://api.telegram.org/bot{$telegram_access_token}/setWebhook?url={$webhook_url}`

## License
```
MIT License

Copyright (c) 2018 zaoldyeck

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```
