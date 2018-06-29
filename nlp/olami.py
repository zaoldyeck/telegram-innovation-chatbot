import configparser
import json
import logging
import time
from hashlib import md5

import requests

config = configparser.ConfigParser()
config.read('config.ini')

logger = logging.getLogger(__name__)


class NliStatusError(Exception):
    """The NLI result status is not 'ok'"""


class Olami:
    URL = 'https://tw.olami.ai/cloudservice/api'

    def __init__(self, app_key=config['OLAMI']['APP_KEY'], app_secret=config['OLAMI']['APP_SECRET'], input_type=1):
        self.app_key = app_key
        self.app_secret = app_secret
        self.input_type = input_type

    def nli(self, text, cusid=None):
        response = requests.post(self.URL, params=self._gen_parameters('nli', text, cusid))
        response.raise_for_status()
        response_json = response.json()
        if response_json['status'] != 'ok':
            raise NliStatusError(
                "NLI responded status != 'ok': {}".format(response_json['status']))
        else:
            nli_obj = response_json['data']['nli'][0]
            return self.intent_detection(nli_obj)

    def _gen_parameters(self, api, text, cusid):
        timestamp_ms = (int(time.time() * 1000))
        params = {'appkey': self.app_key,
                  'api': api,
                  'timestamp': timestamp_ms,
                  'sign': self._gen_sign(api, timestamp_ms),
                  'rq': self._gen_rq(text)}
        if cusid is not None:
            params.update(cusid=cusid)
        return params

    def _gen_sign(self, api, timestamp_ms):
        data = self.app_secret + 'api=' + api + 'appkey=' + self.app_key + \
               'timestamp=' + str(timestamp_ms) + self.app_secret
        return md5(data.encode('ascii')).hexdigest()

    def _gen_rq(self, text):
        obj = {'data_type': 'stt', 'data': {'input_type': self.input_type, 'text': text}}
        return json.dumps(obj)

    def intent_detection(self, nli_obj):
        def handle_selection_type(type):
            reply = {
                'news': lambda: desc['result'] + '\n\n' + '\n'.join(
                    str(index + 1) + '. ' + el['title'] for index, el in enumerate(data)),
                'poem': lambda: desc['result'] + '\n\n' + '\n'.join(
                    str(index + 1) + '. ' + el['poem_name'] + '，作者：' + el['author'] for index, el in
                    enumerate(data)),
                'cooking': lambda: desc['result'] + '\n\n' + '\n'.join(
                    str(index + 1) + '. ' + el['name'] for index, el in
                    enumerate(data))
            }.get(type, lambda: '對不起，你說的我還不懂，能換個說法嗎？')()
            return reply

        type = nli_obj['type']
        desc = nli_obj['desc_obj']
        data = nli_obj.get('data_obj', [])

        reply = {
            'kkbox': lambda: data[0]['url'] if len(data) > 0 else desc['result'],
            'baike': lambda: data[0]['description'],
            'news': lambda: data[0]['detail'],
            'joke': lambda: data[0]['content'],
            'cooking': lambda: data[0]['content'],
            'selection': lambda: handle_selection_type(desc['type']),
            'ds': lambda: desc['result'] + '\n請用 /help 指令看看我能怎麼幫助您'
        }.get(type, lambda: desc['result'])()

        return reply