import json

from engine.e2e.platforms.teams import TeamsOutputBuilder


class OutputBuilder:

    def __init__(self, event):
        self.outputBuilder = TeamsOutputBuilder(event)

    def typing_action(self):
        self.outputBuilder.typing()

    def send_text_message(self, text):
        self.outputBuilder.text_message(
            text
        )

    def send_card_postback(self, state, title, cardTitle, message, menus,
                           urlMenus=None, images=None, subTitle=None,
                           tapAction=None):
        buttons = []
        index = 0

        if menus:
            for menu in menus:
                buttons.append({
                    'type': 'imBack',
                    'title': menu,
                    'text': menu,
                    'value': menu
                })
                index += 1

        if urlMenus:
            for urlMenu in urlMenus:
                buttons.append({
                    'type': 'openUrl',
                    'title': urlMenu,
                    'value': urlMenu[urlMenu]
                })

        respObject = self.outputBuilder.hero_card(title, cardTitle, message,
                                                  buttons, images, subTitle,
                                                  tapAction)
