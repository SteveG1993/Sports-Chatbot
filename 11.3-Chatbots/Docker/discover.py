import os, slackclient

VALET_SLACK_NAME = os.environ.get('VALET_SLACK_NAME')
VALET_SLACK_TOKEN = os.environ.get('VALET_SLACK_TOKEN')
# initialize slack client
valet_slack_client = slackclient.SlackClient(VALET_SLACK_TOKEN)
# check if everything is alright
print(VALET_SLACK_NAME)
print(VALET_SLACK_TOKEN)

