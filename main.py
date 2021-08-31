import os
import random


from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, QuickReplyButton, MessageAction, QuickReply, TextSendMessage, ImageSendMessage, VideoSendMessage, StickerSendMessage, AudioSendMessage, FollowEvent, FlexSendMessage, TemplateSendMessage, PostbackAction, ButtonsTemplate,
)


app = Flask(__name__)
num = 0

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


@ handler.add(MessageEvent, message=TextMessage)
def response_message(event):
    if event.message.text == "Todo":
        select_list = ["make", "check", "finish"]

        items = [QuickReplyButton(action=MessageAction(
            label=f"{select}", text=f"I want {select} Today's todo list")) for select in select_list]

        msg1 = TextSendMessage(text="What do you want to do?",
                               quick_reply=QuickReply(items=items))

        line_bot_api.reply_message(event.reply_token, messages=msg1)

    elif event.message.text == "I want make Today's todo list":
        setting_list = ["No.1", "No.2", "No.3"]

        items = [QuickReplyButton(action=PostbackAction(
            label=f"{setting}", data=f"{setting}")) for setting in setting_list]

        msg2 = TextSendMessage(text="select todo number!",
                               quick_reply=QuickReply(items=items))

        line_bot_api.reply_message(event.reply_token, messages=msg2)

    elif event.message.text == "I want check Today's todo list":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Todo"))

    elif event.message.text == "I want finish Today's todo list":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Todo"))

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Please enter\"Todo\""))


@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'No.1':

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='Hi'))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
