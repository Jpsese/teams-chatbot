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
        if msgObject['value']['index'] == 0:
            pass
        elif msgObject['value']['index'] == 1:
            pass
        elif msgObject['value']['index'] == 2:
            pass
        elif msgObject['value']['index'] == 3:
            pass

    else:
        return 'checkin'