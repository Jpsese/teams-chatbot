import json
import requests


def post_request(func):
    def wrapper(*args, **kw):
        print('@Teams: '+func.__name__)
        requestInfo = func(*args, **kw)

        messageUrl = requestInfo['url'] + requestInfo['convoId']+'/activities/'
        result = requests.post(
            messageUrl,
            json=requestInfo['payload']
        )
        if result:
            try:
                return result.json()
            except:
                pass
        return {}
    return wrapper


class TeamsOutputBuilder:

    def __init__(self, payload):
        self.payload = payload
        self.URL = payload['serviceUrl'] + '/v3/conversations/'
        self.convoId = self.payload['conversation']['id']

    def _new_msg_payload(self):
        return{
            'type': 'message',
            'from': {
                'id': self.payload['recipient']['id'],
                'name': self.payload['recipient']['name']
            },
            'recipient': {
                'id': self.payload['from']['id']
            }
        }

    def _new_post_payload(self, payload):
        return {
            'url': self.URL,
            'convoId': self.convoId,
            'payload': payload
        }

    @post_request
    def typing(self):
        msgPayload = self._new_msg_payload()
        msgPayload['type'] = 'typing'
        return self._new_post_payload(msgPayload)

    @post_request
    def text_message(self, message):
        msgPayload = self._new_msg_payload()
        msgPayload['text'] = message
        return self._new_post_payload(msgPayload)

    @post_request
    def hero_card(self, title, cardMessage, message, menus, images=None,
                  subTitle=None, tapAction=None):
        msgPayload = self._new_msg_payload()
        if message:
            msgPayload['text'] = message
        msgPayload['inputHint'] = 'acceptingInput'
        msgPayload['attachmentLayout'] = 'list'

        if images:
            msgPayload['attachments'] = [{
                'contentType': 'application/vnd.microsoft.card.hero',
                'content': {
                    'title': title,
                    'subtitle': subTitle,
                    'text': cardMessage,
                    'images': images,
                    'buttons': menus,
                    'tap': tapAction
                }
            }]
        else:
            msgPayload['attachments'] = [{
                'contentType': 'application/vnd.microsoft.card.hero',
                'content': {
                    'title': title,
                    'subtitle': subTitle,
                    'text': cardMessage,
                    'buttons': menus,
                    'tap': tapAction
                }
            }]
        return self._new_post_payload(msgPayload)
