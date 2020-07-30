import requests


class DialogFlow:

    def __init__(self, sessionId, clientAccessToken):
        self.URL = 'https://api.dialogflow.com/v1'
        self.sessionId = sessionId
        self.headers = {
            'Authorization': 'Bearer ' + clientAccessToken,
            'Content-Type': 'application/json'
        }

    def get_intent(self, textQuery):
        payload = {
            'query': textQuery,
            'lang': 'en',
            'sessionId': self.sessionId
        }
        result = requests.post(
            self.URL+'/query?v=20150910',
            headers=self.headers,
            json=payload
        ).json()

        return{
            'intentName': result['result']['metadata']['intentName'],
            'speech': result['result']['fulfillment']['speech']
        }
