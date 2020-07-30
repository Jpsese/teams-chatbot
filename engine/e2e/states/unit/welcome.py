def view(userObject, defaultResponse, outputBuilder):
    outputBuilder.send_card_postback(
        'welcome',
        defaultResponse['title'],
        defaultResponse['menuText'],
        None,
        defaultResponse['options'],
        None,
        None,
        defaultResponse['subtitle'],
        None
    )


def exe(userObject, msgObject, defaultResponse, context, outputBuilder):
    if msgObject['type'] == 'payload':
        print(msgObject['value']['index'])
        if msgObject['value']['index'] == 0:
            return 'checkin'
        elif msgObject['value']['index'] == 1:
            pass #health-check
        elif msgObject['value']['index'] == 2:
            pass #status

    return 'welcome'
