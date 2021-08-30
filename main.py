# gcp

import os
import random

from linebot.models import (
    MessageEvent, TextMessage, QuickReplyButton, MessageAction, QuickReply, TextSendMessage, ImageSendMessage, VideoSendMessage, StickerSendMessage, AudioSendMessage)
from linebot.exceptions import (
    InvalidSignatureError)
from linebot import (
    LineBotApi, WebhookHandler)
from flask import Flask, request, abort
import pandas as pd
from datetime import datetime, timedelta, timezone
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# タイムゾーンの生成
JST = timezone(timedelta(hours=+9), 'JST')


def auth():
    SP_CREDENTIAL_FILE = 'secret.json'
    SP_SCOPE = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]

    SP_SHEET_KEY = '1_CwFW_S-m58X25EWuiwMY6kWfotNui9ZTAriRUt9tXU'
    SP_SHEET = 'Todolist'

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        SP_CREDENTIAL_FILE, SP_SCOPE)
    gc = gspread.authorize(credentials)

    worksheet = gc.open_by_key(SP_SHEET_KEY).worksheet(SP_SHEET)
    return worksheet


#

def punch_in(todo):
    worksheet = auth()
    df = pd.DataFrame(worksheet.get_all_records())

    timestamp = datetime.now(JST)
    date = timestamp.strftime('%Y/%m/%d')
    punch_in = todo

    df = df.append({'Todolist': punch_in,
                   'Date': date}, ignore_index=True)
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())


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
            TextSendMessage(text="Please enter what you want to do"))
        a = event.message.text
        punch_in(a)

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
