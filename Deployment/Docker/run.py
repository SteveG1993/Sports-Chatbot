import os, sys, slackclient, time, random
from time import sleep
from baseball_oracle import chatbot_responder



#resp = chatbot_responder()
#resp = chatbot_responder()
r2 = chatbot_responder()

# delay in seconds before checking for new events
SOCKET_DELAY       = 1

# slackbot environment variables
SLACK_NAME   = os.environ.get('SLACK_NAME')
SLACK_TOKEN  = os.environ.get('SLACK_TOKEN')

# Setup basic Slack client object
slack_client = slackclient.SlackClient(SLACK_TOKEN)

# Grabbing the ID for our bot so we can use it later
is_ok = slack_client.api_call("users.list").get('ok')
print(is_ok)
# find the id of our slack bot
if(is_ok):
    for user in slack_client.api_call("users.list").get('members'):
        if user.get('name') == SLACK_NAME:
            SLACK_ID = user.get('id')
            print("Your bot ID is: %s" % user.get('id'))

## We could update this to all files in all subdirectories
## However these are the files that are watched for modification
## which triggers a reload action in this file down the road.
watching = [__file__]
watched_mtimes = [(f, os.path.getmtime(f)) for f in watching]


user_messages = dict()

# how the bot is mentioned on slack
def get_mention(user):
    return '<@{user}>'.format(user=user)

slack_mention = get_mention(SLACK_ID)

def is_hi(message):
    tokens = [word.lower() for word in message.strip().split()]
    return any(g in tokens
               for g in ['hello', 'bonjour', 'hey', 'hi', 'sup', 'morning', 'hola', 'ohai', 'yo'])


def is_bye(message):
    tokens = [word.lower() for word in message.strip().split()]
    return any(g in tokens
               for g in ['bye', 'goodbye', 'revoir', 'adios', 'later', 'cya'])

def say_hi(user_mention):
    """Say Hi to a user by formatting their mention"""
    response_template = random.choice(['Sup, {mention}...',
                                       'Yo!',
                                       'Hola {mention}',
                                       'Bonjour!'])
    return response_template.format(mention=user_mention)


def say_bye(user_mention):
    """Say Goodbye to a user"""
    response_template = random.choice(['see you later, alligator...',
                                       'adios amigo',
                                       'Bye {mention}!',
                                       'Au revoir!'])
    return response_template.format(mention=user_mention)

def is_private(event):
    """Checks if private slack channel"""
    return event.get('channel').startswith('D')

def is_for_me(event):
    """Know if the message is dedicated to me"""
    # check if not my own event
    type = event.get('type')
    if type and type == 'message' and not(event.get('user') == SLACK_ID):
        # in case it is a private message return true
        if is_private(event):
            print("Recieved private message")
            return True
        # in case it is not a private message check mention
        text = event.get('text')
        channel = event.get('channel')
        print(slack_mention, text.strip().split())
        if slack_mention in text.strip().split():
            return True

def handle_message(message, user, channel, event=False):

    if message:

        if is_hi(message):
            user_mention = get_mention(user)
            post_message(message=say_hi(user_mention), channel=channel)
        elif is_bye(message):
            user_mention = get_mention(user)
            post_message(message=say_bye(user_mention), channel=channel)
        else:
            post_message(message=r2.get_response_line(message),channel=channel)
        # Capture messages for later use
        print("YOU PMESSDF US", message)
        if event['type'] == "message":
            user_messages[user] = message

def post_message(message, channel):
    slack_client.api_call('chat.postMessage', channel=channel,
                          text=message, as_user=True)

def run_bot():
    if slack_client.rtm_connect():

        print('--===[ %s (%s) is ONLINE ]===--' % (SLACK_NAME, SLACK_ID))

        while True:

            for f, mtime in watched_mtimes:

                if os.path.getmtime(f) != mtime:
                    print("Reloading %s" % SLACK_ID)
                    os.execv(sys.executable, ['python', '-u'] + sys.argv)

                event_list = slack_client.rtm_read()

                if len(event_list) > 0:

                    for event in event_list:
                        print(event)

                        if is_for_me(event):
                            print("It is for me")
                            handle_message(message=event.get('text'), user=event.get('user'), channel=event.get('channel'), event=event)
                time.sleep(SOCKET_DELAY)

    else:
        print('[!] Connection to Slack failed.')


## Are we running from the command line and this is the main file? Let's run!
if __name__ == "__main__":
    run_bot()
