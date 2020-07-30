import json

from engine.e2e.builder import OutputBuilder
from engine.e2e.router import StateRouter

def profile_builder(convoId, userId):
    return {
        'id': userId,
        'convoId': convoId
    }

def handler(event, context):
    event_body = json.loads(event['body'])

    userObject = {
        'id': event_body['from']['id'],
        'convoId': event_body['conversation']['id'],
        'serviceUrl': event_body['serviceUrl']
    }

    if event_body['type'] == 'message':
        if 'text' in event_body:
            msgObject = {
                'type': 'text',
                'value': event_body['text']
            }
    elif event_body['type'] == 'message_back':
        msgObject = {
            'type': 'message_back',
            'value': event_body['message']
        }
    else:
        msgObject = {'type': 'conversationUpdate', 'value': None}

    outputBuilder = OutputBuilder(event_body)
    outputBuilder.typing_action()
    profileBuilder = profile_builder(userObject['convoId'], userObject['id'])
    stateRouter = StateRouter(userObject, msgObject, outputBuilder, profileBuilder)
    stateRouter.exe()
