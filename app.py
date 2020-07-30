import os
import json
import requests
from flask import request
from flask_api import FlaskAPI

from endpoints import teams

app = FlaskAPI(__name__)


@app.route('/bot/webhooks/teams', methods=['POST'])
def bot_webhook():
    event = {
        'body': json.dumps(request.json)
    }
    teams.handler(event, {})

    return {
        'statusCode': 200,
        'body': json.dumps({
            'msg': 'OK'
        })
    }


if __name__ == '__main__':
    os.environ['dialogflow_token'] = '7c2dfaffdafe46dfa085c62d2c509b43'
    os.environ['chatbot_table'] = 'covid-chatbot'
    os.environ['db_region'] = 'ap-southeast-1'
    app.run('localhost', 3978)
