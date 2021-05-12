from flask import Flask, request
from pymessenger import Bot
import pyshorteners

app = Flask(__name__)
bot = Bot('EAAT5zrtyvo8BAG0Jkpmuv7G2EWOOjcFB5YC1SNNL9QmkidGpAIBAZCZBzDU2jZBRJBJdKN80ZBLZCZCG7o1S03MTOpU3OR8ozZCNOa7mrnhTM9Y3yjRpTTkJtQy9KigQ1RtG86ZAhbqJAnEDIjRW5yNRIRP2Az8nqqtALKhTcP5jZAUbHsLZBkZCeBQ')
verify_token = 'isift'


def process_message(text):
    if text == "test":
        response = "Test Successful!"
    else:
        url = "https://isift.herokuapp.com/search?url=" + text
        response = 'Woohoo! Let’s see how this article breaks down shall we? Click here to view: ' \
                   + pyshorteners.Shortener().tinyurl.short(url)
    return response


@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == verify_token:
            return request.args.get("hub.challenge")
        else:
            return "Hello! Not connected to facebook"
    elif request.method == "POST":
        payload = request.json
        event = payload['entry'][0]['messaging']
        print(event)
        for msg in event:
            text = msg['message']['text']
            sender_id = msg['sender']['id']
            print(text)
            response = process_message(text)
            bot.send_text_message(sender_id, response)
        return "Message Received"
    else:
        return "200"


if __name__ == '__main__':
    app.run()
