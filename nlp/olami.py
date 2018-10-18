import configparser
import json
import logging
import time
from hashlib import md5
from api.kkbox import KKBOX

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
            raise NliStatusError("NLI responded status != 'ok': {}".format(response_json['status']))
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
        data = self.app_secret + 'api=' + api + 'appkey=' + self.app_key + 'timestamp=' + \
               str(timestamp_ms) + self.app_secret
        return md5(data.encode('ascii')).hexdigest()

    def _gen_rq(self, text):
        obj = {'data_type': 'stt', 'data': {'input_type': self.input_type, 'text': text}}
        return json.dumps(obj)

    def intent_detection(self, nli_obj):
        def handle_selection_type(type):
            if type == 'news':
                return desc['result'] + '\n\n' + '\n'.join(
                    str(index + 1) + '. ' + el['title'] for index, el in enumerate(data))
            elif type == 'poem':
                return desc['result'] + '\n\n' + '\n'.join(
                    str(index + 1) + '. ' + el['poem_name'] + '，作者：' + el['author'] for index, el in enumerate(data))
            elif type == 'cooking':
                return desc['result'] + '\n\n' + '\n'.join(
                    str(index + 1) + '. ' + el['name'] for index, el in enumerate(data))
            else:
                return '對不起，你說的我還不懂，能換個說法嗎？'

        def handle_music_kkbox_type(semantic):
            music_type = semantic['modifier'][0].split('_')[2]
            slots = semantic['slots']
            kkbox = KKBOX()

            def get_slot_value_by_key(key):
                return next(filter(lambda el: el['name'] == key, slots))['value']

            key = 'keyword' if music_type == 'playlist' else (music_type + '_name')
            return kkbox.search(music_type, get_slot_value_by_key(key))

        type = nli_obj['type']
        desc = nli_obj['desc_obj']
        data = nli_obj.get('data_obj', [])

        if type == 'kkbox':
            id = data[0]['id']
            return ('https://widget.kkbox.com/v1/?type=song&id=' + id) if len(data) > 0 else desc['result']
        elif type == 'baike':
            return data[0]['description']
        elif type == 'joke':
            return data[0]['content']
        elif type == 'news':
            return data[0]['detail']
        elif type == 'cooking':
            return data[0]['content']
        elif type == 'selection':
            return handle_selection_type(desc['type'])
        elif type == 'ds':
            return desc['result'] + '\n請用 /help 指令看看我能怎麼幫助您'
        elif type == 'music_kkbox':
            return handle_music_kkbox_type(nli_obj['semantic'][0])
        else:
            return desc['result']
