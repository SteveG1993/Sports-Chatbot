FROM python:3.6
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
#CMD ["python", "/Users/steve/Documents/DSI-US-4/Projects/project-5/simple_bot/11.3-Chatbots/Docker/outside_program.py"]

ENV SLACK_TOKEN='xoxb-3171645816-395559020576-W9a5LBKekxmpnmQURZVCzd59'
ENV SLACK_NAME='sports_chatbot'
