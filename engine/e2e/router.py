import json
import os

from os import path
from engine.e2e.intentmanager.dialogflow import DialogFlow
from chatbotdb.dynamodb import Dynamodb

class StateRouter:
    def __init__(self, userObject, msgObject,
                 outputBuilder, profileBuilder=None):
        self.profileBuilder = profileBuilder
        self.userObject = userObject
        self.outputBuilder = outputBuilder
        self.msgObject = msgObject
        self.dialogflow = DialogFlow(
            userObject['id'],
            os.environ.get('dialogflow_token')
        )
        self.dynamodb = Dynamodb(
            os.environ.get('chatbot_table'),
            os.environ.get('db_region')
        )

    def _init_user(self, profileBuilder):
        stateObject = {
            'userId': self.userObject['id'],
            'state': 'welcome'
        }

        userProfile = profileBuilder(
            self.userObject['convoId'],
            self.userObject['id']
        )

        for key in self.userObject:
            print(key)

        for key in userProfile.keys():
            print(key)

        return stateObject

    def _get_user(self):
        dbResp = self.dynamodb.get_item({'user-id': self.userObject['id']})
        if 'Item' not in dbResp:
            return self._init_user(self.profileBuilder)
        dbResp = dbResp['Item']
        return dbResp

    def _intent_check(self, state, textInput):
        intentResult = self.dialogflow.get_intent(textInput)
        intentList = json.loads(open('engine/e2e/intentmanager/intent.json',
                                'r').read())
        if intentResult['intentName'] in intentList:
            intentMatched = intentList[intentResult['intentName']]

            print(intentMatched)
            if intentMatched['type'] == 'reply':
                self.outputBuilder.send_text_message("Thank you and goodbye")
                return 'EXIT'

            if intentMatched['type'] == 'route':
                return intentMatched['state']

    def _run_state_view(self, state):
        print(state)
        fileDir = 'engine/e2e/states/unit/'+state.replace('.', '/')+'.py'
        if not path.exists(fileDir):
            raise ValueError('State ()'+state+' not found')
        nextStateUnit = __import__('engine.e2e.states.unit.'+state, {}, {},
                                   [state])
        nextStateView = json.loads(open('engine/e2e/states/view/' +
                                   state + '.json').read())
        reroute = nextStateUnit.view({}, nextStateView, self.outputBuilder)



    def exe(self):
        user = self._get_user()

        # Check for message back activities
        if self.msgObject['type'] == 'message_back':
            self.outputBuilder.send_text_message(
                self.msgObject['value']
            )
            return

        # Check the intent of message
        if self.msgObject['type'] == 'text':
            state = self._intent_check({}, self.msgObject['value'])
            if state:
                if state == 'EXIT':
                    return
                else:
                    self._run_state_view(state)
                    return
        
        print('@Teams [state]: ' + user['state'])
        unit = __import__('engine.e2e.states.unit.'+user['state'], {}, {},
                          [user['state']])
        view = json.loads(open('engine/e2e/states/view/'+user['state']+'.json').read())

        if 'options' in view:
            if self.msgObject['type'] == 'text':
                index = 0
                for options in view['options']:
                    print(self.msgObject)
                    if options == self.msgObject['value']:
                        self.msgObject['type'] = 'payload'
                        self.msgObject['value'] = {'index': index}
                        break
                    index += 1

        print('@Teams executing: ' + user['state'])
        nextState = unit.exe(user, self.msgObject, view, None, self.outputBuilder)

        if nextState:
            self._run_state_view(nextState)
