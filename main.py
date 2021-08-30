import os
import random
import gspread


from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, QuickReplyButton, MessageAction, QuickReply, TextSendMessage, ImageSendMessage, VideoSendMessage, StickerSendMessage, AudioSendMessage)

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'line-bot-test-324508-8fb79546f3b4.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open('gspreadサンプル').sheet1

wks.update_acell('A1', 'Hello World!')
print(wks.acell('A1'))

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def response_message(event):

    if event.message.text == "Todo":

        language_list = ["make", "check", "finish"]

        items = [QuickReplyButton(action=MessageAction(
            label=f"{language}", text=f"I want {language} Today's todo list")) for language in language_list]

        messages = TextSendMessage(text="What do you want to do?",
                                   quick_reply=QuickReply(items=items))

        line_bot_api.reply_message(event.reply_token, messages=messages)

    elif event.message.text == "I want make Today's todo list":

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="No.1"))
        a = event.message.text
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="No.2"))
        b = event.message.text
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="No.3"))
        c = event.message.text
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="No.4"))
        d = event.message.text
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="No.5"))
        e = event.message.text

        for x in todolist:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text={todolist}))

    elif event.message.text == "I want check Today's todo list":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Todo"))

    elif event.message.text == "I want finish Today's todo list":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Todo"))

    else:
        message = event.message.text
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
